import time
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent
TARGET_URL = "https://www.fonplata.org/en/contact-us/grievance-channel"
PDF_NAME = "nftmp-fbRMe-nftmpv9accdoreamon2.pdf"
PDF_PATH = BASE_DIR / PDF_NAME

def main():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(TARGET_URL)
        time.sleep(5)
        
        file_input = driver.find_element(By.ID, "edit-upload-upload")
        driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';", file_input)
        file_input.send_keys(str(PDF_PATH))
        
        print("⏳ File upload ho rahi hai... 15 seconds wait.")
        time.sleep(15) 
        
        # --- DEBUGGING STEP ---
        # Agar error aaye, toh hum check karenge ki screen par kya elements hain
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"DEBUG: Total links found on page: {len(links)}")
        
        # Sirf wahi links print karo jisme PDF ka koi part ho
        for link in links:
            href = link.get_attribute("href")
            text = link.text
            if href and "pdf" in href.lower():
                print(f"DEBUG FOUND: Text: {text} | URL: {href}")

        # Attempt to find via partial link text
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, ".pdf"))
            )
            print(f"\n🎉 SUCCESS! URL: {element.get_attribute('href')}")
        except:
            print("\n❌ .pdf extension wala link nahi mila.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()