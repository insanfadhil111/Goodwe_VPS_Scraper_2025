# 🌞 GoodWe SEMS Scraper & Data Uploader

Proyek ini adalah script Python berbasis **Selenium** yang digunakan untuk:
- Login otomatis ke portal **GoodWe SEMS**.
- Memilih plant/gedung tertentu (contoh: *Gedung 3 Teknik Elektro*).
- Scraping data monitoring **PV Generation, Income, Power** secara berkala.
- Upload data hasil scraping ke **API Smart ENMS UNS**.

---

## 🚀 Fitur
- Login otomatis ke portal [SEMS GoodWe](https://www.semsportal.com/).
- Deteksi otomatis jika sesi login **expired** → relogin.
- Ambil data berikut secara periodik:
  - **PV Generation Today**
  - **Income Today**
  - **Total Generation**
  - **Total Income**
  - **Power (Daya)**
- Upload data ke endpoint API (format JSON).
- Logging hasil scraping & upload data.

---

## 🛠️ Persyaratan

- Python **3.10+** (tested on 3.12)
- [Selenium](https://pypi.org/project/selenium/)
- [Requests](https://pypi.org/project/requests/)
- Firefox + Geckodriver

---

## 📦 Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/username/goodwe-scraper.git
   cd goodwe-scraper

2. Buat virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   
4. Setup Firefox & Geckodriver
   - Download Firefox ESR atau portable.
   - Download geckodriver
   - Letakkan di /usr/local/bin/geckodriver atau sesuaikan path di script.

## ▶️ Menjalankan Scraper
```bash
  python3 scrapping.py

```
Contoh Output:
```bash
Gedung 3 Teknik Elektro berhasil diklik.
Berhasil pindah ke tab dashboard monitoring.
Halaman di-refresh untuk mendapatkan data terbaru.
Data yang dikirim: {'P': 7575.0, 'today_generation': 25300.0, 'total_generation': 26876500.0, 'today_income': 36550, 'total_income': 38828479}
Data berhasil dikirim ke API: {'message': 'Data added successfully'}
PV Generation Today: 25.30 kWh
Income Today: 36550.91 IDR
Total Generation: 26876.50 kWh
Total Income: 38828479.55 IDR
Power (Daya): 7.575kW
```

## 📡 Arsitektur Sederhana
```bash
+-------------+        +----------------+        +------------------+
| Selenium    | -----> | GoodWe SEMS    | -----> | Scraper          |
| (Firefox)   |        | Web Dashboard  |        | (Python Script)  |
+-------------+        +----------------+        +------------------+
                                                    |
                                                    v
                                          +------------------+
                                          | Smart ENMS API   |
                                          | (iotlab-uns.com) |
                                          +------------------+


