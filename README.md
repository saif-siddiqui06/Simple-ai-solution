# Simple AI Solution

Flask web app that demonstrates common AI/NLP features:

- Sentiment analysis and keyword extraction
- Named entity recognition
- Text summarization
- Topic modeling
- Text translation
- Speech recognition
- Question answering

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## Deployment

The app includes a `Procfile` for platforms such as Render, Railway, or Heroku-compatible hosts.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```
