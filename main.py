from flask import Flask, request
import requests
import time
import logging
import os

# ================== 🔒 GİZLİ BİLGİLER ==================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOK")
API_KEY = os.getenv("API_KEY", "YOK")
# =====================================================================

# --- ⭐ KENDİ KATEGORİ LİSTENİZ ---
FAVORI_KATEGORILER = {
    # Sizin özel kategori listeniz buraya gelecek
    "Yapay Zeka (AI)": "artificial-intelligence",
    "Meme Token": "meme-token",
}
# ----------------------------------------------------------------

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
headers = {"x-cg-demo-api-key": API_KEY}

# --- CEVAP GÖNDERME FONKSİYONUNU SADELEŞTİRDİK ---
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # Artık formatlama (Markdown) yok, sadece saf metin gönderiyoruz.
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, json=payload)
        # Hata ayıklama için Telegram'ın cevabını loglayalım
        logging.info(f"Telegram'a gönderilen cevap: {response.json()}")
    except Exception as e:
        logging.error(f"Telegram'a mesaj gönderirken hata: {e}")

# ... (search_and_filter_coins fonksiyonu aynı kalıyor) ...
def search_and_filter_coins(category, blockchain, max_mc):
    try:
        coins_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category={category}&order=market_cap_desc&per_page=250&page=1"
        response = requests.get(coins_url, headers=headers, timeout=20)
        response.raise_for_status()
        kategori_coinleri = response.json()
        on_filtrelenmis_coinler = [c for c in kategori_coinleri if c.get('market_cap') and c.get('market_cap') < max_mc]
        if not on_filtrelenmis_coinler: return "Ön filtreleme sonrası hiç aday bulunamadı."
        son_liste = []
        for coin_data in on_filtrelenmis_coinler:
            coin_id = coin_data['id']
            detay_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            detay_response = requests.get(detay_url, headers=headers)
            if detay_response.status_code == 200:
                coin_detaylari = detay_response.json()
                if coin_detaylari.get('asset_platform_id') == blockchain:
                    son_liste.append(coin_data)
            time.sleep(1.2)
        if not son_liste: return "Belirttiğiniz kriterlere uygun hiçbir coin bulunamadı."
        mesaj = f"Kriterlerinize uygun {len(son_liste)} adet coin bulundu:\n\n"
        for i, coin in enumerate(son_liste, 1):
            isim = coin.get('name'); sembol = coin.get('symbol').upper(); mc_str = f"${coin.get('market_cap'):,}"
            mesaj += f"{i}. {isim} ({sembol}) - Piyasa Değeri: {mc_str}\n"
        return mesaj
    except Exception as e:
        logging.error(f"Arama sırasında hata oluştu: {e}"); return f"Arama sırasında bir hata oluştu."

@app.route('/', methods=['POST'])
def webhook_handler():
    if request.is_json:
        data = request.get_json()
        try:
            chat_id = data['message']['chat']['id']
            text = data['message']['text']
            
            if text == '/start':
                mesaj = "Merhaba! Arama formatı:\n/search <kategori> <blokzincir> <piyasa_değeri>"
                send_telegram_message(chat_id, mesaj)
            elif text == '/kategoriler':
                mesaj = "Favori Kategorilerim:\n\n"
                for isim, cat_id in FAVORI_KATEGORILER.items():
                    mesaj += f"İsim: {isim}\nID: {cat_id}\n\n"
                send_telegram_message(chat_id, mesaj)
            elif text == '/blokzincirler':
                mesaj = "Popüler Blokzincir ID'leri:\n\nethereum\nbinance-smart-chain\nsolana"
                send_telegram_message(chat_id, mesaj)
            elif text.startswith('/search'):
                send_telegram_message(chat_id, "Aramanız başladı... Bu işlem birkaç dakika sürebilir, lütfen bekleyin.")
                parts = text.split()
                if len(parts) != 4:
                    mesaj = "Hatalı kullanım! Format:\n/search <kategori> <blokzincir> <piyasa_değeri>"
                else:
                    try:
                        category, blockchain, max_mc = parts[1], parts[2], int(parts[3])
                        mesaj = search_and_filter_coins(category, blockchain, max_mc)
                    except ValueError:
                        mesaj = "Piyasa değeri bir sayı olmalıdır!"
                send_telegram_message(chat_id, mesaj)
        except KeyError:
            logging.error("Gelen veride beklenen anahtarlar bulunamadı.")
    return 'OK', 200
