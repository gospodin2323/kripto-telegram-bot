from flask import Flask, request
import os
import requests
import logging

# Loglamayı başlat
logging.basicConfig(level=logging.INFO)

# Gerekli tek sırrı al
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOK")

# Flask uygulamasını başlat
app = Flask(__name__)

# Geri mesaj göndermek için yardımcı fonksiyon
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    # Hata ayıklama için isteği logla
    logging.info(f"Telegram'a gönderilen cevap: {payload}")
    requests.post(url, json=payload)

# Telegram'dan bir mesaj geldiğinde Vercel bu fonksiyonu çalıştırır
@app.route('/', methods=['POST'])
def webhook_handler():
    # Vercel loglarına bir iz bırakalım
    logging.info(">>> Webhook'a bir istek geldi!")
    
    if request.is_json:
        data = request.get_json()
        logging.info(f"Gelen veri: {data}") # Gelen verinin tamamını logla
        
        try:
            chat_id = data['message']['chat']['id']
            gelen_mesaj = data['message']['text']
            
            # Gelen mesajı ve chat_id'yi logla
            logging.info(f"Chat ID: {chat_id}, Gelen Mesaj: {gelen_mesaj}")
            
            # Ne gelirse gelsin, standart bir cevap gönder
            cevap_metni = f"Test başarılı! Mesajınızı aldım: '{gelen_mesaj}'"
            send_telegram_message(chat_id, cevap_metni)
            
        except KeyError:
            logging.error("Gelen veride 'message' veya 'chat' anahtarı bulunamadı.")
            return 'Error: Invalid data structure', 400

    return 'OK', 200

# Bu handler, Vercel'in ana fonksiyonu bulmasını sağlar.
handler = app
