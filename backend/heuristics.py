# heuristics.py
# Manual rule-based checks for phishing detection
# These are "common sense" rules written by hand (no ML involved)

def check_heuristics(url):
    """
    Input  : URL string
    Output : Dictionary with:
             - 'flags'      → list of triggered rule names
             - 'risk_score' → total penalty points (0-100)
    """

    flags = []        # list of red flags found
    risk_score = 0    # total penalty points

    url_lower = url.lower()

    # ── Rule 1: @ symbol in URL ──────────────────────────
    # Browsers ignore everything before @ — phishers abuse this
    # e.g. http://google.com@evil.com → actually goes to evil.com
    if '@' in url:
        flags.append("Contains '@' symbol (browser redirect trick)")
        risk_score += 25

    # ── Rule 2: IP address instead of domain name ────────
    import re
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    if re.search(ip_pattern, url):
        flags.append("Uses raw IP address instead of domain name")
        risk_score += 20

    # ── Rule 3: No HTTPS ──────────────────────────────────
    if not url.startswith('https'):
        flags.append("No HTTPS (connection not encrypted)")
        risk_score += 10

    # ── Rule 4: Too many hyphens ──────────────────────────
    # Real domains rarely have 2+ hyphens
    if url.count('-') >= 2:
        flags.append("Too many hyphens in URL")
        risk_score += 15

    # ── Rule 5: Too many dots ──────────────────────────────
    # e.g. paypal.secure.login.verify.com
    if url.count('.') >= 4:
        flags.append("Too many subdomains/dots")
        risk_score += 15

    # ── Rule 6: Suspicious keywords ───────────────────────
    suspicious_words = ['login', 'verify', 'secure', 'update', 'confirm', 'account', 'signin']
    found_words = [w for w in suspicious_words if w in url_lower]
    if len(found_words) >= 2:
        flags.append(f"Multiple suspicious keywords: {', '.join(found_words)}")
        risk_score += 15

    # ── Rule 7: URL is too long ────────────────────────────
    # Real, simple URLs are usually under 54 characters
    if len(url) > 75:
        flags.append("URL is unusually long")
        risk_score += 10

    # ── Rule 8: Brand name + extra words (typosquatting) ──
    # e.g. "paypal-secure", "amaz0n", "g00gle"
    brand_tricks = ['paypa1', 'amaz0n', 'g00gle', 'micros0ft', 'app1e', 'faceb00k']
    for trick in brand_tricks:
        if trick in url_lower:
            flags.append(f"Possible brand impersonation: '{trick}'")
            risk_score += 25
            break

    # ── Rule 9: Suspicious top-level domains ──────────────
    # .tk, .ml, .ga, .cf, .ru are free/cheap domains often used by phishers
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.ru', '.xyz', '.top']
    for tld in suspicious_tlds:
        if tld in url_lower:
            flags.append(f"Suspicious domain extension: '{tld}'")
            risk_score += 15
            break

    # ── Rule 10: Numbers replacing letters in domain ──────
    # e.g. "g00gle.com" has digits where letters should be
    try:
        domain = url.split('/')[2]
        if any(c.isdigit() for c in domain):
            flags.append("Domain contains digits (possible character substitution)")
            risk_score += 10
    except:
        pass

    # ── Rule 11: Multiple slashes after domain (deep paths) ─
    if url.count('/') > 5:
        flags.append("Unusually deep URL path (many slashes)")
        risk_score += 5

    # Cap risk_score at 100
    risk_score = min(risk_score, 100)

    return {
        'flags': flags,
        'risk_score': risk_score
    }


# ── TEST SECTION ──────────────────────────────────────────
if __name__ == "__main__":

    test_urls = [
        "http://paypa1-login-secure-verify.ru/account/confirm",
        "https://www.google.com/search",
        "http://192.168.1.1/bank/login",
        "https://www.amazon.com/orders",
        "http://user@evil-site.com/paypal/login",
    ]

    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"URL: {url}")
        print(f"{'='*60}")
        result = check_heuristics(url)
        print(f"Risk Score: {result['risk_score']}/100")
        if result['flags']:
            print("Flags triggered:")
            for flag in result['flags']:
                print(f"  ⚠ {flag}")
        else:
            print("No red flags found ✅")