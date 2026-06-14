from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from email.mime.text import MIMEText
import smtplib
import time
import datetime
import csv
import os

# --- 1. MyRabbAI Platform Credentials ---
LOGIN_URL = "[https://portal.example-edtech.com/login](https://portal.example-edtech.com/login)" 
USERNAME = "REDACTED_FOR_GITHUB" 
PASSWORD = "REDACTED_FOR_GITHUB"        

# --- 2. Automated Email Alert Credentials ---
ALERT_SENDER_EMAIL = "REDACTED_FOR_GITHUB"     # The Gmail sending the alert
ALERT_SENDER_APP_PASSWORD = "REDACTED_FOR_GITHUB" # The App Password from Google
ALERT_RECEIVER_EMAIL = "REDACTED_FOR_GITHUB"   # Where you want to receive the alert (can be the same email)
LATENCY_THRESHOLD = 10.0                        # Send a warning if load time is higher than this (seconds)

# --- 3. Configuration ---
LOG_FILE = "EdTech startup.csv"

def send_email_alert(subject, body):
    """Sends a standardized email alert to the QA Engineer."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = ALERT_SENDER_EMAIL
        msg['To'] = ALERT_RECEIVER_EMAIL

        # Connect to Gmail's server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() # Secure the connection
            server.login(ALERT_SENDER_EMAIL, ALERT_SENDER_APP_PASSWORD)
            server.send_message(msg)
        print(" -> Alert email dispatched successfully.")
    except Exception as e:
        print(f" -> Failed to send email alert: {str(e)}")

def log_to_excel(status, details, load_time):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Time", "Status", "Load Time (s)", "Details"])
        now = datetime.datetime.now()
        writer.writerow([now.strftime('%Y-%m-%d'), now.strftime('%H:%M'), status, load_time, details])

def daily_login_check():
    print(f"--- EdTech startup Daily Login Check: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ---")
    
    options = webdriver.EdgeOptions()
    # options.add_argument('--headless') # Keep commented out while testing
    options.add_argument('--disable-gpu')
    driver = webdriver.Edge(options=options)
    
    try:
        print(f"Navigating to {LOGIN_URL}...")
        start_time = time.time() 
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)
        
        print("Locating login fields...")
        email_xpath = '//*[@id="app"]/div/div[2]/div[2]/div/div/div[2]/form/div[1]/input'
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, email_xpath))) 
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        print("Populating credentials...")
        email_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        submit_button.click()
        
        try:
            wait.until(EC.url_changes(LOGIN_URL))
            end_time = time.time()
            load_time = round(end_time - start_time, 2)
            
            print(f"STATUS: SUCCESS. Load Time: {load_time}s")
            log_to_excel("SUCCESS", "Platform login optimal.", load_time)
            
            # Trigger Proactive Warning if load time is too slow
            if load_time > LATENCY_THRESHOLD:
                subject = "⚠️ PROACTIVE WARNING: EdTech startup High Latency"
                body = f"The automated daily check passed, but latency is high.\n\nLoad Time: {load_time} seconds.\n\nLog this as a proactive blocker before the 9:00 AM cadence."
                send_email_alert(subject, body)
            
        except TimeoutException:
            end_time = time.time()
            load_time = round(end_time - start_time, 2)
            
            print(f"STATUS: FAILED. Load Time: {load_time}s")
            log_to_excel("FAILED", "Dashboard timed out or credentials rejected.", load_time)
            
            # Trigger Critical Alert for Failure
            subject = "🚨 CRITICAL FAILURE: EdTech startup Login Down"
            body = f"The automated daily check failed.\n\nError: Dashboard timed out or credentials rejected.\nLoad Time: {load_time} seconds.\n\nInvestigate immediately."
            send_email_alert(subject, body)
                
    except Exception as e:
        print("STATUS: CRITICAL ERROR.")
        log_to_excel("CRITICAL ERROR", str(e), "N/A")
        send_email_alert("🚨 SYSTEM CRASH: Python Automation Failed", f"The Selenium script crashed with the following error:\n\n{str(e)}")
        
    finally:
        driver.quit()
        print("--- Testing & Logging Completed ---\n")

if __name__ == "__main__":
    daily_login_check()
