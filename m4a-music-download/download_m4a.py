#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Music Downloader (M4A / FLAC / MP3)
Primary engine: Direct lossless/Hi-Res stream retrieval via vehicle music API.
Fallback engine: Bilibili audio stream search and extraction via yt-dlp.
Supports output formats: M4A (AAC-LC, default 256k), FLAC (lossless), MP3 (up to 320k).
Automatically embeds title and artist metadata.
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
import re
import ast
import html
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== Bilibili Fallback Config ====================
BAD_KEYWORDS_BILI = [
    '架子鼓', '吉他谱', '钢琴谱', '鼓谱', '教学', '教程',
    '翻唱', 'cover', '伴奏', '纯伴奏', '去人声', '消音',
    'reaction', '剪辑', '练习用', 'dj', '电音版', '重低音',
    '慢速', '加速', '降调', '升调', '卡拉ok', 'ktv版伴奏'
]
GOOD_KEYWORDS_BILI = ['无损', 'hi-res', '4k', '官方', 'mv', '纯享', '原曲', '专辑', '完整版', 'cd', 'flac']

b_3 = ""
b_4 = ""

def get_spi_cookies():
    global b_3, b_4
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        spi_req = urllib.request.Request(
            'https://api.bilibili.com/x/frontend/finger/spi',
            headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15'}
        )
        c = json.loads(opener.open(spi_req, timeout=5).read())['data']
        b_3, b_4 = c['b_3'], c['b_4']
    except Exception as e:
        pass

def search_bili(query, max_retries=2):
    global b_3, b_4
    if not b_3:
        get_spi_cookies()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    kw = urllib.parse.quote(query)
    url = f'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={kw}&page_size=10'
    for attempt in range(max_retries):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://search.bilibili.com/',
            'Origin': 'https://search.bilibili.com',
            'Cookie': f'buvid3={b_3}; buvid4={b_4}'
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            res = json.loads(opener.open(req, timeout=6).read())
            if res.get('code') == 0:
                return res.get('data', {}).get('result', [])
        except Exception:
            time.sleep(0.5)
            get_spi_cookies()
    return []

def pick_best_bili(results, title, artist=""):
    if not results:
        return None
    best_score = -9999
    best_item = None
    t_low = title.lower()
    a_low = artist.lower() if artist else ""
    for it in results:
        t = re.sub('<[^<]+?>', '', it.get('title', '')).lower()
        author = it.get('author', '').lower()
        score = 100
        for b in BAD_KEYWORDS_BILI:
            if b in t and b not in t_low:
                score -= 60
        for g in GOOD_KEYWORDS_BILI:
            if g in t:
                score += 15
        if a_low and (a_low in t or a_low in author):
            score += 30
        dur = it.get('duration', '')
        try:
            p = list(map(int, dur.split(':')))
            sec = p[0]*60 + p[1] if len(p)==2 else p[0]*3600 + p[1]*60 + p[2]
            if sec < 90:
                score -= 100
            elif sec > 600:
                score -= 50
        except Exception:
            pass
        if score > best_score:
            best_score = score
            best_item = it
    return best_item

# ==================== Kuwo Lossless API ====================
def search_kuwo(query):
    kw = urllib.parse.quote(query)
    url = f'http://search.kuwo.cn/r.s?client=kt&all={kw}&ft=music&cluster=0&strategy=2012&encoding=utf8&rformat=json&vipver=1&p=0&rn=10'
    req = urllib.request.Request(url, headers={'User-Agent': 'okhttp/3.10.0'})
    try:
        raw = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', errors='ignore')
        raw = raw.replace('&nbsp;', ' ')
        data = ast.literal_eval(raw)
        return data.get('abslist', [])
    except Exception:
        return []

def pick_best_kuwo(results, title, artist=""):
    if not results:
        return None
    best_item = None
    best_score = -9999
    t_clean = re.sub(r'\(.*?\)', '', title).strip().lower()
    a_clean = artist.strip().lower() if artist else ""

    for item in results:
        s_name = html.unescape(item.get('SONGNAME', '')).lower()
        s_artist = html.unescape(item.get('ARTIST', '')).lower()
        formats = item.get('FORMATS', '')
        score = 100

        # Penalize non-studio versions unless explicitly requested
        for bad in ['live', '伴奏', '铃声', '翻唱', 'dj', '片段']:
            if bad in s_name and bad not in t_clean:
                score -= 40

        # Prefer lossless FLAC master availability
        if 'ALFLAC' in formats or 'HIRFLAC' in formats:
            score += 25

        # Artist match
        if a_clean:
            if a_clean == s_artist:
                score += 50
            elif a_clean in s_artist or s_artist in a_clean:
                score += 30
            else:
                score -= 30

        # Title match
        if t_clean == s_name:
            score += 40
        elif t_clean in s_name:
            score += 20

        if score > best_score:
            best_score = score
            best_item = item

    return best_item

def get_kuwo_stream_url(rid, preferred_format="flac"):
    """
    Fetch direct audio stream from vehicle endpoint.
    br options: 2000kflac, 320kmp3, 128kmp3
    """
    br_candidates = ["2000kflac", "320kmp3", "128kmp3"]
    if preferred_format == "mp3":
        br_candidates = ["320kmp3", "128kmp3", "2000kflac"]

    for br in br_candidates:
        url = (
            f"https://nmobi.kuwo.cn/mobi.s?f=web&user=0&source=kwplayerhd_ar_4.3.0.8_tianbao_T1A_qirui.apk"
            f"&type=convert_url_with_sign&rid={rid}&br={br}"
        )
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'okhttp/3.10.0'})
            res = json.loads(urllib.request.urlopen(req, timeout=5).read().decode('utf-8'))
            d = res.get('data', {})
            audio_url = d.get('url')
            fmt = d.get('format')
            if audio_url:
                return audio_url, fmt
        except Exception:
            continue
    return None, None

# ==================== Helpers ====================
def sanitize(name):
    return re.sub(r'[\/\\:\*\?\"<>\|]', '_', name).strip()

def download_file_stream(url, target_path):
    req = urllib.request.Request(url, headers={'User-Agent': 'okhttp/3.10.0'})
    with urllib.request.urlopen(req, timeout=30) as resp, open(target_path, 'wb') as f:
        while chunk := resp.read(64 * 1024):
            f.write(chunk)

# ==================== Core Download Logic ====================
def download_track(artist, title, output_dir, bitrate="256k", format_type="m4a"):
    os.makedirs(output_dir, exist_ok=True)
    format_type = format_type.lower()
    clean_title = re.sub(r'\(.*?\)', '', title).strip()
    clean_artist = artist.split('、')[0].strip() if artist else ""

    display_name = f"{artist} - {title}" if artist else title
    filename = sanitize(f"{display_name}.{format_type}")
    target_path = os.path.join(output_dir, filename)

    # Skip existing completed downloads
    min_size = 500000 if format_type != 'flac' else 3000000
    if os.path.exists(target_path) and os.path.getsize(target_path) > min_size:
        sz_mb = os.path.getsize(target_path) / (1024 * 1024)
        print(f"[SKIP] {filename} already exists ({sz_mb:.1f}MB)")
        return target_path

    cache_dir = os.path.join(output_dir, ".cache")
    os.makedirs(cache_dir, exist_ok=True)

    # ---------------- 1. Primary Engine: Kuwo Lossless API ----------------
    search_query = f"{clean_artist} {clean_title}".strip() if clean_artist else clean_title
    kw_results = search_kuwo(search_query)
    best_kw = pick_best_kuwo(kw_results, clean_title, clean_artist)
    if not best_kw and clean_artist:
        # Retry with reverse query
        kw_results = search_kuwo(f"{clean_title} {clean_artist}".strip())
        best_kw = pick_best_kuwo(kw_results, clean_title, clean_artist)

    if best_kw:
        rid = best_kw.get('MUSICRID', '').replace('MUSIC_', '')
        s_title = html.unescape(best_kw.get('SONGNAME', title))
        s_artist = html.unescape(best_kw.get('ARTIST', artist))
        pref_br = "320kmp3" if format_type == "mp3" else "2000kflac"
        stream_url, fmt = get_kuwo_stream_url(rid, pref_br)

        if stream_url:
            print(f"[KUWO] Found: {s_artist} - {s_title} (RID: {rid}, Stream: {fmt})")
            
            # Case A: User wants FLAC and source is FLAC -> Direct stream download
            if format_type == "flac" and fmt == "flac":
                try:
                    download_file_stream(stream_url, target_path)
                    sz_mb = os.path.getsize(target_path) / (1024 * 1024)
                    print(f"[DONE] Saved Lossless FLAC: {target_path} ({sz_mb:.1f}MB)")
                    return target_path
                except Exception as e:
                    print(f"[WARN] Kuwo FLAC stream download failed: {e}", file=sys.stderr)

            # Case B: User wants MP3 and source is MP3 -> Direct stream download
            elif format_type == "mp3" and fmt == "mp3":
                try:
                    download_file_stream(stream_url, target_path)
                    sz_mb = os.path.getsize(target_path) / (1024 * 1024)
                    print(f"[DONE] Saved 320k MP3: {target_path} ({sz_mb:.1f}MB)")
                    return target_path
                except Exception as e:
                    print(f"[WARN] Kuwo MP3 stream download failed: {e}", file=sys.stderr)

            # Case C: User wants M4A (or transcoding required)
            else:
                temp_audio = os.path.join(cache_dir, f"kw_{rid}.{fmt}")
                try:
                    download_file_stream(stream_url, temp_audio)
                    if format_type == "m4a":
                        ff_cmd = [
                            'ffmpeg', '-y', '-i', temp_audio,
                            '-vn', '-c:a', 'aac', '-b:a', bitrate,
                            '-metadata', f'title={title.strip()}',
                            '-metadata', f'artist={artist.strip()}',
                            target_path
                        ]
                    elif format_type == "flac":
                        ff_cmd = [
                            'ffmpeg', '-y', '-i', temp_audio,
                            '-vn', '-c:a', 'flac',
                            '-metadata', f'title={title.strip()}',
                            '-metadata', f'artist={artist.strip()}',
                            target_path
                        ]
                    else: # mp3
                        ff_cmd = [
                            'ffmpeg', '-y', '-i', temp_audio,
                            '-vn', '-c:a', 'libmp3lame', '-b:a', '320k',
                            '-metadata', f'title={title.strip()}',
                            '-metadata', f'artist={artist.strip()}',
                            target_path
                        ]

                    f_res = subprocess.run(ff_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                    if os.path.exists(temp_audio):
                        os.remove(temp_audio)

                    if f_res.returncode == 0 and os.path.exists(target_path) and os.path.getsize(target_path) > 100000:
                        sz_mb = os.path.getsize(target_path) / (1024 * 1024)
                        print(f"[DONE] Saved: {target_path} ({sz_mb:.1f}MB)")
                        return target_path
                except Exception as e:
                    print(f"[WARN] Transcode failed: {e}", file=sys.stderr)
                    if os.path.exists(temp_audio):
                        try:
                            os.remove(temp_audio)
                        except Exception:
                            pass

    # ---------------- 2. Fallback Engine: Bilibili ----------------
    print(f"[INFO] Lossless stream not available for '{search_query}', falling back to Bilibili...")
    bili_results = search_bili(search_query)
    best_bili = pick_best_bili(bili_results, title, artist)
    if not best_bili:
        bili_results = search_bili(f"{artist} {title}".strip())
        best_bili = pick_best_bili(bili_results, title, artist)

    if not best_bili:
        print(f"[FAIL] No audio source found for '{search_query}' on any engine", file=sys.stderr)
        return None

    bvid = best_bili['bvid']
    video_title = re.sub('<[^<]+?>', '', best_bili.get('title', ''))
    print(f"[BILI] Found: {bvid} ({best_bili.get('duration')}) - {video_title}")

    temp_pattern = os.path.join(cache_dir, f"{bvid}.%(ext)s")
    dl_cmd = [
        'yt-dlp', '--proxy', '', '-f', 'ba/b',
        '--no-playlist',
        '-o', temp_pattern,
        f'https://www.bilibili.com/video/{bvid}'
    ]
    res = subprocess.run(dl_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if res.returncode != 0:
        print(f"[FAIL] yt-dlp download failed for {bvid}: {res.stderr.strip()}", file=sys.stderr)
        return None

    temp_file = None
    for ext in ['.m4a', '.mp4', '.webm', '.ogg', '.m4s']:
        cand = os.path.join(cache_dir, f"{bvid}{ext}")
        if os.path.exists(cand):
            temp_file = cand
            break

    if not temp_file:
        print(f"[FAIL] Cached download not found for {bvid}", file=sys.stderr)
        return None

    if format_type == "flac":
        ff_cmd = [
            'ffmpeg', '-y', '-i', temp_file,
            '-vn', '-c:a', 'flac',
            '-metadata', f'title={title.strip()}',
            '-metadata', f'artist={artist.strip()}',
            target_path
        ]
    elif format_type == "mp3":
        ff_cmd = [
            'ffmpeg', '-y', '-i', temp_file,
            '-vn', '-c:a', 'libmp3lame', '-b:a', '320k',
            '-metadata', f'title={title.strip()}',
            '-metadata', f'artist={artist.strip()}',
            target_path
        ]
    else:  # default m4a
        ff_cmd = [
            'ffmpeg', '-y', '-i', temp_file,
            '-vn', '-c:a', 'aac', '-b:a', bitrate,
            '-metadata', f'title={title.strip()}',
            '-metadata', f'artist={artist.strip()}',
            target_path
        ]

    f_res = subprocess.run(ff_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    try:
        os.remove(temp_file)
    except Exception:
        pass

    if f_res.returncode == 0 and os.path.exists(target_path) and os.path.getsize(target_path) > 100000:
        sz_mb = os.path.getsize(target_path) / (1024 * 1024)
        print(f"[DONE] Saved (Bilibili): {target_path} ({sz_mb:.1f}MB)")
        return target_path
    else:
        print(f"[FAIL] Encoding failed for {filename}", file=sys.stderr)
        return None

def process_file_list(file_path, output_dir, bitrate="256k", format_type="m4a", max_workers=4):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [l.lstrip('\ufeff').strip() for l in f if l.strip()]

    tasks = []
    for line in lines:
        if '：' in line:
            title, artist = line.split('：', 1)
        elif ':' in line:
            parts = line.split(':', 1)
            if '：' in parts[1]:
                title, artist = parts[1].split('：', 1)
            else:
                title, artist = parts[0], parts[1]
        elif '-' in line:
            artist, title = line.split('-', 1)
        else:
            title, artist = line, ""
        tasks.append((artist.strip(), title.strip()))

    print(f"Total songs in list: {len(tasks)} (Format: {format_type.upper()})")
    success_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(download_track, artist, title, output_dir, bitrate, format_type): (artist, title)
            for artist, title in tasks
        }
        for future in as_completed(futures):
            res = future.result()
            if res:
                success_count += 1

    # Cleanup cache dir if empty
    cache_dir = os.path.join(output_dir, ".cache")
    if os.path.exists(cache_dir):
        try:
            os.rmdir(cache_dir)
        except Exception:
            pass

    print(f"\nCompleted: {success_count}/{len(tasks)} songs saved to {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Download songs in M4A / FLAC / MP3 format.")
    parser.add_argument('query', nargs='?', help="Song name or 'Artist Song'")
    parser.add_argument('--artist', '-a', help="Artist name", default="")
    parser.add_argument('--title', '-t', help="Song title", default="")
    parser.add_argument('--file', '-f', help="Path to a text file containing song list", default="")
    parser.add_argument('--output', '-o', help="Output directory", default=".")
    parser.add_argument('--format', '-m', choices=['m4a', 'flac', 'mp3'], default="m4a", help="Output format: m4a (default), flac, or mp3")
    parser.add_argument('--bitrate', '-b', help="Target bitrate for M4A/MP3 (e.g. 256k, 320k)", default="256k")
    parser.add_argument('--workers', '-w', help="Concurrent workers for batch download", type=int, default=4)

    args = parser.parse_args()

    if args.file:
        process_file_list(args.file, os.path.abspath(args.output), args.bitrate, args.format, args.workers)
        return

    if args.query:
        if '-' in args.query:
            p = args.query.split('-', 1)
            artist, title = p[0].strip(), p[1].strip()
        elif ' ' in args.query:
            p = args.query.split(' ', 1)
            artist, title = p[0].strip(), p[1].strip()
        else:
            artist, title = args.artist, args.query
    else:
        artist, title = args.artist, args.title

    if not title:
        parser.print_help()
        sys.exit(1)

    download_track(artist, title, os.path.abspath(args.output), args.bitrate, args.format)

if __name__ == '__main__':
    main()
