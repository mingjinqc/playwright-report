import json
import os
import allure
from playwright.sync_api import sync_playwright

@allure.feature("Salesforce Login")
@allure.story("Username Field Test")
@allure.severity(allure.severity_level.NORMAL)
def test_salesforce_username():
    repo_root = os.getcwd()
    json_path = os.path.join(repo_root, "username.json")
    report_dir = os.path.join(repo_root, "docs")
    os.makedirs(report_dir, exist_ok=True)

    username = ""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            username = json.load(f).get("username", "")
    except Exception as e:
        allure.attach(str(e), "Error reading username.json")

    step1_path = os.path.join(report_dir, "step1.png")
    step2_path = os.path.join(report_dir, "step2.png")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto("https://login.salesforce.com/")

        filled_ok = cleared_ok = False

        with allure.step("Step 1: Fill username field"):
            try:
                page.fill("#username", username)
                filled_ok = page.input_value("#username") == username
                page.screenshot(path=step1_path)
                allure.attach.file(step1_path, name="Step 1 Screenshot",
                                   attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                allure.attach(str(e), "Step 1 Error")

        with allure.step("Step 2: Clear username field"):
            try:
                page.fill("#username", "")
                cleared_ok = page.input_value("#username") == ""
                page.screenshot(path=step2_path)
                allure.attach.file(step2_path, name="Step 2 Screenshot",
                                   attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                allure.attach(str(e), "Step 2 Error")

        browser.close()

    html = f"""
    <html>
    <head>
        <style>
            table {{border-collapse:collapse;width:100%;font-family:Arial,sans-serif;}}
            th,td {{border:1px solid #ccc;padding:8px;text-align:left;}}
            th {{background:#f2f2f2;}}
            .pass {{color:green;font-weight:bold;}}
            .fail {{color:red;font-weight:bold;}}
            img {{max-width:300px;border:1px solid #999;}}
        </style>
    </head>
    <body>
    <h3>Step Results Summary</h3>
    <table>
        <tr><th>No.</th><th>Step</th><th>Result</th><th>Screenshot</th><th>Feature</th></tr>
        <tr>
          <td>1</td><td>Fill username field</td>
          <td class="{ 'pass' if filled_ok else 'fail' }">{ 'PASS' if filled_ok else 'FAIL' }</td>
          <td><img src="{os.path.basename(step1_path)}"/></td>
          <td rowspan="2">Salesforce Login</td>
        </tr>
        <tr>
          <td>2</td><td>Clear username field</td>
          <td class="{ 'pass' if cleared_ok else 'fail' }">{ 'PASS' if cleared_ok else 'FAIL' }</td>
          <td><img src="{os.path.basename(step2_path)}"/></td>
        </tr>
    </table>
    </body>
    </html>
    """
    allure.attach(html, name="Custom Step Table",
                  attachment_type=allure.attachment_type.HTML)
    assert filled_ok and cleared_ok, "One or more steps failed"
