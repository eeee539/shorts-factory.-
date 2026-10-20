"""Offline Piper speech synthesis, avoiding Microsoft websocket 403."""
import subprocess
from pathlib import Path

OUT = Path('output')
OUT.mkdir(exist_ok=True)
text = Path('narration.txt').read_text(encoding='utf-8').strip()
voice = 'ru_RU-dmitri-medium'
model = OUT / f'{voice}.onnx'
base = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/dmitri/medium/'
for filename in (voice + '.onnx', voice + '.onnx.json'):
    dest = OUT / filename
    if not dest.exists():
        subprocess.run(['curl', '-fL', '--retry', '3', '--retry-delay', '2', '-o', str(dest), base + filename], check=True)
subprocess.run(['piper', '--model', str(model), '--output_file', str(OUT/'voice.wav')], input=text, text=True, check=True)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(OUT/'voice.wav'), '-c:a', 'libmp3lame', '-q:a', '3', str(OUT/'voice.mp3')], check=True)
print('Generated offline voice:', OUT/'voice.mp3')
