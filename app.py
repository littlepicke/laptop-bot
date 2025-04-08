import os
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def ara():
    if request.method == "POST":
        islemci = request.form.get("islemci")
        # Kullanıcıdan gelen işlemci kriterini al
        if islemci:
            # ChromeDriver için seçenekler
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # ChromeDriver sürümünü manuel belirt
            driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install(), options=chrome_options)

            # Burada sahibinden.com üzerindeki arama işlemini yapabilirsin.
            # Bu kısmı, işlemi gerçekleştirip sonuçları almak için geliştirebilirsin.
            driver.get(f"https://www.sahibinden.com/laptop?search_text={islemci}")
            # Örneğin, sayfadaki başlıkları almak
            titles = driver.find_elements_by_class_name("classifiedTitle")

            results = []
            for title in titles:
                results.append(title.text)
            driver.quit()  # İşlem tamamlandıktan sonra driver'ı kapat

            return render_template("results.html", results=results)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
