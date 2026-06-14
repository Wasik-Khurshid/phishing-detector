# dataset.py
# Create a sample dataset of URLs labeled as phishing (1) or safe (0)

import pandas as pd
from features import extract_features  # our function from Day 1

# A small list of example URLs with their labels
# 1 = Phishing, 0 = Safe (Legitimate)
urls_data = [
    # Phishing examples
    ("http://paypa1-login.ru/secure/verify", 1),
    ("http://192.168.1.1/paypal/login", 1),
    ("http://secure-update-account.com/login/verify", 1),
    ("http://amaz0n-security-check.com/signin", 1),
    ("http://bank-of-america.verify-account.net/login", 1),
    ("http://www.paypal-secure-login.tk/account", 1),
    ("http://apple-id-locked.com/unlock/verify", 1),
    ("http://192.168.0.5/banking/secure/login", 1),
    ("http://netflix-billing-update.com/payment", 1),
    ("http://facebook-security-alert.com/login/confirm", 1),
    ("http://login-verify-account-now.ru/secure", 1),
    ("http://update-your-info-paypal.com/login", 1),
    ("http://signin-ebay-account.com/secure/verify", 1),
    ("http://microsoft-account-locked.tk/verify", 1),
    ("http://confirm-your-identity-bank.com/login", 1),

    # Safe examples
    ("https://www.google.com/search", 0),
    ("https://www.amazon.com/orders", 0),
    ("https://www.facebook.com/profile", 0),
    ("https://www.paypal.com/signin", 0),
    ("https://www.netflix.com/browse", 0),
    ("https://www.github.com/explore", 0),
    ("https://www.wikipedia.org/wiki/Python", 0),
    ("https://www.youtube.com/watch", 0),
    ("https://www.linkedin.com/feed", 0),
    ("https://www.microsoft.com/en-us", 0),
    ("https://www.apple.com/store", 0),
    ("https://www.bankofamerica.com/login", 0),
    ("https://www.ebay.com/sl/sell", 0),
    ("https://www.instagram.com/explore", 0),
    ("https://www.twitter.com/home", 0),
]

# Extract features for each URL and build rows
rows = []
for url, label in urls_data:
    features = extract_features(url)
    features['label'] = label   # 1 = phishing, 0 = safe
    rows.append(features)

# Convert to a pandas DataFrame (table)
df = pd.DataFrame(rows)

# Save to a CSV file
df.to_csv('dataset.csv', index=False)

print("Dataset created successfully!")
print(f"Total rows: {len(df)}")
print(f"Phishing URLs: {df['label'].sum()}")
print(f"Safe URLs: {len(df) - df['label'].sum()}")
print("\nFirst 5 rows:")
print(df.head())