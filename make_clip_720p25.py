#!/usr/bin/env python3
import subprocess
import shlex

# input video (asli)
INPUT = "clip_1m3s.mp4"
# output video (target)
OUTPUT = "clip_1m3s_720p25.mp4"

# ffmpeg command: ubah resolusi ke 1280x720 dan FPS ke 25
cmd = f"ffmpeg -y -i {shlex.quote(INPUT)} -vf scale=1280:720,fps=25 -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p {shlex.quote(OUTPUT)}"

print("Running:", cmd)
subprocess.run(cmd, shell=True, check=True)
print("Selesai. File tersimpan di:", OUTPUT)
