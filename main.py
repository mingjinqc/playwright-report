import json
import os
import time
import allure
from playwright.sync_api import sync_playwright

@allure.step("Attach HTML summary table to Allure report")
def attach_html_summary(result_data):
    table_rows = ""
    for row in result_data:
        color = "green" if row["result"] == "Passed" else "red"
        table_rows += f"<tr><td>{row['step']}</td><td style='color:{color}'>{row['result']}</td><td><img src='{row['screenshot']}' width='200'></td></tr>"
    html = f"""
    <html><body>
    <h3>Execution Summary</h3>
    <table border='1' cellpadding='6'>
      <tr><th>Step</th><th>Result</th><th>Screenshot</th></tr>
      {table_rows}
    </table>
    </body></html>
    """
    allure.attach(html, name="Summary Table", attachment_type=allure.attachment_type.HTML)

def generate_static_report(result_data):
    os.makedirs("docs", exist_ok=True)
    table_rows = ""
    for i, row in enumerate(result_data, 1):
        color = "green" if row["result"] == "Passed" else "red"
        table_rows += f"<tr><td>{i}</td><td>{row['step']}</td><td style='color:{color}'>{row['result']}</td><td><img src='{row['screenshot']}' width='200'></td></tr>"
    html = f"""
    <html><body>
    <h2>Static HTML Summary</h2>
    <table border='1' cellpadding='6'>
      <tr><th>No.</th><th>Step</th><th>Result</th><th>Screenshot</th></tr>
      {table_rows}
    </table>
    </body></html>
    """
    with open("docs/report.html", "w") as f:
        f.write(html)

@allure.feature("Salesforce Username Field Test")
def test_salesforce_username():
    with open("username.json") as f:
        username_data = json.load(f)
    username = username_data.get("username", "test_user")

    os.makedirs("screenshots", exist_ok=True)
    result_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://login.salesforce.com")
        time.sleep(2)

        try:
            page.fill("input#username", username)
            step1 = "screenshots/step1_filled.png"
            page.screenshot(path=step1)
            allure.attach.file(step1, name="Step 1 - Filled Username", attachment_type=allure.attachment_type.PNG)
            result_data.append({"step": "Fill Username Field", "result": "Passed", "screenshot": step1})
        except Exception:
            result_data.append({"step": "Fill Username Field", "result": "Failed", "screenshot": step1})

        try:
            page.fill("input#username", "")
            step2 = "screenshots/step2_cleared.png"
            page.screenshot(path=step2)
            allure.attach.file(step2, name="Step 2 - Cleared Field", attachment_type=allure.attachment_type.PNG)
            result_data.append({"step": "Clear Username Field", "result": "Passed", "screenshot": step2})
        except Exception:
            result_data.append({"step": "Clear Username Field", "result": "Failed", "screenshot": step2})

        browser.close()

    attach_html_summary(result_data)
    generate_static_report(result_data)
