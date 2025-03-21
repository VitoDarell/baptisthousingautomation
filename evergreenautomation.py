import os.path
import os
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

load_dotenv()


print("Starting Evergreen Automation")

# Path to where you want to save the downloaded file
download_dir = os.path.join(os.getcwd(), 'downloads')  # Downloads folder in the current directory
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Set up Chrome options to download files to the specified directory
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Optional: Run in headless mode for GitHub Actions
# chrome_options.add_argument("--disable-gpu")  # Optional for headless mode

# Set download directory
prefs = {"download.default_directory": download_dir}
chrome_options.add_experimental_option("prefs", prefs)

# Set up WebDriver with the options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open a website
    driver.get("https://eg-srvr4.evergreen-home.com/app/portal")

    primary_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "userLoginButton"))
    )

    primary_button.click()  # Click the button

    time.sleep(0.3)

    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(os.getenv("EVERGREEN_USER"))
    passsword_field = driver.find_element(By.ID, "password")
    passsword_field.send_keys(os.getenv("EVERGREEN_PASS"))
    submit = driver.find_element(By.ID, "logonButton").click()
     
    time.sleep(0.3)
    submit = driver.find_element(By.ID, "logonButton").click()

    time.sleep(0.3)
    question1 = driver.find_element(By.XPATH, "//input[@placeholder='What is the make and colour of your first car?']")
    question1.send_keys(os.getenv("EVERGREEN_QUESTION1"))
    question2 = driver.find_element(By.XPATH, "//input[@placeholder='Where was your most memorable holiday?']")
    question2.send_keys(os.getenv("EVERGREEN_QUESTION2"))
    submit = driver.find_element(By.ID, "logonButton").click()

    userList = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "accessControl"))
    )
    userList.click()

    tbody_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    

    filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "input_contentUsersfilterColumnAutoComplete"))
    )
    filter.click()
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@data-value='filter.profile.complete']"))
    )
    element.click()

    time.sleep(.3)
    csvDownload = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "exportToCSV"))
    )
    csvDownload.click()
    csvName = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "csvFilename"))
    )

    csvName.clear()
    csvName.send_keys("completedUserTemp.csv")
    time.sleep(1)
    csvDownloadButton = driver.find_element(By.ID, "exportButton").click()

    time.sleep(5)

finally:
    # Close the browser
    driver.quit()