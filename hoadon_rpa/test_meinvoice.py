from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://www.meinvoice.vn/tra-cuu"
ma_hoa_don = "B1HEIRR8N0WP"

options = Options()
driver = webdriver.Chrome(options=options)
driver.get(url)

try:
    # Chờ input hiện ra
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-tax-code"))
    )
    input_box.send_keys(ma_hoa_don)

    # Click nút tra cứu
    tra_cuu_btn = driver.find_element(By.ID, "tra-cuu-btn")
    tra_cuu_btn.click()

    # Chờ kết quả hiện ra
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "invoice-detail"))
    )
    print("✅ Tìm thấy hóa đơn!")

except Exception as e:
    print("❌ Lỗi:", e)

time.sleep(5)
driver.quit()
