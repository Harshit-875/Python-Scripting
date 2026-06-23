import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor
import time

class SmartScanner:
    def __init__(self, target, proxy=None):
        self.session = requests.Session()
        
        # 1. Retries
        retry = Retry(total=2, backoff_factor=0.5, status_forcelist=[429, 500])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # 2. Headers
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        
        # 3. Proxies
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}
        
        self.target = target.rstrip('/')
        self.timeout = (3, 5)
    
    def check_path(self, path):
        url = f"{self.target}{path}"
        try:
            start = time.time()
            resp = self.session.get(url, timeout=self.timeout)
            elapsed = time.time() - start
            
            # Interesting status codes for a hacker
            if resp.status_code in [200, 301, 302, 403, 401]:
                return f"[{resp.status_code}] {url} (Response: {len(resp.content)} bytes, Time: {elapsed:.2f}s)"
            return None
        except requests.exceptions.Timeout:
            return f"[TIMEOUT] {url}"
        except requests.exceptions.ConnectionError:
            return f"[DOWN] {url}"

    def scan_wordlist(self, wordlist_file, workers=20):
        with open(wordlist_file, 'r') as f:
            paths = [f"/{line.strip()}" for line in f if line.strip()]
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = executor.map(self.check_path, paths)
            for result in results:
                if result:
                    print(result)

# Usage
scanner = SmartScanner("https://target.com", proxy="socks5://127.0.0.1:9050")
scanner.scan_wordlist("common_directories.txt")