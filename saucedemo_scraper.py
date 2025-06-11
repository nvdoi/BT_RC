from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Danh sách user
usernames = [
    "standard_user", "locked_out_user", "problem_user",
    "performance_glitch_user", "error_user", "visual_user"
]
password = "secret_sauce"

# Cấu hình Chrome
options = Options()
options.add_argument("--headless")  # Gỡ dòng này nếu bạn muốn thấy trình duyệt chạy
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

results = []

for username in usernames:
    try:
        driver.get("https://www.saucedemo.com")
        time.sleep(1)

        # Đăng nhập
        user_input = driver.find_element(By.ID, "user-name")
        pass_input = driver.find_element(By.ID, "password")
        user_input.clear()
        pass_input.clear()
        user_input.send_keys(username)
        pass_input.send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        if "inventory" in driver.current_url:
            print(f"Đăng nhập thành công với: {username}")

            items = driver.find_elements(By.CLASS_NAME, "inventory_item")
            for item in items:
                name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
                results.append({
                    "username": username,
                    "product_name": name,
                    "price": price
                })

            # Mở menu và logout
            driver.find_element(By.ID, "react-burger-menu-btn").click()
            time.sleep(1)
            logout_btn = driver.find_element(By.ID, "logout_sidebar_link")
            driver.execute_script("arguments[0].click();", logout_btn)
            time.sleep(1)
        else:
            print(f"Không đăng nhập được với: {username}")
            time.sleep(1)
    except Exception as e:
        print(f"Lỗi với {username}: {e}")

# Đóng trình duyệt
driver.quit()

# Lưu kết quả ra Excel
df = pd.DataFrame(results)
df.to_excel("saucedemo_products.xlsx", index=False)

print("Đã lưu kết quả vào file saucedemo_products.xlsx")
