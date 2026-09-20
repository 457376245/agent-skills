---
name: m4a-music-download
description: Download single songs or batch playlists in M4A format (AAC audio, 256 kbps) with embedded title and artist metadata. Searches Bilibili high-fidelity audio streams, filters out covers/accompaniments/noise, extracts dash audio via yt-dlp, and encodes to M4A (.m4a) via ffmpeg. Use when the user asks to download songs/music, download M4A or AAC files, batch download from a song list, or says "下载歌曲", "下载音乐", "下载M4A", "下载周杰伦...", "批量下载歌曲".
---

# M4A Music Downloader

Download high-quality M4A audio files (MPEG-4 container, AAC-LC 256 kbps, 44.1 kHz stereo) with embedded title and artist tags directly to the target or current directory.

## Capabilities

1. **Single Song Download**: Downloads a single song by title and optional artist name (e.g. `周杰伦 晴天`).
2. **Batch List Download**: Reads a playlist/text file (`歌名：歌手` or `歌手 - 歌名`) and downloads all tracks concurrently.
3. **High Fidelity & Noise Filtering**:
   - Searches Bilibili audio tracks using dynamic SPI cookie authentication.
   - Automatically penalizes drum scores, accompaniments, amateur covers, reactions, tutorials, and sped-up/slowed-down audio.
   - Prioritizes official releases, Hi-Res, 4K MVs, studio albums, and full-length tracks.
   - Encodes with FFmpeg to standard M4A with embedded `title` and `artist` metadata tags.

## Execution

The skill includes a self-contained Python CLI tool:

```text
E:\tools\agent-skills\m4a-music-download\download_m4a.py
```

### 1. Download Single Song

```bash
python "E:/tools/agent-skills/m4a-music-download/download_m4a.py" "周杰伦 晴天" -o "C:/tmp/music"
```

Or specify artist and title explicitly:

```bash
python "E:/tools/agent-skills/m4a-music-download/download_m4a.py" --artist "周杰伦" --title "晴天" -o "C:/tmp/music" --bitrate "256k"
```

### 2. Batch Download from File List

Supports files formatted with colons (`歌名：歌手` or `序号:歌名：歌手`) or dashes (`歌手 - 歌名`):

```bash
python "E:/tools/agent-skills/m4a-music-download/download_m4a.py" -f "C:/tmp/music/music_list.txt" -o "C:/tmp/music" -w 5
```

- `-f, --file`: Path to the text list of songs.
- `-o, --output`: Target directory where `.m4a` files are saved.
- `-b, --bitrate`: Target AAC bitrate (default: `256k`).
- `-w, --workers`: Number of concurrent download workers (default: `4`).

## Dependencies

- **Python 3.10+** (standard library only).
- **yt-dlp**: Located in PATH or `D:\python3\Scripts\yt-dlp.exe`.
- **ffmpeg**: Located in PATH or `C:\Users\h4573\scoop\shims\ffmpeg.exe`.

## Output Convention

- Saved filename: `{歌手} - {歌名}.m4a` (or `{歌名}.m4a` if artist is unknown).
- Format: MPEG-4 Audio (`.m4a`), AAC-LC, 256 kbps, 44.1 kHz, Stereo, with embedded `title` and `artist` tags.
