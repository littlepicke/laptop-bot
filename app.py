from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ara")
def ara():
    keyword = request.args.get("keyword", "")
    search_url = f"https://www.sahibinden.com/laptop?search_text={keyword.replace(' ', '+')}"

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(search_url)
    time.sleep(5)

    ilanlar = driver.find_elements(By.CSS_SELECTOR, ".classified-list-item")
    urunler = []

    for ilan in ilanlar[:10]:
        try:
            baslik = ilan.find_element(By.CLASS_NAME, "classifiedTitle")
            fiyat = ilan.find_element(By.CLASS_NAME, "price")
            urunler.append({
                "baslik": baslik.text.strip(),
                "fiyat": fiyat.text.strip(),
                "link": baslik.get_attribute("href")
            })
        except:
            continue

    driver.quit()
    return render_template("results.html", keyword=keyword, urunler=urunler)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
