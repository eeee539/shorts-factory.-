# Shorts Factory v3

Что умеет:
- рендерит вертикальное видео 1080x1920 30 fps
- делает полную озвучку через edge-tts
- склеивает видео и аудио в `output/short_final.mp4`
- может залить ролик на YouTube как private, если задать GitHub Secrets

## Локальный запуск
```bash
pip install -r requirements.txt
python run_all.py
```

## Нужные GitHub Secrets для автозагрузки
- `YOUTUBE_CLIENT_SECRET_JSON`
- `YOUTUBE_TOKEN_JSON`

## Управление через переменные среды
- `UPLOAD_TO_YOUTUBE=true`
- `YT_TITLE=...`
- `YT_DESCRIPTION=...`
- `YT_PRIVACY_STATUS=private`
