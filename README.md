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
