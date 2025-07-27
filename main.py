from flask import Flask, request
import logging

# Loglamayı başlat (Vercel'de logları görmek için)
logging.basicConfig(level=logging.INFO)

# Flask uygulamasını başlat
app = Flask(__name__)

# Hem tarayıcıdan (GET) hem de Telegram'dan (POST) gelen tüm isteklere cevap ver
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    # Vercel loglarına bir iz bırakalım
    logging.info(">>> BİR İSTEK GELDİ! <<<")
    
    # Gelen isteğin detaylarını loglayalım
    logging.info(f"Metot: {request.method}, Yol: {request.path}")
    if request.is_json:
        logging.info(f"Gelen JSON Verisi: {request.get_json()}")
    
    # Geriye basit bir cevap dönelim
    return 'OK, istek alindi.', 200
