from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Khởi tạo trình duyệt
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")
time.sleep(3)

# Chờ bảng dữ liệu xuất hiện
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.table tbody tr"))
)

# Lấy dữ liệu
rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 4:
        ma_so_thue = cols[1].text.strip()
        ten_doanh_nghiep = cols[2].text.strip()
        ngay_cap = cols[3].text.strip()
        data.append({
            "Mã số thuế": ma_so_thue,
            "Tên doanh nghiệp": ten_doanh_nghiep,
            "Ngày cấp": ngay_cap
        })

# Tạo DataFrame và lưu vào Excel
df = pd.DataFrame(data)
df.to_excel("ma_so_thue_trang_1.xlsx", index=False)

print("✅ Đã lưu dữ liệu vào ma_so_thue_trang_1.xlsx")
print("Đã lưu dữ liệu vào ma_so_thue_trang_1.xlsx")
driver.quit()
