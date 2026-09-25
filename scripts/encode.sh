#!/usr/bin/env bash
# uso: FORMAT=300x600|160x600 BITRATE=830k scripts/encode.sh DIR_PNG   (sequenza 001.png ... 135.png)
# 1) master lossless RGB (bit-exact rispetto ai PNG)  2) MP4 distribuzione con gli stessi tag colore del master
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd); IN=$1; FMT=${FORMAT:-300x600}; BR=${BITRATE:-830k}; TMP=$(mktemp -d)
ffmpeg -hide_banner -loglevel error -y -framerate 15 -i "$IN/%03d.png" -c:v libx264rgb -qp 0 -preset veryslow -pix_fmt rgb24 \
  "$ROOT/09_rebuild_master/SNAI_BonusSport_${FMT}_CORRETTO_master_lossless_rgb.mkv"
COMMON=(-framerate 15 -i "$IN/%03d.png" -vf "setsar=1,format=yuvj420p" -c:v libx264 -preset veryslow -profile:v high -b:v $BR
        -passlogfile "$TMP/x264" -color_range pc -colorspace bt709 -color_primaries bt709 -color_trc iec61966-2-1 -an)
ffmpeg -hide_banner -loglevel error -y "${COMMON[@]}" -pass 1 -f mp4 /dev/null
ffmpeg -hide_banner -loglevel error -y "${COMMON[@]}" -pass 2 -movflags +faststart "$ROOT/11_distribuzione/SNAI_BonusSport_${FMT}_CORRETTO.mp4"
rm -rf "$TMP"
