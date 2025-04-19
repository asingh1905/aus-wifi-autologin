
# AUS WiFi AutoLogin 🚀

A Python automation script that logs you into **Assam University Silchar's** "CAMPUS CONNECT AUS" WiFi network using Selenium and the Brave browser. The script is automatically triggered on WiFi connection via Windows Task Scheduler.

---

## 📖 **Table of Contents**
1. [Features](#features)
2. [Setup Instructions](#setup-instructions)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Disabling Captive Portal Detection](#disabling-captive-portal-detection)
6. [License](#license)

---

## 🚀 **Features**
- Automatically logs into the "CAMPUS CONNECT AUS" WiFi network.
- Uses **Selenium** with **Brave browser** to automate the login process.
- Automatically triggered using **Windows Task Scheduler** when connected to the WiFi network.
- Script can be customized for similar WiFi networks with minor tweaks.

---

## 🛠️ **Setup Instructions**

1. **Install Python dependencies**:
   You'll need to install the required Python libraries.
   ```bash
   pip install -r requirements.txt
   ```

2. **Download ChromeDriver**:
   Download the compatible version of ChromeDriver from [here](https://googlechromelabs.github.io/chrome-for-testing/). Make sure it matches the version of your Brave browser.

3. **Set up Environment Variables**:
   Create environment variables for the following:
   - `aus_wifi_username`: Your **AUS WiFi username**.
   - `aus_wifi_password`: Your **AUS WiFi password**.
   - `BRAVE_BROWSER_PATH`: Full path to the **Brave browser** (e.g., `C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe`).
   - `CHROME_DRIVER_PATH`: Path to your **ChromeDriver** executable.

4. **Install Dependencies**:
   You can either install them manually or create a `requirements.txt` file with the following contents:
   ```txt
   selenium==4.15.2
   requests==2.31.0
   ```

5. **(Optional) Disable Captive Portal Detection**:
   Run this in an elevated terminal (Admin) to disable the captive portal detection that auto-opens the login page:
   ```bash
   reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet" /v EnableActiveProbing /t REG_DWORD /d 0 /f
   ```

---

## ⚙️ **Usage**

Once the setup is complete, you can run the script using the following command:

```bash
python aus_wifi_autologin.py
```

Alternatively, you can schedule this script using **Windows Task Scheduler** to run automatically when you connect to the "CAMPUS CONNECT AUS" WiFi network. 

### To schedule the script:

1. **Create Task**:
   In Windows Task Scheduler, create a new task that triggers when your WiFi connects to the "CAMPUS CONNECT AUS" network.

2. **Use this XML for the Trigger**:
   ```xml
   <QueryList>
     <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
       <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
         *[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig'] and (EventID=8001)]]
         and *[EventData[Data[@Name='SSID']='CAMPUS CONNECT AUS']]
       </Select>
     </Query>
   </QueryList>
   ```

3. **Action**: In the "Action" tab, set it to **Start a program** and point to your `python.exe` with the path to the script as an argument.

---

## 🔧 **Configuration**

You can customize the following values in the script for different networks:

- **WiFi URL**: `wifi_link` (set to your network’s login page URL).
- **XPath values**: Adjust the XPath values in the Selenium section to match the login page elements.

---

## ⚡ **Disabling Captive Portal Detection**

To prevent Windows from auto-opening the captive portal (login page), you can disable the network probing. Run this command in an elevated (Admin) Command Prompt:

```bash
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet" /v EnableActiveProbing /t REG_DWORD /d 0 /f
```

To **enable** it again, use:

```bash
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet" /v EnableActiveProbing /t REG_DWORD /d 1 /f
```

---

## 📝 **License**

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

### 🏷️ **Keywords**

`#Python #WiFiAutomation #Selenium #Brave #AUSWiFi #WiFiLogin #Automation #AssamUniversitySilchar`
