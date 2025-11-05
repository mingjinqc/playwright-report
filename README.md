# 🧪 Playwright Report Generator

This repository runs a Playwright automation whenever `username.json` is changed in the `main` branch.

---

## 🔹 What it does
1. Opens [https://login.salesforce.com](https://login.salesforce.com).
2. Fills the username field with the value from `username.json` and takes a screenshot.
3. Clears the field and takes a screenshot.
5. Generates an HTML report in the `docs/` folder.
6. Automatically publishes it to GitHub Pages 🌐.

---

## 🔹 Files
- `main.py` → Main Playwright script  
- `username.json` → Input data  
- `docs/` → Screenshots + `report.html`  
- `.github/workflows/generate-report.yml` → GitHub Actions automation

---

## 🔹 Trigger
Runs automatically when `username.json` changes in the `main` branch.

---

## 🔹 View the Report on GitHub Pages
After the first successful workflow run, view your latest report here:

```html
https://<your-username>.github.io/<your-repo-name>/report.html
```
