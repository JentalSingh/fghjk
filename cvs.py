import time
import logging
from pathlib import Path
import random
# Selenium wire ka use karenge proxy ke liye
from seleniumwire import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent
TARGET_URL = "https://www.fonplata.org/en/contact-us/grievance-channel"
# PDF Name updated
PDF_NAME = "Expedia-does-Guide.pdf"
PDF_PATH = BASE_DIR / PDF_NAME
PROXY_FILE = BASE_DIR / "proxies.txt"

# --- PROXY UTILS ---
def get_proxy():
    if not PROXY_FILE.exists():
        return None
    with PROXY_FILE.open("r") as f:
        proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    if not proxies:
        return None
    
    p = random.choice(proxies).split(':')
    # Format: ip:port:user:password
    return {
        'proxy': {
            'http': f'http://{p[2]}:{p[3]}@{p[0]}:{p[1]}',
            'https': f'http://{p[2]}:{p[3]}@{p[0]}:{p[1]}',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

def main():
    options = Options()
    options.add_argument("--start-maximized")
    
    # Proxy configuration load karo
    proxy_options = get_proxy()
    
    # Driver initialization with selenium-wire
    driver = webdriver.Chrome(options=options, seleniumwire_options=proxy_options)
    
    try:
        driver.get(TARGET_URL)
        time.sleep(5)
        
        file_input = driver.find_element(By.ID, "edit-upload-upload")
        driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';", file_input)
        file_input.send_keys(str(PDF_PATH))
        
        print(f"⏳ File '{PDF_NAME}' upload ho rahi hai... 15 seconds wait.")
        time.sleep(15) 
        
        # --- DEBUGGING STEP ---
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"DEBUG: Total links found: {len(links)}")
        
        for link in links:
            href = link.get_attribute("href")
            if href and "pdf" in href.lower():
                print(f"DEBUG FOUND: URL: {href}")

        # Final extraction
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, ".pdf"))
            )
            final_url = element.get_attribute('href')
            print(f"\n🎉 SUCCESS! URL: {final_url}")
            with open("upload_result.txt", "w") as f: f.write(final_url)
        except:
            print("\n❌ .pdf extension wala link nahi mila.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()