from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def prompt(prompt="Hello, how are you?"):
    chrome_options = Options()
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"

    # Add the User-Agent argument to the options
    chrome_options.add_argument(f'user-agent={custom_user_agent}')
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://chatgpt.com")  # Replace with actual URL

    try:
        # Wait for the contenteditable div to be visible (you can update the XPath here)
        input_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div/main/div/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/div[1]/div/div")
            )
        )

        # Click and send the prompt
        input_field.click()
        input_field.send_keys(prompt)

        # Wait for the send button and click it
        send_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div/div/main/div/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/div[3]/div/button")
            )
        )
        send_button.click()

    except Exception as e:
        print(f"Error: {e}")

    #finally:
    #    driver.quit()

# Test the function
prompt("Hello, how are you?")
