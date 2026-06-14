# Test file — Python kaam kar raha hai ya nahi

url = "http://paypa1-login.ru/secure"

print("URL hai:", url)
print("URL ki length:", len(url))
print("HTTPS hai?", url.startswith("https"))
print("Suspicious .ru domain?", ".ru" in url)