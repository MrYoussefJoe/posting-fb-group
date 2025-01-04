# Facebook Group Posting Script

*******************************************
*         Script Name: Posting FB Groups  *
*         Created by: Youssef Joe         *
*         GitHub: github.com/MrYoussefJoe *
*         Version: 1.0                    *
*******************************************

## Facebook Group Posting Script

This Python script automates the process of posting messages to Facebook groups using **Selenium WebDriver**. It's designed to help you post predefined messages to multiple Facebook groups at once, saving time and effort, especially if you're managing or marketing across several groups.

## Features
- **Automated Posting**: Automatically posts messages to specified Facebook groups.
- **Cookie Management**: Saves and loads cookies to maintain your logged-in session between script runs.
- **Customizable Messages**: Allows adding dynamic timestamps and random strings to messages to avoid being flagged as spam.
- **Error Handling**: Graceful error handling for common issues like cookies not loading or element not found.
- **Delay Between Posts**: Configurable delay between posts to avoid triggering Facebook's spam detection algorithms.

## Requirements
- Python 3.x
- Selenium
- TensorFlow (for suppressing log messages)

Before running the script, make sure to install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
