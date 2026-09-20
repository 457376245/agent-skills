#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M4A Music Downloader
Downloads songs in M4A format (AAC audio, 256 kbps) using Bilibili's high-fidelity audio streams.
Automatically embeds title and artist metadata into the M4A container.
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

BAD_KEYWORDS = [
    '架子鼓', '吉他谱', '钢琴谱', '鼓谱', '教学', '教程',
    '翻唱', 'cover', '伴奏', '纯伴奏', '去人声', '消音',
    'reaction', '剪辑', '练习用', 'dj', '电音版', '重低音',
    '慢速', '加速', '降调', '升调', '卡拉ok', 'ktv版伴奏'
]
GOOD_KEYWORDS = ['无损', 'hi-res', '4k', '官方', 'mv', '纯享', '原曲', '专辑', '完整版', 'cd', 'flac']

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
        print(f"[WARN] Failed to refresh cookies: {e}", file=sys.stderr)

get_spi_cookies()

def search_bili(query, max_retries=3):
    global b_3, b_4
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

def pick_best(results, title, artist=""):
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
        for b in BAD_KEYWORDS:
            if b in t and b not in t_low:
                score -= 60
        for g in GOOD_KEYWORDS:
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

def sanitize(name):
    return re.sub(r'[\/\\:\*\?\"<>\|]', '_', name).strip()

def download_track(artist, title, output_dir, bitrate="256k"):
    os.makedirs(output_dir, exist_ok=True)
    clean_title = re.sub(r'\(.*?\)', '', title).strip()
    clean_artist = artist.split('、')[0].strip() if artist else ""

    if artist:
        filename = sanitize(f"{artist} - {title}.m4a")
        search_query = f"{clean_artist} {clean_title}".strip()
    else:
        filename = sanitize(f"{title}.m4a")
        search_query = clean_title

    target_path = os.path.join(output_dir, filename)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 500000:
        print(f"[SKIP] {filename} already exists ({os.path.getsize(target_path)/(1024*1024):.1f}MB)")
        return target_path

    results = search_bili(search_query)
    best = pick_best(results, title, artist)
    if not best:
        # Fallback with original query
        results = search_bili(f"{artist} {title}".strip())
        best = pick_best(results, title, artist)

    if not best:
        print(f"[FAIL] No audio source found for '{search_query}'", file=sys.stderr)
        return None

    bvid = best['bvid']
    video_title = re.sub('<[^<]+?>', '', best.get('title', ''))
    print(f"[SEARCH] Found: {bvid} ({best.get('duration')}) - {video_title}")

    cache_dir = os.path.join(output_dir, ".cache")
    os.makedirs(cache_dir, exist_ok=True)
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

    # Transcode to M4A with metadata
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
        print(f"[DONE] Saved: {target_path} ({sz_mb:.1f}MB)")
        return target_path
    else:
        print(f"[FAIL] ffmpeg encoding failed for {filename}", file=sys.stderr)
        return None

def process_file_list(file_path, output_dir, bitrate="256k", max_workers=4):
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

    print(f"Total songs in list: {len(tasks)}")
    success_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(download_track, artist, title, output_dir, bitrate): (artist, title) for artist, title in tasks}
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
    parser = argparse.ArgumentParser(description="Download songs in M4A format.")
    parser.add_argument('query', nargs='?', help="Song name or 'Artist Song'")
    parser.add_argument('--artist', '-a', help="Artist name", default="")
    parser.add_argument('--title', '-t', help="Song title", default="")
    parser.add_argument('--file', '-f', help="Path to a text file containing song list", default="")
    parser.add_argument('--output', '-o', help="Output directory", default=".")
    parser.add_argument('--bitrate', '-b', help="AAC bitrate (e.g. 256k, 320k)", default="256k")
    parser.add_argument('--workers', '-w', help="Concurrent workers for batch download", type=int, default=4)

    args = parser.parse_args()

    if args.file:
        process_file_list(args.file, os.path.abspath(args.output), args.bitrate, args.workers)
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

    download_track(artist, title, os.path.abspath(args.output), args.bitrate)

if __name__ == '__main__':
    main()
