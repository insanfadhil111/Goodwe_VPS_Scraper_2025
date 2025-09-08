from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

service = Service("/usr/local/bin/geckodriver")
options = Options()
options.binary_location = "/opt/firefox/firefox"  # paksa ke binary firefox
options.add_argument("--headless")  # wajib di server

driver = webdriver.Firefox(service=service, options=options)
driver.get("https://example.com")
print(driver.title)
driver.quit()
