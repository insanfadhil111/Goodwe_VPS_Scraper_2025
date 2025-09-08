from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import requests
import random
from datetime import datetime

# --- Konfigurasi Firefox ---
options = Options()
options.binary_location = "/opt/firefox/firefox"   # Lokasi Firefox manual
options.add_argument("--headless")                 # Headless stabil
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/local/bin/geckodriver")    # Lokasi geckodriver manual

# --- Start WebDriver ---
driver = webdriver.Firefox(service=service, options=options)

# Fungsi untuk membersihkan dan mengonversi data
def clean_data(value, is_integer=False):
    try:
        # Menghapus satuan dan karakter non-numerik
        cleaned_value = ''.join(filter(lambda x: x.isdigit() or x == '.', value))
        
        # Mengonversi ke float
        numeric_value = float(cleaned_value)
        
        # Jika satuan kWh atau kW terdeteksi, kalikan 1000 untuk mengonversinya ke Wh atau W
        if 'kWh' in value or 'kW' in value:
            numeric_value *= 1000
        
        # Mengembalikan nilai sebagai integer jika diminta
        if is_integer:
            return int(numeric_value)
        return numeric_value
    except ValueError:
        return 0.0 if not is_integer else 0

# Fungsi untuk mengupload data ke API
def upload_data(pv_generation_today, income_today, total_generation, total_income, power_value):
    url = "http://iotlab-uns.com/smart-enms/api/add-gwdata"
    data = {
        "P": clean_data(power_value),  # Bersihkan dan konversi data daya
        "today_generation": clean_data(pv_generation_today),  # Bersihkan dan konversi data
        "total_generation": clean_data(total_generation),  # Bersihkan dan konversi data
        "today_income": clean_data(income_today, is_integer=True),  # Bersihkan dan konversi data
        "total_income": clean_data(total_income, is_integer=True)  # Bersihkan dan konversi data
    }
    print(f"Data yang dikirim: {data}")  # Tambahkan ini untuk debugging
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Akan menghasilkan exception jika status code bukan 2xx
        print(f"Data berhasil dikirim ke API: {response.json()}")
    except requests.RequestException as e:
        print(f"Terjadi kesalahan saat mengirim data ke API: {e}")
        print(f"Respons dari server: {response.text}")  # Tambahkan ini untuk debugging

def login():
    driver.get("https://www.semsportal.com/home/login")

    # Tunggu sampai form login muncul
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    # Isi username & password
    driver.find_element(By.ID, "username").send_keys("elektro@ft.uns.ac.id")
    pwd = driver.find_element(By.ID, "password")
    pwd.clear()
    pwd.send_keys("Solar2019")

    # Centang checkbox
    if not driver.find_element(By.ID, "chkRemember").is_selected():
        driver.find_element(By.ID, "chkRemember").click()
    if not driver.find_element(By.ID, "readStatement").is_selected():
        driver.find_element(By.ID, "readStatement").click()

    # Klik tombol login
    driver.find_element(By.ID, "btnLogin").click()

def pilih_gedung():
    gedung_elemen = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(@title, "Gedung 3 Teknik")]'))
    )
    time.sleep(5)  # delay biar siap
    gedung_elemen.click()
    print("Gedung 3 Teknik Elektro berhasil diklik.")

    # Setelah klik, pindah ke tab baru
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])
    print("Berhasil pindah ke tab dashboard monitoring.")

def check_logout():
    try:
        # Tunggu hingga elemen box expired login muncul
        logout_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gdw-message-box.active"))
        )
        
        if logout_box:
            print("Sesi login telah kedaluwarsa. Melakukan login ulang...")
            sys.stdout.flush()
            
            # Klik tombol 'Log In' pada box expired
            login_button = driver.find_element(By.CSS_SELECTOR, ".gdw-message-box-button-group button")
            login_button.click()
            
            # Panggil fungsi login lagi
            login()
    except Exception:
        pass  # Jika elemen logout tidak ditemukan, lanjutkan scraping

# Fungsi untuk memeriksa apakah saat ini adalah waktu yang tepat untuk mengirim data (menit kelipatan 5)
def is_time_to_upload():
    current_time = datetime.now()
    minute = current_time.minute
    return minute % 5 == 0  # Hanya jika menit adalah kelipatan 5

# Inisialisasi browser menggunakan Firefox
# options = Options()
# options.headless = False  # Set ke True jika ingin menjalankan Firefox tanpa antarmuka grafis

# driver = webdriver.Firefox(service=service, options=options)

try:
    login()
    pilih_gedung()

    # Loop untuk mengambil data secara berkala
    while True:
        try:
            # Cek apakah akun logout
            check_logout()

            # Refresh halaman
            driver.refresh()
            print("Halaman di-refresh untuk mendapatkan data terbaru.")
            sys.stdout.flush()

            # Delay 10 detik agar data selesai update
            time.sleep(10)

            # Ambil data 'PV Generation Today'
            pv_generation_today_value = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.kpi-item.kpi-power.today-power p"))
            ).text

            # Ambil data 'Income Today'
            income_today_value = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.kpi-item.kpi-income.today-income p"))
            ).text

            # Ambil data 'Total Generation'
            total_generation_value = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.kpi-item.kpi-power.total-power p"))
            ).text

            # Ambil data 'Total Income'
            total_income_value = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.kpi-item.kpi-income.total-income p"))
            ).text

            # Ambil data 'P' (Daya)
            power_value = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "power_div"))
            ).text

            # Upload data ke API
            upload_data(pv_generation_today_value, income_today_value, total_generation_value, total_income_value, power_value)

            print(f"PV Generation Today: {pv_generation_today_value}")
            print(f"Income Today: {income_today_value}")
            print(f"Total Generation: {total_generation_value}")
            print(f"Total Income: {total_income_value}")
            print(f"Power (Daya): {power_value}")
            sys.stdout.flush()

            # Delay random 40–60 menit sebelum loop berikutnya
            delay = random.randint(2400, 3600)
            print(f"Tidur selama {delay/60:.1f} menit sebelum refresh berikutnya...")
            sys.stdout.flush()
            time.sleep(delay)

        except Exception as e:
            print(f"Terjadi kesalahan saat mengambil data: {e}")
            sys.stdout.flush()

except Exception as e:
    print(f"Terjadi kesalahan: {e}")
finally:
    driver.quit()
