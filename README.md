# 🧪 Playwright Allure Report Generator

This repository runs automated Playwright browser tests and generates **two reports** whenever `username.json` is updated on the `main` branch.

---

## 🔹 What it does
1. Opens [https://login.salesforce.com](https://login.salesforce.com).
2. Fills the username from `username.json` and takes a screenshot.
3. Clears the field and takes another screenshot.
4. Generates **two reports**:
   - 📊 `docs/index.html` → Allure interactive report  
   - 📋 `docs/report.html` → Static HTML summary table
5. Publishes both automatically to **GitHub Pages 🌐**.

---

## 🔹 Files
- `main.py` → Playwright test + report logic  
- `username.json` → Test input data  
- `.github/workflows/generate-report.yml` → Automation  
- `docs/` → Allure report (`index.html`) + static report (`report.html`)

---

## 🔹 Trigger
Runs automatically when either `main.py` or `username.json` changes in the `main` branch.

---

## 🔹 View the Reports on GitHub Pages
After the first successful run:

```html
https://<your-username>.github.io/<your-repo-name>/index.html
https://<your-username>.github.io/<your-repo-name>/report.html
