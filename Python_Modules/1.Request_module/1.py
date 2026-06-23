import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

# 1. Set up session with retries and proxy
session = requests.Session()

# Retry strategy
retry = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=['GET', 'POST']
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Proxy (Burp)
session.proxies.update({
    'http': 'http://127.0.0.1:8081',
    'https': 'http://127.0.0.1:8081'
})
session.verify = False  # for debugging only

# Default headers
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
})

# 2. GET login page to extract CSRF token
login_url = 'https://example.com/login'
resp = session.get(login_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

# 3. Prepare login payload
payload = {
    'csrf_token': csrf_token,
    'username': 'my_user',
    'password': 'my_pass'
}

# 4. POST login (CSRF token goes in form data)
login_post = session.post(login_url, data=payload)

# 5. Now we are logged in – session holds cookies
profile = session.get('https://example.com/dashboard')
print(profile.status_code)

# 6. Close session
session.close()