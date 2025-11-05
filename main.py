import pytest
import allure
import json
import os
import time
from playwright.sync_api import sync_playwright

@allure.feature("Salesforce Username Field Test")
def test_salesforce_username():
    # Load username
    with open("username.json") as f:
        username_data = json.load(f)
    username = username_data.get("username", "test_user")

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

        # Step 2: Clear field
        try:
            page.fill("input#username", "")
            step2 = "screenshots/step2_cleared.png"
            page.screenshot(path=step2)
            allure.attach.file(step2, name="Step 2 - Cleared Field", attachment_type=allure.attachment_type.PNG)
            result_data.append({"step": "Clear Username Field", "result": "Passed", "screenshot": step2})
        except Exception:
            result_data.append({"step": "Clear Username Field", "result": "Failed", "screenshot": None})

        browser.close()

    # Create static HTML summary
    html_summary = """
    <html>
    <head><style>
    table {border-collapse: collapse; width: 100%;}
    th, td {border: 1px solid #ddd; padding: 8px;}
    th {background-color: #f2f2f2;}
    img {width: 200px;}
    </style></head><body>
    <h3>Test Summary</h3>
    <table>
        <tr><th>Step</th><th>Result</th><th>Screenshot</th></tr>
    """
    for item in result_data:
        html_summary += f"""
        <tr>
            <td>{item['step']}</td>
            <td>{item['result']}</td>
            <td>{'<img src="'+item['screenshot']+'">' if item['screenshot'] else 'N/A'}</td>
        </tr>
        """
    html_summary += "</table></body></html>"

    summary_path = "docs/report.html"
    with open(summary_path, "w") as f:
        f.write(html_summary)

    # Attach to Allure
    allure.attach.file(summary_path, name="HTML Summary", attachment_type=allure.attachment_type.HTML)
