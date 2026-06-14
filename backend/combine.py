# combine.py
# Combine ML model prediction + heuristic rules into a final verdict

import joblib
import pandas as pd
from features import extract_features
from heuristics import check_heuristics

# Load the trained ML model (from Day 2)
model = joblib.load('phishing_model.pkl')


def analyze_url(url):
    """
    Input  : URL string
    Output : Dictionary with full analysis:
             - ml_score       → ML model's phishing probability (0-100)
             - heuristic_score→ heuristic risk score (0-100)
             - final_score    → combined weighted score (0-100)
             - verdict        → 'SAFE', 'SUSPICIOUS', or 'PHISHING'
             - flags          → list of triggered heuristic rules
             - features       → all extracted features
    """

    # ── Step 1: Extract features (Day 1) ──────────────────
    features = extract_features(url)

    # ── Step 2: ML model prediction (Day 2) ────────────────
    df = pd.DataFrame([features])
    probabilities = model.predict_proba(df)[0]
    # probabilities[1] = probability of being phishing (label 1)
    ml_score = probabilities[1] * 100

    # ── Step 3: Heuristic rules (Day 3) ────────────────────
    heuristic_result = check_heuristics(url)
    heuristic_score = heuristic_result['risk_score']
    flags = heuristic_result['flags']

    # ── Step 4: Combine with weights ───────────────────────
    # ML gets 60% weight, heuristics get 40% weight
    final_score = (ml_score * 0.6) + (heuristic_score * 0.4)

    # ── Step 5: Decide final verdict ───────────────────────
    if final_score <= 30:
        verdict = "SAFE"
    elif final_score <= 60:
        verdict = "SUSPICIOUS"
    else:
        verdict = "PHISHING"

    return {
        'url': url,
        'ml_score': round(ml_score, 1),
        'heuristic_score': heuristic_score,
        'final_score': round(final_score, 1),
        'verdict': verdict,
        'flags': flags,
        'features': features
    }


# ── TEST SECTION ──────────────────────────────────────────
if __name__ == "__main__":

    test_urls = [
        "http://paypa1-login-secure-verify.ru/account/confirm",
        "https://www.google.com/search",
        "http://192.168.1.1/bank/login",
        "https://www.amazon.com/orders",
        "http://user@evil-site.com/paypal/login",
        "https://www.spotify.com/playlist",
    ]

    for url in test_urls:
        result = analyze_url(url)
        print(f"\n{'='*65}")
        print(f"URL: {result['url']}")
        print(f"{'='*65}")
        print(f"ML Score        : {result['ml_score']}%")
        print(f"Heuristic Score : {result['heuristic_score']}/100")
        print(f"FINAL SCORE     : {result['final_score']}/100")
        print(f"VERDICT         : {result['verdict']}")
        if result['flags']:
            print("Red Flags:")
            for flag in result['flags']:
                print(f"  ⚠ {flag}")