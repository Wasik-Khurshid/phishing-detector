# features.py
# Extract important information from URLs

import re  # Regular expressions — for finding patterns

def extract_features(url):
    """
    This function takes a URL
    and returns 10 properties
    """
    features = {}  # Empty dictionary — all data stored here

    # 1. Total length of URL
    features['url_length'] = len(url)

    # 2. Does it have HTTPS? (1 = safe, 0 = risky)
    features['has_https'] = 1 if url.startswith('https') else 0

    # 3. How many dots? (paypal.secure.login.com = 3 dots = suspicious)
    features['dot_count'] = url.count('.')

    # 4. How many hyphens? (pay-pal-login-secure.com = suspicious)
    features['hyphen_count'] = url.count('-')

    # 5. Has '@' symbol? (http://user@evil.com = always suspicious)
    features['has_at_symbol'] = 1 if '@' in url else 0

    # 6. Does URL contain IP address directly? (http://192.168.1.1/login)
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    features['has_ip_address'] = 1 if re.search(ip_pattern, url) else 0

    # 7. How long is the domain?
    try:
        domain = url.split('/')[2]  # "http://evil.com/page" → "evil.com"
        features['domain_length'] = len(domain)
    except:
        features['domain_length'] = 0

    # 8. How many '/' slashes? (too many = suspicious)
    features['slash_count'] = url.count('/')

    # 9. Any suspicious words in URL?
    suspicious_words = ['login', 'secure', 'verify', 'update', 'bank', 'paypal']
    features['has_suspicious_words'] = 1 if any(w in url.lower() for w in suspicious_words) else 0

    # 10. Are there digits in the domain? (paypa1.com)
    try:
        domain = url.split('/')[2]
        features['digits_in_domain'] = sum(c.isdigit() for c in domain)
    except:
        features['digits_in_domain'] = 0

    return features


# --- TEST ---
if __name__ == "__main__":

    # Test with a phishing URL
    phishing_url = "http://paypa1-login.ru/secure/verify"
    print("=== PHISHING URL TEST ===")
    result = extract_features(phishing_url)
    for feature, value in result.items():
        print(f"  {feature}: {value}")

    print()

    # Test with a safe URL
    safe_url = "https://www.google.com/search"
    print("=== SAFE URL TEST ===")
    result = extract_features(safe_url)
    for feature, value in result.items():
        print(f"  {feature}: {value}")