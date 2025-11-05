import json
import os
import time
import allure
from playwright.sync_api import sync_playwright

@allure.feature("Salesforce Username Field Test")
def test_salesforce_username():
    # Load username from JSON
    with open("username.json") as f:
        username_data = json.load(f)
    username = username_data.get("username", "test_user")

    # Create docs folder
    os.makedirs("docs", exist_ok=True)

    result_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://login.salesforce.com")
        time.sleep(2)

        # Step 1: Fill username
        with allure.step("Step 1: Fill username field"):
            try:
                page.fill("input#username", username)
                step1 = "docs/step1.png"
                page.screenshot(path=step1)
                allure.attach.file(step1, name="Step 1 Screenshot", attachment_type=allure.attachment_type.PNG)
                result_data.append({"step": "Fill Username Field", "result": "Passed", "screenshot": step1})
            except Exception:
                result_data.append({"step": "Fill Username Field", "result": "Failed", "screenshot": None})

        # Step 2: Clear username
        with allure.step("Step 2: Clear username field"):
            try:
                page.fill("input#username", "")
                step2 = "docs/step2.png"
                page.screenshot(path=step2)
                allure.attach.file(step2, name="Step 2 Screenshot", attachment_type=allure.attachment_type.PNG)
                result_data.append({"step": "Clear Username Field", "result": "Passed", "screenshot": step2})
            except Exception:
                result_data.append({"step": "Clear Username Field", "result": "Failed", "screenshot": None})

        browser.close()

    # Count pass/fail
    passed = sum(1 for x in result_data if x["result"] == "Passed")
    failed = sum(1 for x in result_data if x["result"] == "Failed")

    # Generate HTML summary
    html_summary = f"""
    <html>
    <head>
    <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background-color: #f2f2f2; }}
    img {{ width: 200px; cursor: pointer; }}
    #chartContainer {{ width: 300px; height: 300px; margin: auto; }}
    </style>
    </head>
    <body>
    <h2>Salesforce Username Field Test Summary</h2>
    <div id="chartContainer">
        <canvas id="resultChart" width="300" height="300"></canvas>
    </div>
    <script>
    const ctx = document.getElementById('resultChart').getContext('2d');
    const passed = {passed};
    const failed = {failed};
    const total = passed + failed;
    const passPct = ((passed / total) * 100).toFixed(1);
    const failPct = ((failed / total) * 100).toFixed(1);
    const data = {{
        labels: [`Passed: ${{passed}} (${{passPct}}%)`, `Failed: ${{failed}} (${{failPct}}%)`],
        datasets: [{{
            data: [passed, failed],
            backgroundColor: ['#4CAF50', '#F44336']
        }}]
    }};
    const Chart = function(ctx, config) {{
        const canvas = ctx.canvas;
        const values = config.data.datasets[0].data;
        const colors = config.data.datasets[0].backgroundColor;
        const total = values.reduce((a,b) => a+b, 0);
        const cx = canvas.width/2, cy = canvas.height/2, r = Math.min(cx, cy) - 10;
        let start = 0;
        for (let i=0;i<values.length;i++) {{
            const val = values[i]/total;
            const end = start + val * 2 * Math.PI;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.arc(cx, cy, r, start, end);
            ctx.closePath();
            ctx.fillStyle = colors[i];
            ctx.fill();
            start = end;
        }}
    }};
    Chart(ctx, data);
    </script>
    <table>
        <tr><th>Step</th><th>Result</th><th>Screenshot</th></tr>
    """

    for item in result_data:
        html_summary += f"""
        <tr>
            <td>{item['step']}</td>
            <td>{item['result']}</td>
            <td>
                {'<a href="'+item['screenshot']+'" target="_blank"><img src="'+item['screenshot'].replace("docs/", "")+'"></a>' if item['screenshot'] else 'N/A'}
            </td>
        </tr>
        """

    html_summary += "</table></body></html>"

    # Save static HTML report
    report_path = "docs/report.html"
    with open(report_path, "w") as f:
        f.write(html_summary)

    # Save Allure HTML report
    allure_path = "docs/index.html"
    with open(allure_path, "w") as f:
        f.write(html_summary)

    # Attach Allure HTML report inside a step
    with allure.step("Attach Allure HTML Summary"):
        with open(allure_path, "r") as f:
            allure.attach(f.read(), name="Allure HTML Summary", attachment_type=allure.attachment_type.HTML)
