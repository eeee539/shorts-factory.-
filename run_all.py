import os, subprocess
# Speech first, then render visuals to the exact length of the narration.
for step in [['python', 'voiceover.py'], ['python', 'generate.py'], ['python', 'mux.py']]:
    subprocess.run(step, check=True)
if os.getenv('UPLOAD_TO_YOUTUBE', 'false').lower() == 'true':
    subprocess.run(['python', 'upload_to_youtube.py'], check=True)
