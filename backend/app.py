# app.py
# Flask API — wraps our phishing detection logic into a web server

from flask import Flask, request, jsonify
from flask_cors import CORS
from combine import analyze_url

# ── Create the Flask app ──────────────────────────────────
app = Flask(__name__)

# ── Enable CORS ────────────────────────────────────────────
# This allows our React frontend (running on a different port)
# to send requests to this Flask server
CORS(app)


# ── Route 1: Health check ─────────────────────────────────
# Just to confirm the server is running
@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'message': 'Phishing Detector API is live!'
    })


# ── Route 2: Analyze a URL ─────────────────────────────────
# This is the MAIN endpoint our React frontend will call
@app.route('/api/analyze', methods=['POST'])
def analyze():
    # Step 1: Get the data sent by the client
    data = request.get_json()

    # Step 2: Check if 'url' key exists
    if not data or 'url' not in data:
        return jsonify({'error': 'Please provide a "url" field'}), 400

    url = data['url']

    # Step 3: Validate it's not empty
    if not url.strip():
        return jsonify({'error': 'URL cannot be empty'}), 400

    # Step 4: Run our analysis (Day 1-3 logic combined)
    try:
        result = analyze_url(url)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


# ── Run the server ──────────────────────────────────────────
if __name__ == '__main__':
    print("Starting Phishing Detector API...")
    print("Server running at: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)