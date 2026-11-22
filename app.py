
import requests
from flask import Flask, jsonify, request, send_from_directory
from langdetect import detect, LangDetectException

app = Flask(__name__, static_folder='public', static_url_path='')

MAX_TEXT_LENGTH = 5000
MYMEMORY_URL = 'https://api.mymemory.translated.net/get'

LANGUAGES = [
    {'code': 'ar', 'name': 'Arabic'},
    {'code': 'bn', 'name': 'Bengali'},
    {'code': 'zh', 'name': 'Chinese'},
    {'code': 'nl', 'name': 'Dutch'},
    {'code': 'en', 'name': 'English'},
    {'code': 'fr', 'name': 'French'},
    {'code': 'de', 'name': 'German'},
    {'code': 'gu', 'name': 'Gujarati'},
    {'code': 'hi', 'name': 'Hindi'},
    {'code': 'id', 'name': 'Indonesian'},
    {'code': 'it', 'name': 'Italian'},
    {'code': 'ja', 'name': 'Japanese'},
    {'code': 'kn', 'name': 'Kannada'},
    {'code': 'ko', 'name': 'Korean'},
    {'code': 'ml', 'name': 'Malayalam'},
    {'code': 'mr', 'name': 'Marathi'},
    {'code': 'ne', 'name': 'Nepali'},
    {'code': 'pt', 'name': 'Portuguese'},
    {'code': 'ru', 'name': 'Russian'},
    {'code': 'es', 'name': 'Spanish'},
    {'code': 'ta', 'name': 'Tamil'},
    {'code': 'te', 'name': 'Telugu'},
    {'code': 'tr', 'name': 'Turkish'},
    {'code': 'uk', 'name': 'Ukrainian'}
]

def split_text(text, max_bytes=450):
    chunks = []
    current = ''

    for word in text.split():
        candidate = word if not current else current + ' ' + word

        if len(candidate.encode('utf-8')) <= max_bytes:
            current = candidate
        else:
            if current:
                chunks.append(current)

            if len(word.encode('utf-8')) > max_bytes:
                raise ValueError('One word is too long to translate.')

            current = word

    if current:
        chunks.append(current)

    return chunks


@app.get('/')
def home():
    return send_from_directory('public', 'index.html')


@app.get('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'service': 'language-translation-tool',
        'provider': 'MyMemory'
    })


@app.get('/api/languages')
def languages():
    return jsonify(LANGUAGES)


@app.post('/api/translate')
def translate():
    data = request.get_json(silent=True) or {}

    text = str(data.get('text', '')).strip()
    source = str(data.get('source', 'auto')).strip()
    target = str(data.get('target', '')).strip()

    if not text:
        return jsonify({'error': 'Please enter some text.'}), 400

    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({
            'error': 'Please keep text under 5000 characters.'
        }), 400

    if not target:
        return jsonify({
            'error': 'Please choose a target language.'
        }), 400

    if source == 'auto':
        try:
            source = detect(text)
        except LangDetectException:
            return jsonify({
                'error': 'Language detection failed. Please select a source language.'
            }), 400

    language_codes = {
        'zh': 'zh-CN',
        'no': 'nb'
    }

    source = language_codes.get(source, source)
    target = language_codes.get(target, target)

    if source.lower() == target.lower():
        return jsonify({
            'error': 'Choose two different languages.'
        }), 400

    try:
        chunks = split_text(text)
        translated_chunks = []

        for chunk in chunks:
            response = requests.get(
                MYMEMORY_URL,
                params={
                    'q': chunk,
                    'langpair': f'{source}|{target}'
                },
                timeout=25
            )

            response.raise_for_status()
            result = response.json()

            if result.get('responseStatus') != 200:
                return jsonify({
                    'error': result.get(
                        'responseDetails',
                        'Translation service unavailable.'
                    )
                }), 502

            translated = result.get(
                'responseData', {}
            ).get('translatedText', '')

            if not translated:
                return jsonify({
                    'error': 'No translation was returned.'
                }), 502

            translated_chunks.append(translated)

        return jsonify({
            'translatedText': ' '.join(translated_chunks),
            'detectedLanguage': source,
            'confidence': None
        })

    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    except requests.Timeout:
        return jsonify({
            'error': 'Translation took too long. Please try again.'
        }), 504

    except requests.RequestException:
        return jsonify({
            'error': 'Translation service is temporarily unavailable.'
        }), 502


if __name__ == '__main__':
    app.run(debug=True)
    
