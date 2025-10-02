#!/usr/bin/env python3
#python extract_frames.py clip_2m41s_720p25.mp4 data/clip/images
#python extract_frames.py clip_2m41s_720p25.mp4
import subprocess
import shlex
import sys
from pathlib import Path

def extract_frames(video_path, out_dir="data/clip/images"):
    """
    Ekstrak semua frame dari video ke folder out_dir.
    Nama file frame: 000001.jpg, 000002.jpg, dst.
    """
    video_path = Path(video_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # command ffmpeg
    cmd = f"ffmpeg -i {shlex.quote(str(video_path))} -vsync 0 {shlex.quote(str(out_dir))}/%06d.jpg"
    print("Running:", cmd)
    subprocess.run(cmd, shell=True, check=True)
    print(f"Selesai. Frame tersimpan di: {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_frames.py <video_file> [output_dir]")
        sys.exit(1)

    video_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/clip/images"
    extract_frames(video_file, output_dir)
