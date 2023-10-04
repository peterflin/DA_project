# 程式執行說明
clone程式後，請先執行，以安裝需求套件
```bash
pip install -r requirements.txt
```
## 試題1
未完成，只完成使用selenium取得頁面上的驗證碼截圖，並使用ddddocr套件完成驗證碼辨識，程式碼部分參考"試題1/doorplate.py"
## 試題2
合併題目三執行(轉換完直接寫入DB)，首先啟動好mongodb
```
docker pull mongo:7.0.2
docker run --name mongodb --rm -d --privileged=true -p 27017:27017 mongo:7.0.2
```
確認DB啟動成功後，執行下列指令
```
cd "試題2"
python transform.py
```
## 試題3
![](https://hackmd.io/_uploads/BksSaY5xp.png)
