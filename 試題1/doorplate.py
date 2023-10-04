from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import ddddocr
import numpy as np
import io
from PIL import Image
import cv2


if __name__ == '__main__':
    url = "https://www.ris.gov.tw/info-doorplate/app/doorplate/main?retrievalPath=%2Fdoorplate%2F"
    option = Options()
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    # driver.get(url)
    # time.sleep(2)
    # e = driver.find_element(By.CSS_SELECTOR, ".btn.btn-info.btn-block.ps-classification")
    # e.click()
    # 取得element的截圖
    img = driver.find_element(By.CSS_SELECTOR, ".td2 > img")
    imageStream = io.BytesIO(img.screenshot_as_png)
    imageFile = Image.open(imageStream)
    image = cv2.cvtColor(np.asarray(imageFile), cv2.COLOR_RGB2GRAY)
    cv2.imwrite("image.png", image)
    # 取得驗證碼
    ocr = ddddocr.DdddOcr()
    with open('image.png', 'rb') as f:
        img_bytes = f.read()
    captcha_code = ocr.classification(img_bytes).upper()
