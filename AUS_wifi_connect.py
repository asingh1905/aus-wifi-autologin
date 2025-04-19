"""
Auto Login Script for 'CAMPUS CONNECT AUS' WiFi

Features:
- Checks if you're connected to the desired SSID
- Verifies internet connectivity
- Scheduled to run automatically on connection via Windows Task Scheduler
- Prevents auto-opening of captive portal by disabling active probing

Author: Anshuman Singh
"""

import os
import re
import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


# ======================= CONFIGURATION ======================= #

wifi_link = "http://122.252.242.93/"
aus_username = os.getenv("aus_wifi_username")
aus_password = os.getenv("aus_wifi_password")
brave_path = os.getenv("BRAVE_BROWSER_PATH")
driver_path = os.getenv("CHROME_DRIVER_PATH")

# ======================= VALIDATIONS ======================= #

if not aus_username or not aus_password:
    raise ValueError("❌ AUS WiFi username or password not set in environment variables.")
if not brave_path:
    raise ValueError("❌ Brave browser path is not set in environment variables.")
if not driver_path or not os.path.exists(driver_path):
    raise ValueError(f"❌ ChromeDriver path is invalid or not found: {driver_path}")

# ======================= HELPER FUNCTIONS ======================= #

def check_SSID():
    """
    Check the currently connected WiFi SSID using 'netsh'.
    """
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8')
    match = re.search(r'SSID\s*:\s*(.+)', result)
    return match.group(1).strip() if match else None

def internet_connection(ssid):
    """
    Check if device has internet access.
    """
    print(f"🔍 Checking internet connectivity on SSID: {ssid}")
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def check_aus_server():
    """
    Check if AUS WiFi login server is reachable.
    """
    try:
        requests.get(wifi_link, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def connect():
    """
    Open Brave browser with Selenium and perform login to AUS WiFi.
    """
    print("🚀 Launching Brave browser...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = brave_path
    chrome_options.add_experimental_option("detach", True)  # Keeps browser open after script ends

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(wifi_link)
    
    print("🌐 Loaded AUS WiFi login page.")
    wait = WebDriverWait(driver, 10)

    try:
        # Navigate to login options
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/a[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/a[2]"))).click()

        # Fill credentials
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/div[1]/input[1]'))).send_keys(aus_username)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/div[1]/input[2]'))).send_keys(aus_password)

        print("🔑 Credentials entered.")

        # Submit login form
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/div[3]/input'))).click()
        print("✅ Login successful.")

    except Exception as e:
        print(f"❌ Error during login: {e}")
    finally:
        time.sleep(2)
        driver.quit()

def try_connecting_again(attempts=5):
    """
    Retry AUS server check and login if needed.
    """
    for attempt in range(1, attempts + 1):
        if check_aus_server():
            print("✅ Server reachable. Attempting login...")
            connect()
            return
        else:
            print(f"⏳ Attempt {attempt}/{attempts}: Server unreachable.")
        time.sleep(2)
    print("❌ Maximum retry attempts reached. Exiting...")

# ======================= MAIN FUNCTION ======================= #

def main():
    ssid = check_SSID()

    print("------------------------------------------------------------")
    print("🛜 AUS WiFi Auto Login Script")
    print("------------------------------------------------------------")

    if ssid == "CAMPUS CONNECT AUS":
        print(f"📶 Connected SSID: {ssid}")
        
        if internet_connection(ssid):
            print("🌍 Already connected to the internet. Exiting...")
        else:
            print("🌐 Internet not available. Checking login server...")
            if check_aus_server():
                connect()
            else:
                try_connecting_again()
    else:
        print(f"❌ Not connected to 'CAMPUS CONNECT AUS'. Detected SSID: {ssid}")
        print("🛑 Exiting script...")

    time.sleep(3)

# ======================= ENTRY POINT ======================= #

if __name__ == "__main__":
    main()