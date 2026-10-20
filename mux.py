import subprocess
from pathlib import Path
OUT = Path('output')
video = OUT / 'video.mp4'
audio = OUT / 'voice.mp3'
final = OUT / 'short_final.mp4'
cmd = [
    'ffmpeg','-hide_banner','-loglevel','error','-y',
    '-i', str(video),
    '-i', str(audio),
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    '-movflags', '+faststart',
    str(final)
]
subprocess.run(cmd, check=True)
print('Created', final)
