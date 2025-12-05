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

# Firefox / GeckoDriver imports (Selenium 4 style)
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


# ======================= CONFIGURATION ======================= #

# Captive portal URL
wifi_link = "http://122.252.242.93/"

# Credentials from environment variables
aus_username = os.getenv("aus_wifi_username")
aus_password = os.getenv("aus_wifi_password")

# Firefox binary path (optional if Firefox is installed in default location)
# Example: C:\Program Files\Mozilla Firefox\firefox.exe
firefox_path = os.getenv("FIREFOX_BROWSER_PATH")

# GeckoDriver path (NOT ChromeDriver anymore)
# Example: C:\Tools\geckodriver.exe
gecko_driver_path = os.getenv("GECKO_DRIVER_PATH")


# ======================= VALIDATIONS ======================= #

if not aus_username or not aus_password:
    raise ValueError("❌ AUS WiFi username or password not set in environment variables.")

# firefox_path can be optional if Firefox is in a standard location,
# but keeping this strict ensures the correct installation is used.
if not firefox_path:
    raise ValueError("❌ Firefox browser path is not set in environment variables.")

# Ensure GeckoDriver exists at the given path
if not gecko_driver_path or not os.path.exists(gecko_driver_path):
    raise ValueError(f"❌ GeckoDriver path is invalid or not found: {gecko_driver_path}")


# ======================= HELPER FUNCTIONS ======================= #

def check_SSID():
    """
    Check the currently connected WiFi SSID using 'netsh'.
    """
    result = subprocess.check_output(
        ["netsh", "wlan", "show", "interfaces"]
    ).decode("utf-8")
    match = re.search(r"SSID\s*:\s*(.+)", result)
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
    Open Firefox browser with Selenium and perform login to AUS WiFi.
    Uses GeckoDriver and Firefox options instead of Chrome/Brave.
    """
    print("🚀 Launching Firefox browser...")

    # Configure Firefox options
    firefox_options = Options()

    # Set the Firefox binary path if provided
    if firefox_path:
        firefox_options.binary_location = firefox_path

    # Uncomment this if you want headless (no window)
    # firefox_options.add_argument("--headless")

    # Create the Firefox driver service with GeckoDriver
    service = Service(gecko_driver_path)

    # Launch Firefox WebDriver
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # Navigate to the captive portal
    driver.get(wifi_link)

    print("🌐 Loaded AUS WiFi login page.")
    wait = WebDriverWait(driver, 10)

    try:
        # Navigate to login options (keep your existing XPaths)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/a[1]"))
        ).click()
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/a[2]"))
        ).click()

        # Fill credentials
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/div[1]/input[1]'))
        ).send_keys(aus_username)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/div[1]/input[2]'))
        ).send_keys(aus_password)

        print("🔑 Credentials entered.")

        # Submit login form
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/div[3]/input'))
        ).click()
        print("✅ Login successful.")

        # Optional: keep the browser open for debugging
        # time.sleep(5)

    except Exception as e:
        print(f"❌ Error during login: {e}")
    finally:
        # Close browser after short delay to avoid leaving stray processes
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
