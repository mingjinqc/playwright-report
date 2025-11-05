# 🧪 Playwright Allure & Static Report Generator

This repository automatically runs a Playwright + Allure test suite whenever `username.json` is changed in the `main` branch.

---

## 🔹 What it does
1. Launches a headless Chromium browser using **Playwright (Python)**.  
2. Opens [https://login.salesforce.com](https://login.salesforce.com).  
3. Reads the username from `username.json` and fills it in.  
4. Takes screenshots before and after clearing the field.  
5. Generates **two reports** in the `docs/` folder:
   - 📊 `index.html` — interactive **Allure report** (with screenshots and charts).  
   - 📘 `report.html` — simple static summary table for quick viewing.  
6. Publishes automatically to **GitHub Pages 🌐**.

---

## 🔹 Folder Overview
| File | Description |
|------|--------------|
| `main.py` | Playwright automation and Allure logic |
| `username.json` | Input test data |
| `requirements.txt` | Python dependencies |
| `.github/workflows/generate-report.yml` | GitHub Actions automation |
| `docs/` | Allure report (`index.html`) + static summary (`report.html`) |

---

## 🔹 Trigger
Runs automatically whenever `username.json` is modified in the `main` branch.

---

## 🔹 View the Reports on GitHub Pages
After the first successful workflow run, view your reports here:
```html
https://<your-username>.github.io/<your-repo-name>/
```

