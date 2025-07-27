from flask import Flask, request
import requests
import time
import logging
import os
import json # JSON dosyasını okumak için eklendi

# ================== 🔒 GİZLİ BİLGİLER ==================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOK")
API_KEY = os.getenv("API_KEY", "YOK")
# =====================================================================

# --- ⭐ KATEGORİLER ARTIK BU DOSYADAN OKUNACAK ---
FAVORI_KATEGORILER = {}
try:
    with open('categories.json', 'r', encoding='utf-8') as f:
        FAVORI_KATEGORILER = json.load(f)
except FileNotFoundError:
    logging.error("categories.json dosyası bulunamadı!")
except json.JSONDecodeError:
    logging.error("categories.json dosyasında format hatası var!")
# ----------------------------------------------------------------

app = Flask(__name__)
# ... (Kodun geri kalanında hiçbir değişiklik yok, olduğu gibi kalabilir)
# ...
# Flask, search_and_filter_coins, start, search, kategoriler, blokzincirler, webhook_handler fonksiyonları...

# Kodun geri kalanını bir önceki mesajımdan kopyalayıp buraya yapıştırabilirsiniz
# veya daha kolayı, sadece yukarıdaki FAVORI_KATEGORILER bloğunu güncelleyebilirsiniz.
# Emin olmak için tam kodu aşağıya tekrar ekliyorum.
logging.basicConfig(level=logging.INFO)
headers = {"x-cg-demo-api-key": API_KEY}

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        logging.error(f"Telegram'a mesaj gönderirken hata: {e}")

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
        mesaj = f"✅ Kriterlerinize uygun {len(son_liste)} adet coin bulundu:\n\n"
        for i, coin in enumerate(son_liste, 1):
            isim = coin.get('name'); sembol = coin.get('symbol').upper(); mc_str = f"${coin.get('market_cap'):,}"
            mesaj += f"{i}. **{isim} ({sembol})**\n   Piyasa Değeri: {mc_str}\n"
        return mesaj
    except Exception as e:
        logging.error(f"Arama sırasında hata oluştu: {e}"); return f"❌ Arama sırasında bir hata oluştu."

@app.route('/', methods=['POST'])
def webhook_handler():
    if request.is_json:
        data = request.get_json()
        try:
            chat_id = data['message']['chat']['id']
            text = data['message']['text']
            
            if text == '/start':
                mesaj = "Merhaba! Arama formatı:\n`/search <kategori> <blokzincir> <piyasa_değeri>`"
                send_telegram_message(chat_id, mesaj)
            elif text == '/kategoriler':
                if FAVORI_KATEGORILER:
                    mesaj = "⭐ **Favori Kategorilerim:**\n\n"
                    for isim, cat_id in FAVORI_KATEGORILER.items():
                        mesaj += f"**İsim:** {isim}\n**Kullanılacak ID:** `{cat_id}`\n\n"
                    # Mesaj çok uzun olabileceğinden, parçalara ayırarak gönderelim
                    for i in range(0, len(mesaj), 4000):
                        send_telegram_message(chat_id, mesaj[i:i + 4000])
                else:
                    send_telegram_message(chat_id, "Hata: Kategori listesi yüklenemedi.")
            elif text == '/blokzincirler':
                mesaj = "**Popüler Blokzincir ID'leri:**\n\n`ethereum`\n`binance-smart-chain`\n`solana`"
                send_telegram_message(chat_id, mesaj)
            elif text.startswith('/search'):
                send_telegram_message(chat_id, "🔍 Aramanız başladı... Bu işlem birkaç dakika sürebilir, lütfen bekleyin.")
                parts = text.split()
                if len(parts) != 4:
                    mesaj = "Hatalı kullanım! Format:\n`/search <kategori> <blokzincir> <piyasa_değeri>`"
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
