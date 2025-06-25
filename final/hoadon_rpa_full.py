# === 1. IMPORT VÀ CẤU HÌNH ===
import os
import time
import pandas as pd
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# === CẤU HÌNH THƯ MỤC ===
BASE_DIR = r"G:\\BT RC\\final"
HOADON_DIR = os.path.join(BASE_DIR, "invoices")
XML_DIR = os.path.join(HOADON_DIR, "xml")
PDF_DIR = os.path.join(HOADON_DIR, "pdf")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")
INPUT_FILE = os.path.join(BASE_DIR, "input.xlsx")
OUTPUT_FILE = os.path.join(BASE_DIR, "output.xlsx")

os.makedirs(XML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# === 2. GHI LOG ===
def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

# === 3. CấU HÌNH TRÌNH DUYỆT ===
def setup_driver(download_dir):
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": os.path.abspath(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", False)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === 4. TRA CỨU HÓA ĐƠN TỬa 3 HỆ THỐNG ===
def tra_cuu_fpt(driver, mst, ma_tra_cuu):
    wait = WebDriverWait(driver, 20)
    driver.get("https://tracuuhoadon.fpt.com.vn/search.html")

    mst_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='MST bên bán']")))
    mst_box.clear()
    mst_box.send_keys(mst)

    code_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mã tra cứu hóa đơn']")))
    code_box.clear()
    code_box.send_keys(ma_tra_cuu)

    tra_cuu_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.webix_icon_btn.wxi-search")))
    tra_cuu_btn.click()

    time.sleep(4)
    if "Không tìm thấy hóa đơn" in driver.page_source:
        raise Exception("Không tìm thấy hóa đơn")

    xml_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.webix_icon_btn.mdi-xml")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", xml_icon)
    time.sleep(1)
    xml_icon.click()

def tra_cuu_meinvoice(driver, ma_tra_cuu):
    wait = WebDriverWait(driver, 20)
    driver.get("https://www.meinvoice.vn/tra-cuu/")

    input_box = wait.until(EC.presence_of_element_located((By.ID, "txtCode")))
    input_box.clear()
    input_box.send_keys(ma_tra_cuu)

    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSearchInvoice")))
    search_btn.click()

    download_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.res-btn.download")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", download_btn)

    xml_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dm-item.xml.txt-download-xml")))
    time.sleep(1)
    xml_btn.click()

def tra_cuu_ehoadon(driver, ma_tra_cuu):
    wait = WebDriverWait(driver, 20)
    driver.get("https://van.ehoadon.vn/TCHD?MTC")

    code_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Nhập Mã tra cứu Hóa đơn']")))
    code_box.clear()
    code_box.send_keys(ma_tra_cuu)

    tra_cuu_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.btnSearch")))
    tra_cuu_btn.click()

    iframe = wait.until(EC.presence_of_element_located((By.ID, "frameViewInvoice")))
    driver.switch_to.frame(iframe)

    btn_download = wait.until(EC.presence_of_element_located((By.ID, "btnDownload")))
    actions = ActionChains(driver)
    actions.move_to_element(btn_download).perform()
    time.sleep(1)

    link_xml = wait.until(EC.element_to_be_clickable((By.ID, "LinkDownXML")))
    link_xml.click()

    driver.switch_to.default_content()

# === 5. PHÂN TÍCH FILE XML ===
def parse_fpt(root):
    dlhdon = root.find(".//DLHDon")
    if dlhdon is None:
        return {}

    ttchung = dlhdon.find("TTChung")
    ndhdon = dlhdon.find("NDHDon")
    nban = ndhdon.find("NBan") if ndhdon is not None else None
    nmua = ndhdon.find("NMua") if ndhdon is not None else None

    return {
        "Số hóa đơn": ttchung.findtext("SHDon", "") if ttchung is not None else "",
        "Đơn vị bán hàng": nban.findtext("Ten", "") if nban is not None else "",
        "Mã số thuế bên bán (XML)": nban.findtext("MST", "") if nban is not None else "",
        "Địa chỉ bên bán": nban.findtext("DChi", "") if nban is not None else "",
        "Số tài khoản bên bán": nban.findtext("STKNHang", "") if nban is not None else "",
        "Điện thoại bên bán": nban.findtext("SDThoai", "") if nban is not None else "",
        "Họ tên người mua hàng": nmua.findtext("HVTNMHang", "") if nmua is not None else "",
        "Tên đơn vị mua": nmua.findtext("Ten", "") if nmua is not None else "",
        "Mã số thuế bên mua (XML)": nmua.findtext("MST", "") if nmua is not None else "",
        "Địa chỉ bên mua": nmua.findtext("DChi", "") if nmua is not None else "",
        "Số tài khoản bên mua": nmua.findtext("STKNHang", "") if nmua is not None else ""
    }

def parse_meinvoice(root):
    ttchung = root.find(".//TTChung")
    ndhdon = root.find(".//NDHDon")
    nban = root.find(".//NBan")
    nmua = root.find(".//NMua")

    return {
        "Số hóa đơn": ttchung.findtext("SHDon", "") if ttchung is not None else "",
        "Đơn vị bán hàng": nban.findtext("Ten", "") if nban is not None else "",
        "Mã số thuế bên bán (XML)": nban.findtext("MST", "") if nban is not None else "",
        "Địa chỉ bên bán": nban.findtext("DChi", "") if nban is not None else "",
        "Số tài khoản bên bán": nban.findtext("STKNHang", "") if nban is not None else "",
        "Điện thoại bên bán": nban.findtext("SDThoai", "") if nban is not None else "",
        "Họ tên người mua hàng": nmua.findtext("HVTNMHang", "") if nmua is not None else "",
        "Tên đơn vị mua": nmua.findtext("Ten", "") if nmua is not None else "",
        "Mã số thuế bên mua (XML)": nmua.findtext("MST", "") if nmua is not None else "",
        "Địa chỉ bên mua": nmua.findtext("DChi", "") if nmua is not None else "",
        "Số tài khoản bên mua": nmua.findtext("STKNHang", "") if nmua is not None else ""
    }

def parse_ehoadon(root):
    ttchung = root.find(".//TTChung")
    ndhdon = root.find(".//NDHDon")
    nban = ndhdon.find("NBan") if ndhdon is not None else None
    nmua = ndhdon.find("NMua") if ndhdon is not None else None

    return {
        "Số hóa đơn": ttchung.findtext("SHDon", "") if ttchung is not None else "",
        "Đơn vị bán hàng": nban.findtext("Ten", "") if nban is not None else "",
        "Mã số thuế bên bán (XML)": nban.findtext("MST", "") if nban is not None else "",
        "Địa chỉ bên bán": nban.findtext("DChi", "") if nban is not None else "",
        "Số tài khoản bên bán": nban.findtext("STKNHang", "") if nban is not None else "",
        "Điện thoại bên bán": nban.findtext("SDThoai", "") if nban is not None else "",
        "Họ tên người mua hàng": nmua.findtext("HVTNMHang", "") if nmua is not None else "",
        "Tên đơn vị mua": nmua.findtext("Ten", "") if nmua is not None else "",
        "Mã số thuế bên mua (XML)": nmua.findtext("MST", "") if nmua is not None else "",
        "Địa chỉ bên mua": nmua.findtext("DChi", "") if nmua is not None else "",
        "Số tài khoản bên mua": nmua.findtext("STKNHang", "") if nmua is not None else ""
    }

def extract_info_from_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        if root.find(".//DLHDon") is not None:
            return parse_fpt(root)
        elif root.find(".//NBan") is not None and root.find(".//TTChung") is not None:
            return parse_meinvoice(root)
        elif root.find(".//NDHDon") is not None and root.find(".//NBan") is not None:
            return parse_ehoadon(root)
        else:
            log(f"❌ Không xác định được định dạng XML: {xml_path}")
            return {}
    except Exception as e:
        log(f"❌ Lỗi phân tích XML {xml_path}: {e}")
        return {}

# === 6. Xử LÝ DANH SÁCH HÓA ĐƠN ===
def process_all():
    df = pd.read_excel(INPUT_FILE, dtype={"Mã số thuế": str, "Mã tra cứu": str})
    driver_xml = setup_driver(XML_DIR)
    results = []
    stt = 1

    for index, row in df.iterrows():
        mst_raw = str(row.get("Mã số thuế", "")).strip()
        ma_tra_cuu = str(row["Mã tra cứu"]).strip()
        url = str(row["URL"]).strip()

        record = {
            "STT": stt,
            "MST (input)": mst_raw,
            "Mã tra cứu": ma_tra_cuu,
            "URL": url,
        }

        try:
            if "fpt" in url:
                if not mst_raw.isdigit():
                    raise Exception("MST không hợp lệ")
                mst = mst_raw.zfill(10)
                before_files = set(os.listdir(XML_DIR))
                tra_cuu_fpt(driver_xml, mst, ma_tra_cuu)
                time.sleep(4)
            elif "meinvoice" in url:
                before_files = set(os.listdir(XML_DIR))
                tra_cuu_meinvoice(driver_xml, ma_tra_cuu)
                time.sleep(4)
            elif "ehoadon" in url:
                before_files = set(os.listdir(XML_DIR))
                tra_cuu_ehoadon(driver_xml, ma_tra_cuu)
                time.sleep(4)
            else:
                raise Exception("Không hỗ trợ URL này")

            after_files = set(os.listdir(XML_DIR))
            new_files = list(after_files - before_files)
            xml_files = [f for f in new_files if f.lower().endswith(".xml")]
            if not xml_files:
                raise Exception("Không tìm thấy file XML sau khi tải")
            xml_path = os.path.join(XML_DIR, xml_files[0])
            invoice_data = extract_info_from_xml(xml_path)
            record.update(invoice_data)
            record["Status"] = "success"

            log(f" ✓ Thành công: {ma_tra_cuu} | {url}")
        except Exception as e:
            record.update({
                "Số hóa đơn": 0,
                "Đơn vị bán hàng": 0,
                "Mã số thuế bên bán (XML)": 0,
                "Địa chỉ bên bán": 0,
                "Số tài khoản bên bán": 0,
                "Điện thoại bên bán": 0,
                "Họ tên người mua hàng": 0,
                "Tên đơn vị mua": 0,
                "Mã số thuế bên mua (XML)": 0,
                "Địa chỉ bên mua": 0,
                "Số tài khoản bên mua": 0,
                "Status": "fail",
                "Error": str(e)
            })
            log(f" ! Lỗi: {ma_tra_cuu} | {url} | {e}")

        results.append(record)
        stt += 1

    pd.DataFrame(results).to_excel(OUTPUT_FILE, index=False)
    driver_xml.quit()
    log("\n=== KẾT THÚc Xử LÝ ===")

# === 7. MAIN ===
if __name__ == "__main__":
    process_all()
