from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

# --- Configuration ---
LOGIN_URL = "https://myrabbai.tus-e.com/login"
# UPDATE THIS: The exact URL where you add a new question after logging in
ADD_ASSET_URL = "https://myrabbai.tus-e.com/admin/add-question" 

USERNAME = "REDACTED_FOR_GITHUB" 
PASSWORD = "REDACTED_FOR_GITHUB"        

CSV_FILE = "assets.csv"
IMAGE_FOLDER = "asset_images" # The folder where the diagrams are kept

def login_to_platform(driver, wait):
    """Executes your proven login sequence."""
    print("Executing authentication sequence...")
    driver.get(LOGIN_URL)
    
    email_xpath = '//*[@id="app"]/div/div[2]/div[2]/div/div/div[2]/form/div[1]/input'
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, email_xpath))) 
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    
    email_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    submit_button.click()
    wait.until(EC.url_changes(LOGIN_URL))
    print("Authentication successful.")

def process_asset_batch():
    print("--- Initiating Bulk Asset Ingestion ---")
    
    options = webdriver.EdgeOptions()
    # options.add_argument('--headless') # Keep commented out while building/testing
    driver = webdriver.Edge(options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # 1. Log in first
        login_to_platform(driver, wait)
        
        # 2. Open the CSV file and start reading
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Loop through every single row in the spreadsheet
            for row in reader:
                print(f"Processing Asset: {row['Question_ID']}...")
                
                try:
                    # Navigate to the blank form page for each new question
                    driver.get(ADD_ASSET_URL)
                    
                    # 🛑 ACTION REQUIRED: You will need to use "Copy XPath" for these fields on the real page
                    question_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Question Text']")))
                    opt_a_box = driver.find_element(By.XPATH, "//input[@placeholder='Option A']")
                    opt_b_box = driver.find_element(By.XPATH, "//input[@placeholder='Option B']")
                    opt_c_box = driver.find_element(By.XPATH, "//input[@placeholder='Option C']")
                    opt_d_box = driver.find_element(By.XPATH, "//input[@placeholder='Option D']")
                    correct_ans_box = driver.find_element(By.XPATH, "//input[@placeholder='Correct Answer']")
                    
                    # Inject text from the CSV directly into the browser
                    question_box.send_keys(row['Question_Text'])
                    opt_a_box.send_keys(row['Option_A'])
                    opt_b_box.send_keys(row['Option_B'])
                    opt_c_box.send_keys(row['Option_C'])
                    opt_d_box.send_keys(row['Option_D'])
                    correct_ans_box.send_keys(row['Correct_Answer'])
                    
                    # --- THE IMAGE UPLOAD MAGIC ---
                    # Check if the spreadsheet has a filename in the Diagram column
                    if row['Diagram_Filename']:
                        # Build the exact path to the file on your computer
                        image_path = os.path.abspath(os.path.join(IMAGE_FOLDER, row['Diagram_Filename']))
                        
                        # Find the hidden file upload button and send the file path to it
                        upload_button = driver.find_element(By.XPATH, "//input[@type='file']")
                        upload_button.send_keys(image_path)
                        print(f" -> Attached image: {row['Diagram_Filename']}")
                    
                    # Submit the question
                    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save Question')]")
                    submit_btn.click()
                    
                    # Wait 2 seconds for the platform to process the save before looping again
                    time.sleep(2) 
                    print(f" -> {row['Question_ID']} ingested successfully.")
                    
                except Exception as e:
                    # If ONE question breaks, print an error but KEEP GOING to the next row
                    print(f" -> ERROR on {row['Question_ID']}: Skipping to next asset.")
                    continue

    finally:
        driver.quit()
        print("--- Bulk Ingestion Complete ---")

if __name__ == "__main__":
    process_asset_batch()