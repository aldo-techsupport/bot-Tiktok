from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import random
import string
import requests
import json

# Global variable untuk track email yang sudah dicoba
_used_email_indices = []

def get_temp_email(skip_index=0):
    """Ambil email dari API tempmail"""
    global _used_email_indices
    
    try:
        # Cari index yang belum digunakan
        actual_index = skip_index
        while actual_index in _used_email_indices:
            actual_index += 1
        
        if actual_index == 0:
            print("Mengambil email dari API tempmail...")
        else:
            print(f"Mengambil email alternatif (index {actual_index})...")
        
        url = "https://tempmail.alrelshop.my.id/api.php?action=get_generated_emails"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'emails' in data and len(data['emails']) > actual_index:
                # Ambil email dengan index tertentu
                email = data['emails'][actual_index]['email_address']
                print(f"✓ Email berhasil diambil: {email}")
                
                # Tandai index ini sudah digunakan
                _used_email_indices.append(actual_index)
                
                return email
            else:
                print("⚠️ Tidak ada email tersedia di API")
                return None
        else:
            print(f"⚠️ API error: status code {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error saat mengambil email: {e}")
        return None

def save_account_to_json(email, password, username):
    """Simpan data akun ke file JSON"""
    try:
        import json
        from datetime import datetime
        
        filename = "tiktok_accounts.json"
        
        # Baca file existing jika ada
        try:
            with open(filename, 'r') as f:
                accounts = json.load(f)
        except FileNotFoundError:
            accounts = []
        
        # Tambah akun baru
        account_data = {
            "email": email,
            "password": password,
            "username": username,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        accounts.append(account_data)
        
        # Simpan ke file
        with open(filename, 'w') as f:
            json.dump(accounts, f, indent=4)
        
        print(f"✓ Data akun berhasil disimpan ke {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saat menyimpan data: {e}")
        return False

def get_otp_code(email):
    """Ambil OTP code dari API tempmail berdasarkan email"""
    try:
        print(f"Mengambil OTP untuk email: {email}")
        url = f"https://tempmail.alrelshop.my.id/api.php?action=get_latest_otp&email={email}"
        
        # Retry beberapa kali karena OTP mungkin belum sampai
        max_retries = 10
        for attempt in range(max_retries):
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'otp' in data and data['otp']:
                    otp_code = data['otp']
                    print(f"✓ OTP berhasil diambil: {otp_code}")
                    return otp_code
                else:
                    print(f"⏳ OTP belum tersedia, retry {attempt + 1}/{max_retries}...")
                    time.sleep(3)
            else:
                print(f"⚠️ API error: status code {response.status_code}")
                time.sleep(3)
        
        print("⚠️ OTP tidak ditemukan setelah beberapa retry")
        return None
    except Exception as e:
        print(f"❌ Error saat mengambil OTP: {e}")
        return None

def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@example.com"

def generate_random_password():
    """Generate password dengan kombinasi huruf, angka, dan karakter khusus"""
    # Minimal 8 karakter dengan kombinasi huruf besar, kecil, angka, dan karakter khusus
    length = random.randint(10, 14)
    
    # Karakter yang akan digunakan
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*"
    
    # Pastikan minimal ada 1 dari setiap jenis
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Isi sisanya dengan random dari semua karakter
    all_chars = lowercase + uppercase + digits + special_chars
    password += random.choices(all_chars, k=length - 4)
    
    # Shuffle agar tidak predictable
    random.shuffle(password)
    
    return ''.join(password)

def get_random_month():
    """Pilih bulan secara random"""
    months = [ 
        "Januari", "Februari", "Maret", "April", "Mei", "Juni", 
        "Juli", "Agustus", "September", "Oktober", "November", "Desember" ]
    return random.choice(months)

def get_random_day():
    """Pilih tanggal secara random (1-28 untuk aman di semua bulan)"""
    return str(random.randint(1, 28))

def get_random_year():
    """Pilih tahun secara random (di bawah 2002, untuk umur 18+)"""
    return str(random.randint(1990, 2001))

def select_day(wait, driver, day_text):
    """
    Pilih hari/tanggal dari combobox custom (TikTok style)
    """
    try:
        print("\nMembuka dropdown hari...")
        time.sleep(2)
        
        dropdowns = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='combobox'][data-e2e='select-container']"))
        )
        
        if len(dropdowns) < 2:
            raise Exception("Dropdown hari belum muncul")
        
        dropdown = dropdowns[1]
        wait.until(EC.element_to_be_clickable(dropdown))
        print("✓ Dropdown hari ditemukan")
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
        time.sleep(0.5)
        
        actions = ActionChains(driver)
        actions.move_to_element(dropdown).pause(0.5).click().perform()
        print("✓ Dropdown hari diklik")
        time.sleep(2)

        print(f"Mencari opsi hari: {day_text} ...")
        container = wait.until(
            EC.visibility_of_element_located((By.ID, "Day-options-list-container"))
        )
        print("✓ Container opsi hari muncul")
        
        day_options = container.find_elements(By.CSS_SELECTOR, "div[role='option']")
        print(f"✓ Ditemukan {len(day_options)} opsi hari")
        
        for option in day_options:
            if option.text.strip() == day_text:
                actions.move_to_element(option).pause(0.3).click().perform()
                print(f"✓ Hari '{day_text}' berhasil dipilih")
                break
        
        time.sleep(1)
        
    except TimeoutException:
        print("⚠️ Elemen hari tidak ditemukan")
    except Exception as e:
        print(f"❌ Error saat memilih hari: {e}")

def select_year(wait, driver, year_text):
    """
    Pilih tahun dari combobox custom (TikTok style)
    """
    try:
        print("\nMembuka dropdown tahun...")
        time.sleep(2)
        
        dropdowns = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='combobox'][data-e2e='select-container']"))
        )
        
        if len(dropdowns) < 3:
            raise Exception("Dropdown tahun belum muncul")
        
        dropdown = dropdowns[2]
        wait.until(EC.element_to_be_clickable(dropdown))
        print("✓ Dropdown tahun ditemukan")
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
        time.sleep(0.5)
        
        actions = ActionChains(driver)
        actions.move_to_element(dropdown).pause(0.5).click().perform()
        print("✓ Dropdown tahun diklik")
        time.sleep(2)

        print(f"Mencari opsi tahun: {year_text} ...")
        container = wait.until(
            EC.visibility_of_element_located((By.ID, "Year-options-list-container"))
        )
        print("✓ Container opsi tahun muncul")
        
        year_options = container.find_elements(By.CSS_SELECTOR, "div[role='option']")
        print(f"✓ Ditemukan {len(year_options)} opsi tahun")
        
        for option in year_options:
            if option.text.strip() == year_text:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", option)
                time.sleep(0.3)
                actions.move_to_element(option).pause(0.3).click().perform()
                print(f"✓ Tahun '{year_text}' berhasil dipilih")
                break
        
        time.sleep(1)
        
    except TimeoutException:
        print("⚠️ Elemen tahun tidak ditemukan")
    except Exception as e:
        print(f"❌ Error saat memilih tahun: {e}")

def select_month_first(wait, driver, month_text="November"):
    """
    Aksi pertama: pilih bulan dari combobox custom (TikTok style)
    Jika bulan tidak ditemukan, akan mencoba bulan lain yang tersedia
    """
    try:
        print("Menunggu halaman dimuat sepenuhnya...")
        time.sleep(3)
        
        print("Membuka dropdown bulan...")
        dropdown = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='combobox'][data-e2e='select-container']"))
        )
        print("✓ Dropdown bulan ditemukan")
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
        time.sleep(1)
        
        actions = ActionChains(driver)
        actions.move_to_element(dropdown).pause(0.5).click().perform()
        print("✓ Dropdown bulan diklik")
        time.sleep(3)

        print(f"Mencari opsi bulan: {month_text} ...")
        
        try:
            container = wait.until(
                EC.visibility_of_element_located((By.ID, "Month-options-list-container"))
            )
            print("✓ Container opsi bulan muncul")
            
            month_options = container.find_elements(By.CSS_SELECTOR, "div[role='option']")
            print(f"✓ Ditemukan {len(month_options)} opsi bulan")
            
            available_months = [opt.text.strip() for opt in month_options]
            print(f"Debug - Opsi tersedia: {available_months}")
            
            # Cari bulan yang diminta
            month_found = False
            for option in month_options:
                option_text = option.text.strip()
                if option_text == month_text:
                    actions.move_to_element(option).pause(0.3).click().perform()
                    print(f"✓ Bulan '{month_text}' berhasil dipilih")
                    month_found = True
                    break
            
            # Jika tidak ditemukan, pilih bulan pertama yang tersedia
            if not month_found and len(available_months) > 0:
                print(f"⚠️ Bulan '{month_text}' tidak ditemukan, mencoba bulan lain...")
                fallback_month = available_months[0]
                for option in month_options:
                    if option.text.strip() == fallback_month:
                        actions.move_to_element(option).pause(0.3).click().perform()
                        print(f"✓ Bulan '{fallback_month}' berhasil dipilih (fallback)")
                        month_found = True
                        break
            
            if not month_found:
                raise Exception("Tidak ada opsi bulan yang bisa dipilih")
            
        except TimeoutException:
            print("⚠️ Container tidak muncul, coba klik ulang...")
            dropdown.click()
            time.sleep(2)
            container = wait.until(
                EC.visibility_of_element_located((By.ID, "Month-options-list-container"))
            )
            month_options = container.find_elements(By.CSS_SELECTOR, "div[role='option']")
            if len(month_options) > 0:
                month_options[0].click()
                print(f"✓ Bulan '{month_options[0].text.strip()}' berhasil dipilih (retry)")
        
        time.sleep(1)
        
    except TimeoutException:
        print("⚠️ Elemen bulan tidak ditemukan — kemungkinan halaman belum menampilkan elemen tersebut.")
    except Exception as e:
        print(f"❌ Error saat memilih bulan: {e}")

def fill_demo_form():
    import os
    import subprocess
    import socket
    
    def is_port_open(port):
        """Check if port is already in use"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    # Enable logging untuk capture console dan network
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'performance': 'ALL'})
    
    # Cek apakah Chrome dengan debugging port sudah berjalan
    if not is_port_open(9222):
        print("🚀 Membuka Chrome dengan debugging port...")
        
        # Path Chrome
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        
        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if not chrome_path:
            print("❌ Chrome tidak ditemukan")
            return
        
        # Buat temp directory untuk Chrome profile
        temp_profile = os.path.join(os.environ['TEMP'], 'chrome_automation_profile')
        
        # Buka Chrome dengan debugging port, temp profile, dan langsung ke URL
        cmd = f'"{chrome_path}" --remote-debugging-port=9222 --user-data-dir="{temp_profile}" --no-first-run --no-default-browser-check "https://www.tiktok.com/signup/phone-or-email/email"'
        
        subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print(f"Chrome dibuka dengan URL TikTok")
        
        # Tunggu Chrome siap
        print("⏳ Menunggu Chrome siap...")
        for i in range(20):
            if is_port_open(9222):
                print("✓ Chrome siap!")
                time.sleep(2)
                break
            time.sleep(1)
        else:
            print("❌ Timeout menunggu Chrome")
            return
    else:
        print("✓ Chrome dengan debugging port sudah berjalan")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✓ Connected ke Chrome")
    except Exception as e:
        print(f"❌ Gagal connect: {e}")
        return

    try:
        # Hapus semua cookies dan cache
        print("🧹 Menghapus cookies dan cache...")
        driver.delete_all_cookies()
        
        # Hapus local storage dan session storage
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        print("✓ Data situs berhasil dihapus")
        
        # Buka halaman TikTok
        print("Membuka halaman TikTok...")
        driver.get("https://www.tiktok.com/signup/phone-or-email/email")
        
        wait = WebDriverWait(driver, 20)

        # ==========================================
        # 1) PILIH BULAN RANDOM (dengan delay untuk menghindari rate limit)
        # ==========================================
        print("⏳ Menunggu sebentar untuk menghindari rate limit...")
        time.sleep(random.uniform(2, 4))
        
        random_month = get_random_month()
        print(f"🎲 Bulan yang dipilih secara random: {random_month}")
        select_month_first(wait, driver, month_text=random_month)

        # ==========================================
        # 2) PILIH HARI RANDOM
        # ==========================================
        random_day = get_random_day()
        print(f"🎲 Hari yang dipilih secara random: {random_day}")
        select_day(wait, driver, day_text=random_day)

        # ==========================================
        # 3) PILIH TAHUN RANDOM
        # ==========================================
        random_year = get_random_year()
        print(f"🎲 Tahun yang dipilih secara random: {random_year}")
        select_year(wait, driver, year_text=random_year)

        # ==========================================
        # 4) ISI EMAIL
        # ==========================================
        print("\n📧 Mengisi email...")
        temp_email = get_temp_email()
        if temp_email:
            try:
                email_input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
                )
                print("✓ Field email ditemukan")
                
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", email_input)
                time.sleep(1)
                
                # Klik field
                email_input.click()
                time.sleep(0.5)
                
                # Clear field dengan berbagai cara
                email_input.clear()
                time.sleep(0.2)
                
                # Clear dengan JavaScript juga
                driver.execute_script("arguments[0].value = '';", email_input)
                time.sleep(0.2)
                
                # Select all dan delete
                email_input.send_keys(Keys.CONTROL + "a")
                time.sleep(0.1)
                email_input.send_keys(Keys.DELETE)
                time.sleep(0.3)
                
                # Ketik email karakter per karakter untuk lebih natural (dengan delay lebih lama)
                for char in temp_email:
                    email_input.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.25))  # Delay lebih lama untuk terlihat lebih human
                
                # Trigger events
                driver.execute_script("""
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
                """, email_input)
                
                print(f"✓ Email '{temp_email}' berhasil diisi")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Error saat mengisi email: {e}")
        else:
            print("⚠️ Skip mengisi email karena tidak ada email dari API")
            return

        # ==========================================
        # 5) ISI PASSWORD
        # ==========================================
        print("\n🔒 Mengisi password...")
        random_password = generate_random_password()
        print(f"🎲 Password yang di-generate: {random_password}")
        
        try:
            password_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            print("✓ Field password ditemukan")
            
            # Scroll ke atas halaman dulu untuk menghindari element intercepted
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            
            # Scroll ke elemen dengan offset
            driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'smooth'});", password_input)
            time.sleep(1)
            
            # Gunakan JavaScript untuk focus dan set value
            driver.execute_script("arguments[0].focus();", password_input)
            time.sleep(0.3)
            
            # Coba klik dengan JavaScript jika normal click gagal
            try:
                password_input.click()
            except:
                driver.execute_script("arguments[0].click();", password_input)
            
            time.sleep(0.5)
            
            # Clear field dengan berbagai cara
            password_input.clear()
            time.sleep(0.2)
            
            # Clear dengan JavaScript
            driver.execute_script("arguments[0].value = '';", password_input)
            time.sleep(0.2)
            
            # Select all dan delete
            password_input.send_keys(Keys.CONTROL + "a")
            time.sleep(0.1)
            password_input.send_keys(Keys.DELETE)
            time.sleep(0.3)
            
            # Ketik password karakter per karakter (dengan delay lebih lama)
            for char in random_password:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.25))  # Delay lebih lama untuk terlihat lebih human
            
            # Trigger events
            driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """, password_input)
            
            print(f"✓ Password berhasil diisi")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error saat mengisi password: {e}")
            # Fallback: gunakan JavaScript untuk set value langsung
            try:
                print("Mencoba fallback dengan JavaScript...")
                driver.execute_script(f"arguments[0].value = '{random_password}';", password_input)
                driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", password_input)
                print(f"✓ Password berhasil diisi (fallback)")
            except Exception as e2:
                print(f"❌ Fallback juga gagal: {e2}")

        # ==========================================
        # 6) KLIK SEND CODE
        # ==========================================
        if temp_email:
            print("\n📤 Klik tombol Send Code...")
            try:
                # Tunggu tombol menjadi enabled (tidak disabled)
                send_code_button = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-e2e='send-code-button']"))
                )
                
                # Tunggu sampai button tidak disabled
                print("Menunggu tombol Send Code menjadi aktif...")
                for i in range(20):
                    if not send_code_button.get_attribute("disabled"):
                        print("✓ Tombol Send Code sudah aktif")
                        break
                    time.sleep(0.5)
                else:
                    print("⚠️ Tombol masih disabled, coba klik paksa...")
                
                # Scroll ke tombol
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", send_code_button)
                time.sleep(0.5)
                
                # Klik tombol
                try:
                    send_code_button.click()
                except:
                    driver.execute_script("arguments[0].click();", send_code_button)
                
                print("✓ Tombol Send Code berhasil diklik")
                time.sleep(3)
                
                # Cek apakah ada CAPTCHA
                print("🔍 Mengecek CAPTCHA...")
                try:
                    captcha_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Pilih') and contains(text(), 'objek')]")
                    if len(captcha_elements) > 0:
                        print("🤖 CAPTCHA terdeteksi!")
                        print("⚠️ CAPTCHA perlu diselesaikan manual")
                        print("⏳ Menunggu 30 detik untuk Anda selesaikan CAPTCHA...")
                        time.sleep(30)
                except:
                    pass
                
                print("✓ Lanjut ke OTP")
                
                # ==========================================
                # 7) AMBIL OTP DAN ISI
                # ==========================================
                print("\n🔢 Mengambil OTP code...")
                otp_code = get_otp_code(temp_email)
                
                if otp_code:
                    print(f"✓ OTP diterima: {otp_code}")
                    
                    # Isi OTP ke field
                    otp_input = None
                    print("Menunggu field OTP muncul...")
                    time.sleep(3)  # Tunggu field OTP muncul setelah klik send code
                    
                    try:
                        # Coba beberapa selector
                        selectors = [
                            "input[placeholder*='kode 6 digit']",
                            "input[placeholder*='Masukkan kode']",
                            "input[placeholder*='digit']",
                            "input.tiktok-14kebau-InputContainer"
                        ]
                        
                        for selector in selectors:
                            try:
                                otp_input = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                )
                                print(f"✓ Field OTP ditemukan dengan selector: {selector}")
                                break
                            except:
                                continue
                        
                        if not otp_input:
                            raise Exception("Field OTP tidak ditemukan dengan semua selector")
                        
                        # Scroll ke field OTP
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", otp_input)
                        time.sleep(0.5)
                        
                        # Focus dan isi OTP
                        driver.execute_script("arguments[0].focus();", otp_input)
                        time.sleep(0.3)
                        
                        try:
                            otp_input.click()
                        except:
                            driver.execute_script("arguments[0].click();", otp_input)
                        
                        time.sleep(0.3)
                        otp_input.clear()
                        
                        # Ketik OTP karakter per karakter
                        for char in otp_code:
                            otp_input.send_keys(char)
                            time.sleep(random.uniform(0.1, 0.2))
                        
                        print(f"✓ OTP '{otp_code}' berhasil diisi")
                        time.sleep(2)
                        
                        # ==========================================
                        # 8) KLIK TOMBOL BERIKUTNYA
                        # ==========================================
                        print("\n✅ Klik tombol Berikutnya...")
                        try:
                            submit_button = wait.until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                            )
                            
                            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_button)
                            time.sleep(0.5)
                            
                            try:
                                submit_button.click()
                            except:
                                driver.execute_script("arguments[0].click();", submit_button)
                            
                            print("✓ Tombol Berikutnya berhasil diklik")
                            time.sleep(3)
                            
                            # ==========================================
                            # 9) ISI USERNAME
                            # ==========================================
                            print("\n👤 Mengisi username...")
                            
                            # Generate username dari email
                            username_from_email = temp_email.split('@')[0]
                            
                            # Coba isi username
                            max_attempts = 5
                            for attempt in range(max_attempts):
                                try:
                                    # Cari field username
                                    username_input = wait.until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='nama pengguna' i], input[placeholder*='username' i]"))
                                    )
                                    
                                    # Generate username
                                    if attempt == 0:
                                        username = username_from_email
                                    else:
                                        # Generate random username
                                        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 12)))
                                    
                                    print(f"Mencoba username: {username}")
                                    
                                    # Scroll dan focus
                                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", username_input)
                                    time.sleep(0.5)
                                    
                                    username_input.click()
                                    time.sleep(0.3)
                                    
                                    # Clear dan isi username
                                    username_input.clear()
                                    time.sleep(0.3)
                                    
                                    for char in username:
                                        username_input.send_keys(char)
                                        time.sleep(random.uniform(0.05, 0.15))
                                    
                                    # Trigger events
                                    driver.execute_script("""
                                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                                        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
                                    """, username_input)
                                    
                                    print(f"✓ Username '{username}' berhasil diisi")
                                    time.sleep(2)
                                    
                                    # Cek apakah tombol Daftar sudah enabled
                                    register_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                                    is_disabled = register_button.get_attribute("disabled")
                                    
                                    if not is_disabled:
                                        print("✓ Username valid, tombol Daftar sudah aktif")
                                        break
                                    else:
                                        print(f"⚠️ Username tidak valid (attempt {attempt + 1}/{max_attempts}), coba lagi...")
                                        time.sleep(1)
                                        
                                except Exception as e:
                                    print(f"❌ Error saat mengisi username: {e}")
                                    if attempt < max_attempts - 1:
                                        time.sleep(1)
                                        continue
                                    else:
                                        break
                            
                            # ==========================================
                            # 10) KLIK TOMBOL DAFTAR
                            # ==========================================
                            print("\n📝 Klik tombol Daftar...")
                            try:
                                # Tunggu tombol menjadi enabled
                                for i in range(10):
                                    register_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                                    if not register_button.get_attribute("disabled"):
                                        print("✓ Tombol Daftar sudah aktif")
                                        break
                                    time.sleep(0.5)
                                
                                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", register_button)
                                time.sleep(0.5)
                                
                                try:
                                    register_button.click()
                                except:
                                    driver.execute_script("arguments[0].click();", register_button)
                                
                                print("✓ Tombol Daftar berhasil diklik")
                                print("\n🎉 Registrasi selesai!")
                                time.sleep(3)
                                
                                # Simpan data akun ke JSON
                                print("\n💾 Menyimpan data akun...")
                                save_account_to_json(temp_email, random_password, username)
                                
                                time.sleep(2)
                                
                            except Exception as e:
                                print(f"❌ Error saat klik tombol Daftar: {e}")
                            
                        except Exception as e:
                            print(f"❌ Error saat klik tombol Berikutnya: {e}")
                        
                    except Exception as e:
                        print(f"❌ Error saat mengisi OTP: {e}")
                        # Fallback dengan JavaScript
                        if otp_input:
                            try:
                                print("Mencoba fallback dengan JavaScript...")
                                driver.execute_script(f"arguments[0].value = '{otp_code}';", otp_input)
                                driver.execute_script("arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }}));", otp_input)
                                print(f"✓ OTP berhasil diisi (fallback)")
                            except Exception as e2:
                                print(f"❌ Fallback juga gagal: {e2}")
                        else:
                            print("❌ Field OTP tidak ditemukan, skip fallback")
                else:
                    print("⚠️ Tidak bisa mendapatkan OTP")
                    
            except Exception as e:
                print(f"❌ Error saat klik Send Code: {e}")

        print("\n✅ Proses selesai!\n")
        
        # Tunggu sebentar agar bisa melihat hasilnya
        print("Menunggu 5 detik sebelum cleanup...")
        time.sleep(5)

    finally:
        try:
            # Hapus data situs sebelum close
            print("\n🧹 Membersihkan data situs...")
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            print("✓ Data situs berhasil dihapus")
            time.sleep(1)
        except:
            pass
        
        print("\n🔒 Menutup browser...")
        try:
            driver.quit()
        except:
            pass
        
        # Paksa kill Chrome process jika masih ada
        try:
            import subprocess
            subprocess.run("taskkill /F /IM chrome.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✓ Browser berhasil ditutup")
        except:
            pass

if __name__ == "__main__":
    print("=" * 60)
    print("Automated Form + Custom Month Selector")
    print("=" * 60)
    fill_demo_form()
