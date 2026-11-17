#!/bin/bash
# Nén video cho deck: H.264 + AAC, tối đa 1080p, faststart.
# compress_video.sh <vào> <ra.mp4> [crf=25]   (video dài/nặng >60MB: dùng 27; CRF càng cao càng nhẹ)
set -e
FF="${FFMPEG:-$(command -v ffmpeg)}"
[ -n "$FF" ] || { echo "Cần ffmpeg (macOS: brew install ffmpeg · Windows: winget install Gyan.FFmpeg) hoặc đặt biến FFMPEG"; exit 1; }
"$FF" -y -v error -stats -i "$1" -vf "scale='if(gt(ih,1080),-2,iw)':'min(ih,1080)'" -c:v libx264 -preset slow -crf "${3:-25}" \
  -pix_fmt yuv420p -profile:v high -c:a aac -b:a 128k -movflags +faststart "$2"
ls -la "$2"
