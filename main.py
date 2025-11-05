import os
import json
import time
import allure
from playwright.sync_api import sync_playwright

@allure.feature("Salesforce Username Field Test")
def test_salesforce_username():
    # Load username from JSON
    with open("username.json") as f:
        username_data = json.load(f)
    username = username_data.get("username", "test_user")

    # Create folders
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("docs", exist_ok=True)

    result_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://login.salesforce.com")
        time.sleep(2)

        # Step 1: Fill username
        try:
            page.fill("input#username", username)
            step1 = "screenshots/step1_filled.png"
            page.screenshot(path=step1)
            allure.attach.file(step1, name="Step 1 - Filled Username", attachment_type=allure.attachment_type.PNG)
            result_data.append({"step": "Fill Username Field", "result": "Passed", "screenshot": step1})
        except Exception:
            result_data.append({"step": "Fill Username Field", "result": "Failed", "screenshot": None})

        # Step 2: Clear username
        try:
            page.fill("input#username", "")
            step2 = "screenshots/step2_cleared.png"
            page.screenshot(path=step2)
            allure.attach.file(step2, name="Step 2 - Cleared Field", attachment_type=allure.attachment_type.PNG)
            result_data.append({"step": "Clear Username Field", "result": "Passed", "screenshot": step2})
        except Exception:
            result_data.append({"step": "Clear Username Field", "result": "Failed", "screenshot": None})

        browser.close()

    # Count pass/fail
    passed = sum(1 for x in result_data if x["result"] == "Pa_
