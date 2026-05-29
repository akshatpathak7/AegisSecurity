import os
import logging
import sqlite3
import tempfile

import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'app.db')
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'vectorizer.pkl')
AUTO_BOOTSTRAP = os.environ.get('AEGIS_AUTO_BOOTSTRAP', '1') != '0'

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

ATTACK_TYPES = {
    'phishing': 'Phishing',
    'smishing': 'Smishing',
    'vishing': 'Vishing',
    'baiting': 'Baiting',
    'pretexting': 'Pretexting',
    'quid_pro_quo': 'Quid Pro Quo',
    'tailgating': 'Tailgating',
    'spear_phishing': 'Spear Phishing',
}


def get_db():
    ensure_database()
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


model = None
vectorizer = None


def ensure_database():
    if os.path.exists(DB_PATH):
        return
    if not AUTO_BOOTSTRAP:
        raise RuntimeError(f'Database not found at {DB_PATH}. Run python init_db.py before starting the app.')

    from init_db import init_db

    logger.info('Database not found. Initializing SQLite database.')
    init_db()


def load_model():
    global model, vectorizer
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        if not AUTO_BOOTSTRAP:
            logger.warning('Model artifacts are missing and automatic bootstrap is disabled.')
            return

        from model.train import train_model

        logger.info('Model artifacts not found. Training classifier.')
        train_model()

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)


def classify_text(text):
    if model is None or vectorizer is None:
        return {'error': 'Model not loaded'}

    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    probabilities = model.predict_proba(text_vectorized)[0]
    confidence = float(np.max(probabilities))

    if prediction == 'safe':
        return {
            'is_attack': False,
            'message': 'No threat detected',
            'confidence': round(confidence * 100, 1)
        }

    attack_label = ATTACK_TYPES.get(prediction, prediction.replace('_', ' ').title())
    return {
        'is_attack': True,
        'attack_type': prediction,
        'attack_label': attack_label,
        'message': f'Attack Detected — Type: {attack_label}',
        'confidence': round(confidence * 100, 1)
    }


def transcribe_audio(audio_file):
    try:
        import whisper
        model_whisper = whisper.load_model("base")
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            audio_file.save(tmp.name)
            result = model_whisper.transcribe(tmp.name)
            os.unlink(tmp.name)
            return result['text']
    except Exception as e:
        return None


# --- Routes ---

@app.route('/healthz')
def healthz():
    return jsonify({
        'ok': True,
        'database': os.path.exists(DB_PATH),
        'model': model is not None and vectorizer is not None
    })


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect')
def detect_page():
    return render_template('detect.html')


@app.route('/library')
def library_page():
    db = get_db()
    attacks = db.execute('SELECT * FROM attack_types ORDER BY name').fetchall()
    return render_template('library.html', attacks=attacks)


@app.route('/library/<slug>')
def library_detail(slug):
    db = get_db()
    attack = db.execute('SELECT * FROM attack_types WHERE slug = ?', (slug,)).fetchone()
    if not attack:
        return render_template('404.html'), 404
    return render_template('library_detail.html', attack=attack)


@app.route('/guidance/<attack_slug>')
def guidance_page(attack_slug):
    db = get_db()
    attack = db.execute('SELECT * FROM attack_types WHERE slug = ?', (attack_slug,)).fetchone()
    if not attack:
        return render_template('guidance.html', attack=None)
    return render_template('guidance.html', attack=attack)


@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html')


@app.route('/api/detect/text', methods=['POST'])
def detect_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({'error': 'Empty text'}), 400

    result = classify_text(text)
    return jsonify(result)


@app.route('/api/detect/email', methods=['POST'])
def detect_email():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        allowed = file.filename.lower().endswith(('.txt', '.eml'))
        if not allowed:
            return jsonify({'error': 'Only .txt and .eml files are allowed'}), 400

        content = file.read().decode('utf-8', errors='ignore')
    elif request.is_json:
        data = request.get_json()
        content = data.get('content', '').strip()
    else:
        return jsonify({'error': 'No email content provided'}), 400

    if not content:
        return jsonify({'error': 'Empty email content'}), 400

    result = classify_text(content)
    return jsonify(result)


@app.route('/api/detect/voice', methods=['POST'])
def detect_voice():
    if 'file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    transcript = transcribe_audio(file)
    if transcript is None:
        return jsonify({'error': 'Failed to transcribe audio. Ensure Whisper is installed.'}), 500

    result = classify_text(transcript)
    result['transcript'] = transcript
    return jsonify(result)


@app.route('/api/quiz/questions')
def get_quiz_questions():
    db = get_db()
    questions = db.execute(
        'SELECT id, question, option_a, option_b, option_c, option_d, correct_answer, explanation, category '
        'FROM quiz_questions ORDER BY RANDOM() LIMIT 10'
    ).fetchall()
    return jsonify([dict(q) for q in questions])


@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    data = request.get_json()
    if not data or 'answers' not in data:
        return jsonify({'error': 'No answers provided'}), 400

    answers = data['answers']
    db = get_db()

    results = []
    correct_count = 0

    for item in answers:
        qid = item.get('question_id')
        user_answer = item.get('answer')
        question = db.execute(
            'SELECT * FROM quiz_questions WHERE id = ?', (qid,)
        ).fetchone()

        if question:
            is_correct = user_answer == question['correct_answer']
            if is_correct:
                correct_count += 1
            results.append({
                'question_id': qid,
                'correct': is_correct,
                'correct_answer': question['correct_answer'],
                'explanation': question['explanation']
            })

    total = len(results)
    score = round((correct_count / total) * 100) if total > 0 else 0

    return jsonify({
        'score': score,
        'correct': correct_count,
        'total': total,
        'results': results
    })


@app.route('/api/library/search')
def search_library():
    query = request.args.get('q', '').strip().lower()
    db = get_db()
    if query:
        attacks = db.execute(
            "SELECT * FROM attack_types WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ? ORDER BY name",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
    else:
        attacks = db.execute('SELECT * FROM attack_types ORDER BY name').fetchall()
    return jsonify([dict(a) for a in attacks])


with app.app_context():
    ensure_database()
    load_model()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
