# combine.py — Updated for new 11,054 URL trained model

import joblib
import pandas as pd
from heuristics import check_heuristics

# Load trained model and feature names
model = joblib.load('phishing_model.pkl')
model_features = joblib.load('model_features.pkl')


def extract_model_features(url):
    import re
    import urllib.parse

    features = {}
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    features['UsingIP']             = 1  if re.search(ip_pattern, domain) else -1
    features['LongURL']             = 1  if len(url) > 54 else -1
    features['ShortURL']            = 1  if len(url) < 20 else -1
    features['Symbol@']             = 1  if '@' in url else -1
    features['Redirecting//']       = 1  if '//' in url[7:] else -1
    features['PrefixSuffix-']       = 1  if '-' in domain else -1
    features['SubDomains']          = 1  if domain.count('.') > 2 else -1
    features['HTTPS']               = -1 if url.startswith('https') else 1
    features['DomainRegLen']        = 1  if len(domain) > 20 else -1
    features['Favicon']             = -1
    features['NonStdPort']          = 1  if ':' in domain else -1
    features['HTTPSDomainURL']      = 1  if 'https' in domain else -1
    features['RequestURL']          = 1  if len(path) > 20 else -1
    features['AnchorURL']           = -1
    features['LinksInScriptTags']   = -1
    features['ServerFormHandler']   = -1
    features['InfoEmail']           = 1  if 'mail' in url.lower() else -1
    features['AbnormalURL']         = 1  if domain not in url else -1
    features['WebsiteForwarding']   = -1
    features['StatusBarCust']       = -1
    features['DisableRightClick']   = -1
    features['UsingPopupWindow']    = -1
    features['IframeRedirection']   = -1
    features['AgeofDomain']         = 1
    features['DNSRecording']        = -1
    features['WebsiteTraffic']      = -1
    features['PageRank']            = -1
    features['GoogleIndex']         = -1
    features['LinksPointingToPage'] = -1
    features['StatsReport']         = -1

    return features


def analyze_url(url):
    # ── ML Model prediction ───────────────────────────────
    features = extract_model_features(url)
    df = pd.DataFrame([features])[model_features]

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0]

    classes = list(model.classes_)
    phishing_idx = classes.index(-1)
    legit_idx = classes.index(1)

    phish_prob = probability[phishing_idx] * 100
    legit_prob = probability[legit_idx] * 100

    # prediction == 1 = LEGITIMATE, prediction == -1 = PHISHING
    if prediction == 1:
        ml_score = max(0, 100 - legit_prob)
    else:
        ml_score = phish_prob

    # ── Heuristic rules ───────────────────────────────────
    heuristic_result = check_heuristics(url)
    heuristic_score = heuristic_result['risk_score']
    flags = heuristic_result['flags']

    # ── Combine ───────────────────────────────────────────
    final_score = (ml_score * 0.6) + (heuristic_score * 0.4)

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


# ── TEST ──────────────────────────────────────────────────
if __name__ == "__main__":
    test_urls = [
        "http://paypa1-login-secure-verify.ru/account/confirm",
        "https://www.google.com/search",
        "http://192.168.1.1/bank/login",
        "https://www.amazon.com/orders",
        "http://amazon-security-alert.tk/signin/verify",
    ]

    for url in test_urls:
        result = analyze_url(url)
        print(f"\n{'='*55}")
        print(f"URL     : {result['url']}")
        print(f"ML Score: {result['ml_score']}%")
        print(f"Heuristic: {result['heuristic_score']}/100")
        print(f"FINAL   : {result['final_score']}/100")
        print(f"VERDICT : {result['verdict']}")
        if result['flags']:
            for flag in result['flags']:
                print(f"  ⚠ {flag}")