import re
import requests
from PIL import Image
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import sys, os

NOTEBOOK_URL = "https://colab.research.google.com/drive/12lara_NVIx1FCwcfyCgck1lt4ZQbeleJ?usp=sharing"

def fetch_ngrok_url(notebook_url=NOTEBOOK_URL, timeout=60, poll_interval=3):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    # Silence ChromeDriver logs
    service = Service(log_path=os.devnull)

    # Redirect stdout/stderr to null to silence "DevTools listening..."
    devnull = open(os.devnull, 'w')
    old_stderr, old_stdout = sys.stderr, sys.stdout
    sys.stderr = devnull
    sys.stdout = devnull

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(notebook_url)
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                iframe_container = driver.find_element(
                    By.CSS_SELECTOR,
                    "#cell-udm4VvCn_d0T > div.main-content > div > div.codecell-input-output > div.output > div.output-content > div.output-iframe-container"
                )
                iframe_html = iframe_container.get_attribute("innerHTML")
                ngrok_url_match = re.search(r'https://[a-z0-9]+\.ngrok-free\.app', iframe_html)
                if ngrok_url_match:
                    return ngrok_url_match.group(0)
            except:
                pass
            time.sleep(poll_interval)
        return None
    finally:
        driver.quit()
        sys.stderr, sys.stdout = old_stderr, old_stdout
        devnull.close()

def get_image(prompt, ngrok_url=None):
    if ngrok_url is None:
        ngrok_url = fetch_ngrok_url()
        if ngrok_url is None:
            raise RuntimeError("Ngrok URL not found")

    def fetch_image(local_prompt):
        url = f"{ngrok_url}/generate?prompt=" + "+".join(local_prompt.split())
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.content

    image_bytes = fetch_image(prompt)
    return Image.open(io.BytesIO(image_bytes))
