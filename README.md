# Simple AI Solution

Simple AI Solution is a Flask web application that brings several practical
natural-language processing tools into one browser-based interface. Users can
enter text or upload audio and receive results without writing Python code.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/saif-siddiqui06/Simple-ai-solution)

## Features

- **Sentiment analysis:** Reports positive, neutral, negative, and compound
  sentiment scores and extracts frequent keywords.
- **Named entity recognition:** Identifies people, organizations, locations,
  dates, and other entities with spaCy.
- **Text summarization:** Selects the most informative sentences and displays
  the main keywords.
- **Topic modeling:** Uses Gensim LDA to find the strongest topic terms.
- **Text translation:** Translates text between supported language codes.
- **Speech recognition:** Transcribes supported WAV, AIFF, or FLAC audio using
  Google's speech-recognition service.
- **Question answering:** Selects the context sentence most relevant to a
  user's question. If Transformers is installed separately, the app can use a
  DistilBERT question-answering pipeline instead.

## Technology

- Python 3.10 and Flask
- NLTK, spaCy, Gensim, and VADER Sentiment
- Deep Translator and SpeechRecognition
- Bootstrap and Font Awesome
- Gunicorn for production serving

## Project Structure

```text
app.py              Flask routes and NLP functions
templates/          Jinja HTML pages
static/             CSS, JavaScript, images, audio, and sample files
requirements.txt    Production Python dependencies
Procfile            Production start command
render.yaml         Render deployment blueprint
runtime.txt         Python runtime version
```

Large local model checkpoints and the virtual environment are intentionally
excluded from Git. The running application does not use those checkpoint files.

## Local Setup

1. Clone the repository and enter its directory.
2. Create and activate a virtual environment.
3. Install the dependencies.
4. Start Flask.

```powershell
git clone https://github.com/saif-siddiqui06/Simple-ai-solution.git
cd Simple-ai-solution
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`. The health endpoint is available at
`http://localhost:5000/health`.

## Deploy On Render

This repository includes `render.yaml`, so it can be deployed as a Render
Blueprint:

1. Sign in to Render and select **New > Blueprint**.
2. Connect this GitHub repository.
3. Confirm the `simple-ai-solution` web service.
4. Deploy the blueprint.

The blueprint uses these commands:

```text
Build: pip install --upgrade pip && pip install -r requirements.txt
Start: gunicorn app:app --timeout 120
```

Translation, speech recognition, and initial NLTK resource downloads require
outbound internet access from the hosting service.

## Notes

- Use ISO language codes such as `hi`, `en`, `fr`, or `es` for translation.
- Speech recognition depends on Google's external recognition service.
- The first request to an NLP feature may be slower while resources initialize.
- Do not run Flask debug mode in production.

## License

This educational project is provided without a separate license file.
