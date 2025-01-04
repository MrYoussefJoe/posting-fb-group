import json
import time
import random
import string
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore
import os
import platform
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
# Initialize colorama
init(autoreset=True)

def clear_cmd():
    """Clear the command prompt screen."""
    try:
        # Check the operating system
        if platform.system() == "Windows":
            os.system("cls")  # Command for Windows
        else:
            os.system("clear")  # Command for Unix-based OS (Linux, macOS)
    except Exception as e:
        print(Fore.RED + f"Error clearing screen: {e}")

def logo():
    """Display the logo and information at the start of the script."""
    try:
        logo_text = """
        *******************************************
        *                                         *
        *         posting fb groups Script        *
        *                                         *
        *          Created by: youssef joe        *
        *          GitHub: github.com/MrYoussefJoe*
        *          Version: 1.0                   *
        *                                         *
        *******************************************
        """
        
        # Display the logo and information
        print(Fore.GREEN + logo_text)
        print(Fore.CYAN + "Welcome to my posting group fb!")
        print(Fore.YELLOW + "Starting the script... please wait.")
        time.sleep(1)  # Simulate some startup delay
    except Exception as e:
        print(Fore.RED + f"Error displaying logo: {e}")

def initialize_driver(driver_path: str, chrome_options: Options) -> webdriver.Chrome:
    """Initialize the Chrome WebDriver."""
    try:
        service = Service(driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(Fore.RED + f"Error initializing WebDriver: {e}")
        return None

def load_cookies(driver: webdriver.Chrome, cookies_path: str):
    """Load cookies from a JSON file into the browser."""
    try:
        if os.path.exists(cookies_path):
            with open(cookies_path, "r") as cookies_file:
                cookies = json.load(cookies_file)
                for cookie in cookies:
                    if "sameSite" in cookie:
                        cookie.pop("sameSite")
                    driver.add_cookie(cookie)
            print(Fore.GREEN + "Cookies loaded successfully.")
        else:
            print(Fore.RED + f"Cookies file {cookies_path} not found.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(Fore.RED + f"Error loading cookies: {e}")

def save_cookies(driver: webdriver.Chrome, cookies_path: str):
    """Save cookies after the process into a JSON file."""
    try:
        cookies = driver.get_cookies()
        with open(cookies_path, "w") as cookies_file:
            json.dump(cookies, cookies_file)
        print(Fore.GREEN + "Cookies saved successfully.")
    except Exception as e:
        print(Fore.RED + f"Error saving cookies: {e}")

def generate_unique_message(base_message: str) -> str:
    """Add a unique value (timestamp or random string) to avoid being flagged as spam."""
    try:
        # Add a timestamp or random string to the base message to make it unique
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        
        # Create a new message with timestamp or random string
        unique_message = f"{base_message} \n- {timestamp} - {random_string}"
        return unique_message
    except Exception as e:
        print(Fore.RED + f"Error generating unique message: {e}")
        return base_message

def read_message_from_file(file_path: str) -> str:
    """Read the message from a text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            message = file.read().strip()
        return message
    except FileNotFoundError:
        print(Fore.RED + f"Message file {file_path} not found!")
        return ""
    except Exception as e:
        print(Fore.RED + f"Error reading message from file: {e}")
        return ""

def post_message(driver: webdriver.Chrome, group_url: str, message: str):
    """Post a message in a Facebook group."""
    try:
        driver.get(group_url)
        time.sleep(5)

        # Find the write box
        post_box = driver.find_element(By.XPATH, "//span[contains(text(), 'Write something...')]")
        post_box.click()
        time.sleep(2)

        # Enter the post message
        active_box = driver.switch_to.active_element
        active_box.send_keys(message)
        time.sleep(4)

        # Find and click the post button
        post_button = driver.find_element(By.XPATH, "//div[@aria-label='Post']")
        post_button.click()

        print(Fore.GREEN + f"Posted successfully in {group_url}")
    except Exception as e:
        print(Fore.RED + f"Issue posting in {group_url}: {e}")

def read_group_urls(file_path: str) -> list:
    """Read group URLs from a text file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                group_urls = [line.strip() for line in file.readlines()]
            return group_urls
        else:
            print(Fore.RED + f"Group URL file {file_path} not found!")
            return []
    except Exception as e:
        print(Fore.RED + f"Error reading group URLs: {e}")
        return []

def main():
    delay = 120  # delay by seconds (prefer 120)
    driver_path = "./chromedriver.exe"  # Make sure the path is correct
    cookies_path = "cookies.json"  # Path for cookies in JSON format
    group_file_path = "group_urls.txt"  # Path to the file containing group URLs
    message_file_path = "post.txt"  # Path to the file containing the base message

    # Initialize chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximize window
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2  # 1: allow, 2: block
    })

    # Read the base message from the text file
    base_message = read_message_from_file(message_file_path)
    if not base_message:
        print(Fore.RED + "No message to post. Exiting...")
        return

    # Generate a unique message
    unique_message = generate_unique_message(base_message)

    # Read group URLs from the text file
    group_urls = read_group_urls(group_file_path)
    if not group_urls:
        print(Fore.RED + "No group URLs to post to. Exiting...")
        return

    # Initialize the WebDriver
    driver = initialize_driver(driver_path, chrome_options)
    if not driver:
        print(Fore.RED + "Failed to initialize WebDriver. Exiting...")
        return

    driver.get("https://www.facebook.com")
    time.sleep(2)

    # Load cookies if available
    load_cookies(driver, cookies_path)

    # Refresh the page after loading cookies
    driver.refresh()
    time.sleep(5)

    # Post the message in each group
    for group_url in group_urls:
        post_message(driver, group_url, unique_message)
        time.sleep(delay)

    # Save cookies after the process
    save_cookies(driver, cookies_path)

    # Close the browser
    driver.quit()
    print(Fore.YELLOW + "Browser closed.")

if __name__ == "__main__":
    clear_cmd()
    logo()
    main()
