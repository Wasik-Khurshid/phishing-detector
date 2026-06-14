# predict.py
# Use the trained model to predict if a URL is phishing or safe

import joblib
import pandas as pd
from features import extract_features

# Load the trained model
model = joblib.load('phishing_model.pkl')

def predict_url(url):
    # Step 1: Extract features (same as training)
    features = extract_features(url)

    # Step 2: Convert to a DataFrame (model expects table format)
    df = pd.DataFrame([features])

    # Step 3: Predict (0 = safe, 1 = phishing)
    prediction = model.predict(df)[0]

    # Step 4: Get confidence score
    probability = model.predict_proba(df)[0]
    confidence = max(probability) * 100

    return prediction, confidence


# ── TEST with your own URLs ───────────────────────────────
test_urls = [
    "http://paypal-secure-verify-account.com/login",
    "https://www.spotify.com/playlist",
    "http://192.168.1.5/bank/login",
    "https://www.reddit.com/r/python",
    "http://login-confirm-bank-update.ru/secure",
]

for url in test_urls:
    prediction, confidence = predict_url(url)
    result = "🚨 PHISHING" if prediction == 1 else "✅ SAFE"
    print(f"\nURL: {url}")
    print(f"Result: {result} (Confidence: {confidence:.1f}%)")