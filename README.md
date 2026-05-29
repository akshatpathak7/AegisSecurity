# Aegis Security

A Flask web app for social engineering awareness, detection, a learning library, and quizzes.

## Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python model/train.py
flask --app app run --port 5001
```

Open `http://127.0.0.1:5001`.

## Production Start

Use this start command on Python hosts:

```bash
gunicorn app:app --bind 0.0.0.0:${PORT:-8000}
```

Use this build/setup command before the app starts:

```bash
pip install -r requirements.txt && python init_db.py && python model/train.py
```

The app also bootstraps missing `data/app.db`, `model/model.pkl`, and `model/vectorizer.pkl` on startup by default. Set `AEGIS_AUTO_BOOTSTRAP=0` if you prefer startup to fail when build artifacts are missing.

## Deploying With Render

This repo includes `render.yaml`. On Render:

1. Create a new Blueprint or Web Service from this repository.
2. Use the included build command and start command.
3. After the service is live, add `aegissec.in` as your custom domain in Render and point your DNS records to the target Render gives you.

The health check endpoint is `/healthz`.

## Notes

Voice detection uses `openai-whisper`, `torch`, and system `ffmpeg`. This repo includes `apt.txt` for hosts that install apt packages during deploy. Text, email, library, and quiz features do not need `ffmpeg`.
