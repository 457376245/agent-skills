---
name: m4a-music-download
description: Download single songs or batch playlists in M4A (AAC-LC 256 kbps), FLAC (true lossless Hi-Res), or MP3 format with embedded title and artist metadata. Uses direct vehicle lossless stream API as primary engine with Bilibili as fallback. Use when the user asks to download songs/music, download M4A, FLAC, or AAC files, batch download from a song list, or says "下载歌曲", "下载音乐", "下载M4A", "下载FLAC", "下载无损", "下载周杰伦...", "批量下载歌曲".
---

# Music Downloader (M4A / FLAC / MP3)

Download official high-fidelity music files in **M4A (AAC 256k)**, **FLAC (24-bit/16-bit Lossless Hi-Res)**, or **MP3 (320k)** directly with embedded title and artist metadata.

## Capabilities

1. **Dual Engine Architecture**:
   - **Primary Engine**: Direct lossless stream retrieval from vehicle high-resolution music endpoints. Pulls authentic 24-bit/16-bit FLAC master tracks.
   - **Fallback Engine**: Bilibili stream retrieval via `yt-dlp` if a track is unlisted on official streaming libraries.
2. **Multiple Format Support** (`--format` / `-m`):
   - `m4a` (Default): First-generation AAC-LC encode (256 kbps stereo) from lossless master via FFmpeg.
   - `flac`: Direct lossless bit-for-bit stream download (pure Python standard library, no FFmpeg needed).
   - `mp3`: High-bitrate 320 kbps MP3.
3. **Single & Batch Downloads**:
   - Single track by query (e.g. `周杰伦 晴天`) or explicit `--artist` and `--title`.
   - Batch text playlist (`歌名：歌手` or `歌手 - 歌名`) with concurrent multi-threading.
4. **Metadata & Deduplication**:
   - Automatically embeds `title` and `artist` tags.
   - Automatically skips existing completed files.

## Execution

The skill includes a self-contained Python CLI tool in this skill directory (`download_m4a.py`; resolve relative to this `SKILL.md`'s parent directory when invoking):

```text
download_m4a.py
```

### 1. Download Single Song

**Default M4A (AAC 256k):**
```bash
python "download_m4a.py" "周杰伦 晴天" -o "C:/tmp/music"
```

**Lossless FLAC (Hi-Res 24-bit):**
```bash
python "download_m4a.py" "周杰伦 晴天" -o "C:/tmp/music" --format flac
```

**Explicit Artist & Title with Custom Bitrate:**
```bash
python "download_m4a.py" --artist "周杰伦" --title "晴天" -o "C:/tmp/music" --bitrate "320k"
```

### 2. Batch Download from File List

Supports formats: `歌名：歌手`, `序号:歌名：歌手`, or `歌手 - 歌名`:

```bash
python "download_m4a.py" -f "C:/tmp/music/music_list.txt" -o "C:/tmp/music" --format m4a -w 5
```

- `-f, --file`: Path to the text list of songs.
- `-o, --output`: Target directory.
- `-m, --format`: Output format: `m4a` (default), `flac`, or `mp3`.
- `-b, --bitrate`: Target AAC/MP3 bitrate (default: `256k`).
- `-w, --workers`: Number of concurrent workers (default: `4`).

## Dependencies

- **Python 3.10+** (Standard library only).
- **FFmpeg**: Required for M4A/MP3 encoding. (Not required when downloading direct FLAC).
- **yt-dlp**: Optional fallback for Bilibili source.

## Output Convention

- Filename: `{歌手} - {歌名}.{ext}` (or `{歌名}.{ext}` if artist unknown).
- Tags: embedded `title` and `artist`.
