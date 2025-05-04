import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import os

BIEN_SO_XE = os.getenv("BIEN_SO_XE", "43A12345")
LOAI_XE = os.getenv("LOAI_XE", "oto")

def check_vi_pham():
    print("Đang kiểm tra phạt nguội...")
    driver = webdriver.Chrome()
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "BienKiemSoat"))
        )

        driver.find_element(By.NAME, "BienKiemSoat").send_keys(BIEN_SO_XE)
        select = driver.find_element(By.NAME, "LoaiXe")
        for option in select.find_elements(By.TAG_NAME, 'option'):
            if (LOAI_XE == 'oto' and "Ô tô" in option.text) or \
                (LOAI_XE == 'xemay' and "Xe máy" in option.text):
                option.click()
                break

        captcha_img = driver.find_element(By.ID, "imgCaptcha")
        ma_captcha = input("Nhập mã captcha: ")
        driver.find_element(By.NAME, "captchaInput").send_keys(ma_captcha)
        driver.find_element(By.ID, "search").click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "resultSearch"))
        )
        result = driver.find_element(By.ID, "resultSearch").text
        print("Kết quả tra cứu:", result)

    except Exception as e:
        print("Không thể tìm thấy kết quả. Có thể sai captcha hoặc lỗi mạng.")
        print("Chi tiết lỗi:", str(e))

    input("Nhấn Enter để đóng trình duyệt...")
    driver.quit()

schedule.every().day.at("06:00").do(check_vi_pham)
schedule.every().day.at("12:00").do(check_vi_pham)

print("Đang chờ đến giờ chạy kiểm tra phạt nguội!")

while True:
    schedule.run_pending()
    time.sleep(60)
