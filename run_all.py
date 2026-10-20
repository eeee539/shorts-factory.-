import os, subprocess
steps = [
    ['python', 'generate.py'],
    ['python', 'voiceover.py'],
    ['python', 'mux.py'],
]
for step in steps:
    subprocess.run(step, check=True)
if os.getenv('UPLOAD_TO_YOUTUBE', 'false').lower() == 'true':
    subprocess.run(['python', 'upload_to_youtube.py'], check=True)
