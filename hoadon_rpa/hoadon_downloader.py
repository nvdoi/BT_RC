import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# === CẤU HÌNH ===
HOADON_DIR = "hoadon"
LOG_FILE = "log.txt"
os.makedirs(HOADON_DIR, exist_ok=True)

# === HÀM GHI LOG ===
def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

# === KHỞI TẠO TRÌNH DUYỆT ===
def setup_driver():
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": os.path.abspath(HOADON_DIR),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", False)  # Tự đóng trình duyệt sau khi chạy xong
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# === TẢI HÓA ĐƠN THEO MÃ VÀ TRANG ===
def download_invoice(driver, ten_ncc, ma_hoa_don, trang_tra_cuu):
    wait = WebDriverWait(driver, 20)
    driver.get(trang_tra_cuu)

    # Nhập mã hóa đơn
    input_box = wait.until(EC.presence_of_element_located((By.ID, "txtCode")))
    input_box.clear()
    input_box.send_keys(ma_hoa_don)

    # Nhấn nút tìm kiếm
    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSearchInvoice")))
    search_btn.click()

    # Nhấn nút tải hóa đơn
    download_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.res-btn.download")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", download_btn)

    # Chọn mục tải PDF
    pdf_download = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dm-item.pdf.txt-download-pdf")))
    time.sleep(1)
    pdf_download.click()

# === XỬ LÝ FILE SAU KHI TẢI ===
def move_downloaded_file(ten_ncc, ma_hoa_don):
    time.sleep(5)  # Chờ tải về

    files = [os.path.join(HOADON_DIR, f) for f in os.listdir(HOADON_DIR) if f.endswith(".pdf")]
    if not files:
        raise FileNotFoundError("Không tìm thấy file PDF nào được tải về.")

    latest_file = max(files, key=os.path.getctime)

    # Tạo thư mục nhà cung cấp nếu chưa có
    ncc_folder = os.path.join(HOADON_DIR, ten_ncc)
    os.makedirs(ncc_folder, exist_ok=True)

    # Đổi tên và di chuyển
    new_path = os.path.join(ncc_folder, f"{ma_hoa_don}.pdf")
    os.rename(latest_file, new_path)
    return new_path

# === XỬ LÝ TOÀN BỘ DANH SÁCH ===
def process_all_invoices(excel_path):
    df = pd.read_excel(excel_path)
    driver = setup_driver()

    for index, row in df.iterrows():
        ten_ncc = str(row["Ten_NCC"]).strip()
        ma_hoa_don = str(row["Ma_Hoa_Don"]).strip()
        trang_tra_cuu = str(row["Trang_Tra_Cuu"]).strip()

        try:
            log(f" Đang xử lý hóa đơn: {ma_hoa_don} từ NCC: {ten_ncc}")
            download_invoice(driver, ten_ncc, ma_hoa_don, trang_tra_cuu)
            saved_path = move_downloaded_file(ten_ncc, ma_hoa_don)
            log(f"Tải xong: {saved_path}")
        except Exception as e:
            log(f" Lỗi với hóa đơn {ma_hoa_don}: {e}")

    driver.quit()
    log("Đã đóng trình duyệt sau khi xử lý xong.")

# === CHẠY CHÍNH ===
if __name__ == "__main__":
    process_all_invoices("data.xlsx")
