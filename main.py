import os
import json
import time
from playwright.sync_api import sync_playwright
import pytest
import allure

@allure.feature("Salesforce Username Field Test")
def test_salesforce_username():
    # Load username
    with open("username.json") as f:
        username_data = json.load(f)
    username = username_data.get("username", "test_user")

    # Create folders
    os.makedirs("docs", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)  # Allure output folder

    result_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://login.salesforce.com")
        time.sleep(2)

        # Step 1: Fill username
        try:
            page.fill("input#username", username)
            step1 = "docs/step1.png"
            page.screenshot(path=step1)
            allure.attach.file(step1, name="Step 1 - Filled Username", attachment_type=allure.attachment_type.PNG)
            result_data.append({"step": "Fill Username Field", "result": "Passed", "screenshot": step1})
        except Exception:
            result_data.append({"step": "Fill Username Field", "result": "Failed", "screenshot": None})

        # Step 2: Clear username
        try:
            page.fill("input#username", "")
            step2 = "docs/step2.png"
            page.screenshot(path=step2)
            allure.attach.file(step2, name="Step 2 - Cleared Field", attachment_type=allure.attachment_type.PNG)
            result_data.append({"step": "Clear Username Field", "result": "Passed", "screenshot": step2})
        except Exception:
            result_data.append({"step": "Clear Username Field", "result": "Failed", "screenshot": None})

        browser.close()

    # Count pass/fail
    passed = sum(1 for x in result_data if x["result"] == "Passed")
    failed = sum(1 for x in result_data if x["result"] == "Failed")

    # ✅ Static HTML report (docs/index.html)
    html_summary = f"""
    <html>
    <head>
        <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        img {{ width: 200px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h2>Salesforce Username Field Test Summary</h2>
        <table>
            <tr><th>Step</th><th>Result</th><th>Screenshot</th></tr>
    """

    for item in result_data:
        html_summary += f"""
            <tr>
                <td>{item['step']}</td>
                <td>{item['result']}</td>
                <td>{'<a href="'+item['screenshot']+'" target="_blank"><img src="'+item['screenshot'].replace("docs/", "")+'"></a>' if item['screenshot'] else 'N/A'}</td>
            </tr>
        """

    html_summary += "</table></body></html>"

    # Save static HTML report
    with open("docs/index.html", "w") as f:
        f.write(html_summary)
