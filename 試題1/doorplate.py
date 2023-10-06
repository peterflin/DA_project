from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import ddddocr
import numpy as np
import io
from PIL import Image
import cv2
import time
from datetime import datetime
import pandas as pd


if __name__ == '__main__':
    url = "https://www.ris.gov.tw/info-doorplate/app/doorplate/main?retrievalPath=%2Fdoorplate%2F"
    option = Options()
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url)
    time.sleep(3)
    # 點選 "以編釘日期、編釘類別查詢" ==> 進入第二個畫面
    e = driver.find_element(By.CSS_SELECTOR, ".btn.btn-info.btn-block.ps-classification")
    time.sleep(1)
    e.click()
    time.sleep(3)
    # 點選 "桃園市" ==> 進入第三個畫面
    e = driver.find_elements(By.CSS_SELECTOR, "#mapForm > .form-group-odd.text-center > fieldset > .col-xs-12 > map > area")
    time.sleep(1)
    e[1].click()
    time.sleep(3)
    # 點選 "鄉鎮市區"選項
    e = driver.find_element(By.CSS_SELECTOR, "#areaCode")
    e.click()
    time.sleep(1)
    # 點選 "桃園市"
    opts = e.find_elements(By.CSS_SELECTOR, "option")
    opts[1].click()
    time.sleep(1)
    e.click()
    # sDate
    driver.find_element(By.CSS_SELECTOR, "#sDate").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-year.form-control.inline.min-control.yyymmdd").click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-year.form-control.inline.min-control.yyymmdd > option")[-2].click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-month.form-control.inline.min-control.yyymmdd").click()
    driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-month.form-control.inline.min-control.yyymmdd > option")[0].click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, ".ui-state-default")[0].click()
    time.sleep(1)
    # eDate
    driver.find_element(By.CSS_SELECTOR, "#eDate").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-year.form-control.inline.min-control.yyymmdd").click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-year.form-control.inline.min-control.yyymmdd > option")[-1].click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-month.form-control.inline.min-control.yyymmdd").click()
    driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-month.form-control.inline.min-control.yyymmdd > option")[datetime.today().month-1].click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, ".ui-state-default")[datetime.today().day-1].click()
    time.sleep(1)
    # 取得驗證碼的截圖
    img = driver.find_element(By.CSS_SELECTOR, "#captchaImage_captchaKey")
    imageStream = io.BytesIO(img.screenshot_as_png)
    imageFile = Image.open(imageStream)
    # image = cv2.cvtColor(np.asarray(imageFile), cv2.COLOR_RGB2GRAY)
    image = np.asarray(imageFile)
    cv2.imwrite("image.png", image)
    # 取得驗證碼
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open('image.png', 'rb') as f:
        img_bytes = f.read()
    captcha_code = ocr.classification(img_bytes).upper()
    print(captcha_code)
    while len(captcha_code) < 5:  # 如果辨識錯誤，會不足5碼，點選重新生產驗證碼後重新辨識
        driver.find_element(By.CSS_SELECTOR, "#imageBlock_captchaKey").click()
        time.sleep(1)
        img = driver.find_element(By.CSS_SELECTOR, "#captchaImage_captchaKey")
        imageStream = io.BytesIO(img.screenshot_as_png)
        imageFile = Image.open(imageStream)
        # image = cv2.cvtColor(np.asarray(imageFile), cv2.COLOR_RGB2GRAY)
        image = np.asarray(imageFile)
        cv2.imwrite("image.png", image)
        # # 取得驗證碼
        ocr = ddddocr.DdddOcr(show_ad=False)
        with open('image.png', 'rb') as f:
            img_bytes = f.read()
        captcha_code = ocr.classification(img_bytes).upper()
        print(captcha_code)
    # 填入驗證碼
    driver.find_element(By.CSS_SELECTOR, "#captchaInput_captchaKey").send_keys(captcha_code)
    time.sleep(1)
    # 點選"查詢"
    driver.find_element(By.ID, "goSearch").click()
    time.sleep(1)
    # 資料儲存
    df_data = []
    for row in driver.find_elements(By.CSS_SELECTOR, "#jQGrid > tbody > tr")[1:]:
        df_data.append([e.text.strip() for i, e in enumerate(row.find_elements(By.CSS_SELECTOR, "td")[1:])])
    time.sleep(1)
    total_pages = int(driver.find_element(By.ID, "sp_1_result-pager").text)
    for page in range(2):
        driver.find_element(By.ID, "next_result-pager").click()
        time.sleep(2)
        for row in driver.find_elements(By.CSS_SELECTOR, "#jQGrid > tbody > tr")[1:]:
            df_data.append([e.text.strip() for i, e in enumerate(row.find_elements(By.CSS_SELECTOR, "td")[1:])])
    time.sleep(1)
    df = pd.DataFrame(data=df_data,
                      columns=[e.text.strip() for e in driver.find_elements(By.CSS_SELECTOR, ".ui-jqgrid-htable > thead > tr > th")[1:]])
    df.to_csv("doorplate.csv", index_label=False)
