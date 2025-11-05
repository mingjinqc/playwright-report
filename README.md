# 🎭 Playwright-Report

Automated browser test using **Python + Playwright + Allure**  that fills and clears the Salesforce login field —  complete with screenshots, results table, and a HTML report. ✨

---

## 🚀 How it works
1. On every commit to `main`, GitHub Actions runs the Playwright test.  
2. Results are converted to an **Allure HTML report**.  
3. The generated `index.html` is pushed to `/docs`,  
   making it viewable via **GitHub Pages** automatically.

---

## 🌐 View the report
After your first successful run, open:

```html
https://<your-username>.github.io/playwright-report/index.html
```
