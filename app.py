# app.py

import os
from functools import lru_cache

from flask import Flask, render_template, request, redirect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import download
import spacy
import gensim
from gensim import corpora
from deep_translator import GoogleTranslator
import speech_recognition as sr

app = Flask(__name__)


# Load small NLTK resources during startup. Model-heavy resources are loaded lazily
# so the hosted app can boot quickly and fail only on the feature that needs them.
download('punkt', quiet=True)
download('stopwords', quiet=True)
try:
    download('punkt_tab', quiet=True)
except Exception:
    pass


@lru_cache(maxsize=1)
def get_sentiment_analyser():
    return SentimentIntensityAnalyzer()


@lru_cache(maxsize=1)
def get_nlp():
    return spacy.load('en_core_web_sm')


@lru_cache(maxsize=1)
def get_translator():
    return GoogleTranslator


@lru_cache(maxsize=1)
def get_qa_pipeline():
    try:
        from transformers import pipeline
    except ImportError:
        return None

    return pipeline(
        'question-answering',
        model='distilbert-base-uncased-distilled-squad',
        tokenizer='distilbert-base-uncased-distilled-squad',
    )

def analyze_sentiment(text):
    analyser = get_sentiment_analyser()
    sentiment_score = analyser.polarity_scores(text)
    return sentiment_score

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    freq_dist = FreqDist(filtered_words)
    keywords = freq_dist.most_common(5)
    return keywords

def summarize_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    freq_dist = FreqDist(filtered_words)
    sentences = sent_tokenize(text)
    sentence_scores = {}
    
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freq_dist:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = freq_dist[word]
                else:
                    sentence_scores[sentence] += freq_dist[word]
    
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:3]
    summary = ' '.join(summary_sentences)
    return summary

def perform_topic_modeling(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    if not filtered_words:
        return []
    
    dictionary = corpora.Dictionary([filtered_words])
    doc_term_matrix = [dictionary.doc2bow(filtered_words)]
    
    lda_model = gensim.models.ldamodel.LdaModel(doc_term_matrix, num_topics=1, id2word=dictionary, passes=10)
    topics = lda_model.print_topics(num_words=5)
    return topics

def translate_text(text, target_language):
    translator = get_translator()
    return translator(source='auto', target=target_language).translate(text)

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    return text

def answer_question(question, context):
    qa_pipeline = get_qa_pipeline()
    if qa_pipeline is None:
        question_words = {
            word.lower()
            for word in word_tokenize(question)
            if word.isalnum() and word.lower() not in stopwords.words('english')
        }
        sentences = sent_tokenize(context)
        if not sentences:
            return 'No context was provided.'
        best_sentence = max(
            sentences,
            key=lambda sentence: len(question_words.intersection(word.lower() for word in word_tokenize(sentence))),
        )
        return best_sentence

    result = qa_pipeline({
        'question': question,
        'context': context
    })
    return result['answer']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sentiment-analysis', methods=['GET', 'POST'])
def sentiment_analysis():
    if request.method == 'POST':
        text = request.form['text']
        sentiment = analyze_sentiment(text)
        keywords = extract_keywords(text)
        return render_template('sentiment_analysis.html', text=text, sentiment=sentiment, keywords=keywords)
    return render_template('sentiment_analysis.html')

@app.route('/ner', methods=['GET', 'POST'])
def ner():
    if request.method == 'POST':
        text = request.form['text']
        nlp = get_nlp()
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return render_template('ner.html', text=text, entities=entities)
    return render_template('ner.html')

@app.route('/text-summarization', methods=['GET', 'POST'])
def text_summarization():
    if request.method == 'POST':
        text = request.form['text']
        summary = summarize_text(text)
        keywords = extract_keywords(text)
        return render_template('text_summarization.html', text=text, summary=summary, keywords=keywords)
    return render_template('text_summarization.html')

@app.route('/topic-modeling', methods=['GET', 'POST'])
def topic_modeling():
    if request.method == 'POST':
        text = request.form['text']
        topics = perform_topic_modeling(text)
        return render_template('topic_modeling.html', text=text, topics=topics)
    return render_template('topic_modeling.html')

@app.route('/text-translation', methods=['GET', 'POST'])
def text_translation():
    if request.method == 'POST':
        text = request.form['text']
        target_language = request.form['language']
        translated_text = translate_text(text, target_language)
        return render_template('text_translation.html', text=text, translated_text=translated_text, language=target_language)
    return render_template('text_translation.html')

@app.route('/speech-recognition', methods=['GET', 'POST'])
def speech_recognition():
    if request.method == 'POST':
        if 'audio' not in request.files:
            return redirect(request.url)
        audio_file = request.files['audio']
        transcribed_text = transcribe_audio(audio_file)
        return render_template('speech_recognition.html', transcribed_text=transcribed_text)
    return render_template('speech_recognition.html')

@app.route('/question-answering', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        question = request.form['question']
        context = request.form['context']
        answer = answer_question(question, context)
        return render_template('qa.html', question=question, context=context, answer=answer)
    return render_template('qa.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes'}
    app.run(host='0.0.0.0', port=port, debug=debug)
