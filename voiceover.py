import asyncio, os
from pathlib import Path
import edge_tts

TEXT = Path('narration.txt').read_text(encoding='utf-8').strip()
OUT = Path('output')
OUT.mkdir(exist_ok=True)
VOICE = os.getenv('TTS_VOICE', 'ru-RU-DmitryNeural')
RATE = os.getenv('TTS_RATE', '-3%')
PITCH = os.getenv('TTS_PITCH', '+0Hz')
VOL = os.getenv('TTS_VOLUME', '+0%')

async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE, pitch=PITCH, volume=VOL)
    await communicate.save(str(OUT / 'voice.mp3'))
    print('Created', OUT / 'voice.mp3')

asyncio.run(main())
