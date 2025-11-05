# 🧪 Playwright Report Generator

This repository automatically runs an Allure test suite whenever `username.json` is changed in the `main` branch.

---

## 🔹 What it does
1. Launches a headless browser using **Playwright** (via Python).
2. Opens [https://login.salesforce.com](https://login.salesforce.com).
3. Reads the username value from `username.json` and fills it in.
4. Takes screenshots for each step — before and after clearing the field.
5. Generates a **Allure HTML report** (`index.html`) in the `docs/` folder.
6. Publishes the report automatically to **GitHub Pages 🌐** for easy viewing.

---

## 🔹 Files
- `main.py` → Main Playwright automation and Allure integration  
- `username.json` → Input test data (contains username)  
- `requirements.txt` → Python dependencies  
- `.github/workflows/generate-report.yml` → GitHub Actions automation  
- `docs/` → Allure HTML report (auto-generated)  

---

## 🔹 Trigger
Runs automatically when `username.json` is changed in the `main` branch.

---

## 🔹 View the Report on GitHub Pages
After the first successful workflow run, view your latest Allure report here:

```html
https://<your-username>.github.io/<your-repo-name>/
```
