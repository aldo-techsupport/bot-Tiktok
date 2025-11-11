# Web Browser Automation Script

Script Python untuk belajar web automation menggunakan Selenium dengan contoh-contoh praktis.

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download ChromeDriver yang sesuai dengan versi Chrome Anda:
   - Otomatis: Script akan menggunakan webdriver-manager
   - Manual: Download dari https://chromedriver.chromium.org/

## File-file yang Tersedia

### 1. `open_browser.py`
Script dasar untuk membuka halaman web.
```bash
python open_browser.py
```

### 2. `demo_form_filler.py` ⭐ RECOMMENDED
Contoh lengkap mengisi form secara otomatis menggunakan website demo yang legal.
```bash
python demo_form_filler.py
```

Fitur:
- Mengisi berbagai jenis input (text, email, phone, dll)
- Select dropdown
- Radio button dan checkbox
- Submit form
- Generate data random (email, password)

### 3. `advanced_form_techniques.py`
Kumpulan teknik-teknik advanced untuk form automation:
- Typing dengan delay (human-like)
- Date picker handling
- Scroll dan hover
- Wait strategies
- Generate random dates

```bash
python advanced_form_techniques.py
```

### 4. `form_automation_example.py`
Template dan contoh kode untuk berbagai skenario form filling.

## Contoh Penggunaan

### Mengisi Form Otomatis
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://demo-website.com")

# Isi text field
email_field = driver.find_element(By.ID, "email")
email_field.send_keys("test@example.com")

# Klik button
submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_btn.click()

driver.quit()
```

## Website Demo untuk Latihan

Gunakan website-website ini untuk belajar (legal & aman):
- https://demo.seleniumeasy.com/
- https://the-internet.herokuapp.com/
- https://practicetestautomation.com/
- https://testautomationpractice.blogspot.com/

## ⚠️ Panduan Etika

**PENTING:** Baca `ETHICAL_GUIDELINES.md` sebelum menggunakan automation!

✅ Boleh:
- Testing aplikasi Anda sendiri
- Automation di sistem internal
- Latihan di website demo

❌ Jangan:
- Automation di platform seperti TikTok, Instagram, Facebook
- Bypass CAPTCHA atau security measures
- Mass account creation
- Melanggar Terms of Service

## Troubleshooting

**ChromeDriver error:**
```bash
pip install webdriver-manager
```

**Element not found:**
- Tambahkan wait time
- Periksa selector (ID, class, XPath)
- Pastikan element sudah loaded

**Headless mode:**
Uncomment baris ini untuk run tanpa GUI:
```python
chrome_options.add_argument('--headless')
```

## Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Selenium Easy Tutorials](https://demo.seleniumeasy.com/)
- [Web Automation Best Practices](https://www.selenium.dev/documentation/)
