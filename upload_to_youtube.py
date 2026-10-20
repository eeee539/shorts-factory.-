"""Upload output/short_final.mp4 to YouTube as private.
Requires secrets:
  YOUTUBE_CLIENT_SECRET_JSON
  YOUTUBE_TOKEN_JSON
Optional env:
  YT_TITLE, YT_DESCRIPTION, YT_TAGS, YT_PRIVACY_STATUS
"""
import json, os, tempfile
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

video_path = Path('output/short_final.mp4')
if not video_path.exists():
    raise FileNotFoundError(video_path)
client_secret_json = os.getenv('YOUTUBE_CLIENT_SECRET_JSON')
token_json = os.getenv('YOUTUBE_TOKEN_JSON')
if not client_secret_json or not token_json:
    raise SystemExit('Skipping upload: missing YOUTUBE_CLIENT_SECRET_JSON or YOUTUBE_TOKEN_JSON.')
creds_data = json.loads(token_json)
creds = Credentials(
    token=creds_data.get('token'),
    refresh_token=creds_data.get('refresh_token'),
    token_uri=creds_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
    client_id=creds_data.get('client_id'),
    client_secret=creds_data.get('client_secret'),
    scopes=creds_data.get('scopes', ['https://www.googleapis.com/auth/youtube.upload'])
)
youtube = build('youtube', 'v3', credentials=creds)
body = {
    'snippet': {
        'title': os.getenv('YT_TITLE', 'Странное оповещение в 03:17'),
        'description': os.getenv('YT_DESCRIPTION', 'Автоматически сгенерированный тестовый Shorts.'),
        'tags': [t.strip() for t in os.getenv('YT_TAGS', 'shorts,история,мистика').split(',') if t.strip()],
        'categoryId': '24'
    },
    'status': {
        'privacyStatus': os.getenv('YT_PRIVACY_STATUS', 'private'),
        'selfDeclaredMadeForKids': False
    }
}
media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype='video/mp4')
request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
response = None
while response is None:
    _, response = request.next_chunk()
print('Uploaded video ID:', response['id'])
