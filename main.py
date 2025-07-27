from flask import Flask, request
import requests
import time
import logging
import os
import json

# ================== 🔒 GİZLİ BİLGİLER ==================
# Bu bilgileri Vercel'in "Environment Variables" bölümünden alıyoruz.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOK")
API_KEY = os.getenv("API_KEY", "YOK")
# =====================================================================

# --- ⭐ KENDİ KATEGORİ LİSTENİZ ---
FAVORI_KATEGORILER = {
    # Burası sizin özel kategori listenizle dolu olmalı
"AI Agent Launchpad": "ai-agent-launchpad",
"AI Agents": "ai-agents",
"AI Applications": "ai-applications",
"AI Framework": "ai-framework",
"AI Meme": "ai-meme-coins",
"Andreessen Horowitz (a16z) Portfolio": "andreessen-horowitz-a16z-portfolio",
"Anime-Themed": "anime-themed-coins",
"Animoca Brands Portfolio": "animoca-brands",
"ApeChain Ecosystem": "apechain-ecosystem",
"Aptos Ecosystem": "aptos-ecosystem",
"Arbitrum Ecosystem": "arbitrum-ecosystem",
"Arcade Games": "arcade-games",
"Art": "art",
"Artificial Intelligence (AI)": "artificial-intelligence",
"Avalanche Ecosystem": "avalanche-ecosystem",
"Base Ecosystem": "base-ecosystem",
"Base Meme": "base-meme-coins",
"Big Data": "big-data",
"Binance Alpha Spotlight": "binance-alpha-spotlight",
"Binance HODLer Airdrops": "binance-hodler-airdrops",
"Binance Launchpad": "binance-launchpad",
"Binance Launchpool": "binance-launchpool",
"Binance Megadrop": "binance-megadrop",
"Binance Wallet IDO": "binance-wallet-ido",
"Blockchain Capital Portfolio": "blockchain-capital-portfolio",
"BNB Chain Ecosystem": "binance-smart-chain",
"Boba BNB Ecosystem": "boba-bnb-ecosystem",
"Boba Network Ecosystem": "boba-network-ecosystem",
"BRC-20": "brc-20",
"BTCfi Protocol": "btcfi",
"Business Services": "business-services",
"Card Games": "card-games",
"Cat-Themed": "cat-themed-coins",
"Centralized Exchange (CEX) Token": "centralized-exchange-token-cex",
"ChainGPT Launchpad": "chaingpt-pad",
"Chiliz Ecosystem": "chiliz-ecosystem",
"Chinese Meme": "chinese-meme",
"Circle Ventures Portfolio": "circle-ventures-portfolio",
"Coinbase 50 Index": "coinbase-50-index",
"Coinbase Ventures Portfolio": "coinbase-ventures-portfolio",
"Collectibles": "collectibles",
"DaoMaker Launchpad": "daomaker-ecosystem",
"daos.fun Ecosystem": "daos-fun-ecosystem",
"Data Availability": "data-availability",
"Decentralized Exchange (DEX)": "decentralized-exchange",
"Decentralized Finance (DeFi)": "decentralized-finance-defi",
"Decentralized Identifier (DID)": "identity",
"Decentralized Science (DeSci)": "decentralized-science-desci",
"DeFAI": "defai",
"DeFiance Capital Portfolio": "defiance-capital-portfolio",
"DeFi Index": "defi-index",
"Delphi Ventures Portfolio": "delphi-ventures-portfolio",
"DePIN": "depin",
"Derivatives": "decentralized-derivatives",
"Desci Meme": "desci-meme",
"Dex Aggregator": "dex-aggregator",
"Directed Acyclic Graph (DAG)": "directed-acyclic-graph-dag",
"Dogechain Ecosystem": "dogechain-ecosystem",
"Dog-Themed": "dog-themed-coins",
"DragonFly Capital Portfolio": "dragonfly-capital-portfolio",
"DRC-20": "drc-20",
"Duck-Themed": "duck-themed-coins",
"DWF Labs Portfolio": "dwf-labs-portfolio",
"Education": "education",
"Elon Musk-Inspired": "elon-musk-inspired-coins",
"Emoji-Themed": "emoji-themed",
"Energi Ecosystem": "energi-ecosystem",
"Entertainment": "entertainment",
"Ethereum Ecosystem": "ethereum-ecosystem",
"Ethereum PoS IOU": "ethereum-pos-iou",
"EthereumPoW Ecosystem": "ethereumpow-ecosystem",
"Exchange-based Tokens": "exchange-based-tokens",
"Fan Token": "fan-token",
"Fantom Ecosystem": "fantom-ecosystem",
"Farcaster Ecosystem": "farcaster-ecosystem",
"Farming-as-a-Service (FaaS)": "farming-as-a-service-faas",
"Farming Games": "farming-games",
"Fighting Games": "fighting-games",
"Fixed Interest": "fixed-interest",
"Flare Network Ecosystem": "flare-network-ecosystem",
"Flaunch Ecosystem": "flaunch-ecosystem",
"Floor Protocol Tokens": "flooring-protocol",
"Four.meme Ecosystem": "four-meme-ecosystem",
"Fractionalized NFT": "fractionalized-nft",
"Fraxtal Ecosystem": "fraxtal-ecosystem",
"Friend.tech Ecosystem": "friend-tech",
"Frog-Themed": "frog-themed-coins",
"Galaxy Digital Portfolio": "galaxy-digital-portfolio",
"Gambling (GambleFi)": "gambling",
"Game Studio": "game-studio",
"Gaming Blockchains": "gaming-blockchains",
"Gaming (GameFi)": "gaming",
"Gaming Governance Token": "gaming-governance-token",
"Gaming Marketplace": "gaming-marketplace",
"Gaming Platform": "gaming-platform",
"Gaming Utility Token": "gaming-utility-token",
"Glue Ecosystem": "glue-ecosystem",
"GMCI 30 Index": "gmci-30-index",
"GMCI DeFi Index": "gmci-defi-index",
"GMCI DePIN Index": "gmci-depin-index",
"GMCI Index": "gmci-index",
"GMCI Layer 1 Index": "gmci-layer-1-index",
"GMCI Layer 2 Index": "gmci-layer-2-index",
"GMCI Meme Index": "gmci-meme-index",
"Gnosis Chain Ecosystem": "xdai-ecosystem",
"Gotchiverse": "gotchiverse",
"Graphite Network Ecosystem": "graphite-network-ecosystem",
"GraphLinq Ecosystem": "graphlinq-ecosystem",
"Gravity Alpha Ecosystem": "gravity-alpha-ecosystem",
"Healthcare": "healthcare",
"HyperEVM Ecosystem": "hyperevm-ecosystem",
"Hyperliquid Ecosystem": "hyperliquid-ecosystem",
"Impossible Finance Launchpad": "impossible-launchpad",
"Index": "index-coin",
"Index Coop Defi Index": "defi-pulse-index-dpi",
"Index Coop Index": "index-coop-index",
"Infrastructure": "infrastructure",
"Inscriptions": "inscriptions",
"Insurance": "insurance",
"Internet of Things (IOT)": "internet-of-things-iot",
"Launchpad": "launchpad",
"Layer 1 (L1)": "layer-1",
"Layer 2 (L2)": "layer-2",
"Layer 3 (L3)": "layer-3-l3",
"LetsBONK.fun Ecosystem": "letsbonk-fun-ecosystem",
"Made in China": "made-in-china",
"Made in USA": "made-in-usa",
"Mascot-Themed": "mascot-themed",
"Media": "media",
"Meme": "meme-token",
"Memecoin NFTs": "memecoin-nfts",
"MemeCore Ecosystem": "memecore-ecosystem",
"Memeland Ecosystem": "memeland-ecosystem",
"Metaverse": "metaverse",
"Mobile Mining": "mobile-mining",
"Modular Blockchain": "modular-blockchain",
"Move To Earn": "move-to-earn",
"Multicoin Capital Portfolio": "multicoin-capital-portfolio",
"Murad Picks": "murad-picks",
"Music": "music",
"Name Service": "name-service",
"NFT": "non-fungible-tokens-nft",
"NFTFi": "nftfi",
"NFT Index": "nft-index",
"NFT Marketplace": "nft-marketplace",
"OKX Ventures Portfolio": "okx-ventures-portfolio",
"On-chain Gaming": "on-chain-gaming",
"opBNB Ecosystem": "opbnb-ecosystem",
"Oracle": "oracle",
"Outlier Ventures Portfolio": "outlier-ventures-portfolio",
"Pantera Capital Portfolio": "pantera-capital-portfolio",
"Paradigm Portfolio": "paradigm-portfolio",
"Parody Meme": "parody-meme-coins",
"Payment Solutions": "payment-solutions",
"Perpetuals": "decentralized-perpetuals",
"Play To Earn": "play-to-earn",
"Polkadot Ecosystem": "dot-ecosystem",
"Polychain Capital Portfolio": "polychain-capital-portfolio",
"Polygon Ecosystem": "polygon-ecosystem",
"Poolz Finance Launchpad": "poolz-finance-launchpad",
"Prediction Markets": "prediction-markets",
"Privacy": "privacy-coins",
"Privacy Blockchain": "privacy-blockchain",
"Proof of Memes Ecosystem": "proof-of-memes-ecosystem",
"Proof of Stake (PoS)": "proof-of-stake-pos",
"Proof of Work (PoW)": "proof-of-work-pow",
"Pump.fun Ecosystem": "pump-fun",
"Pump Science Ecosystem": "pump-science-ecosystem",
"Racing Games": "racing-games",
"Real World Assets (RWA)": "real-world-assets-rwa",
"Rollup": "rollup",
"RPG": "rpg",
"Runes": "runes",
"RWA Protocol": "rwa-protocol",
"Sequoia Capital Portfolio": "sequoia-capital-portfolio",
"Shooting Games": "shooting-games",
"Simulation Games": "simulation-games",
"Smart Contract Platform": "smart-contract-platform",
"SocialFi": "socialfi",
"Software as a service": "software",
"Solana Ecosystem": "solana-ecosystem",
"Solana Meme": "solana-meme-coins",
"Sports": "sports",
"Sports Games": "sports-games",
"SRC-20": "src-20",
"Sticker-Themed Coins": "sticker-themed-coin",
"Stock market-themed": "stock-market-themed",
"Storage": "storage",
"Strategy Games": "strategy-games",
"Sui Ecosystem": "sui-ecosystem",
"Sui Meme": "sui-meme",
"Synthetic": "synthetic",
"Tap to Earn": "tap-to-earn",
"Telegram Apps": "telegram_apps",
"Terminal of Truths": "terminal-of-truths",
"The Boy’s Club": "the-boy-s-club",
"TikTok Meme": "tiktok-meme",
"Time.fun Ecosystem": "time-fun-ecosystem",
"TokenFi Launchpad": "tokenfi-launchpad",
"Tokenized Real Estate": "real-estate",
"TON Ecosystem": "ton-ecosystem",
"TON Meme": "ton-meme-coins",
"VPN": "vpn",
"Wallets": "wallets",
"Wojak-Themed": "wojak-themed",
"World Liberty Financial Portfolio": "world-liberty-financial-portfolio",
"YZi Labs (Prev. Binance Labs) Portfolio": "binance-labs-portfolio",
"Zero Knowledge (ZK)": "zero-knowledge-zk",
"Zero Network Ecosystem": "zero-network-ecosystem",
"zkLink Nova Ecosystem": "zklink-nova-ecosystem",
"ZkSync Ecosystem": "zksync-ecosystem",
"Zora Ecosystem": "zora-ecosystem",
"Retail": "retail",
"4chan Themed": "4chan-themed",
"Ether-fi Ecosystem": "ether-fi-ecosystem",
}
# ----------------------------------------------------------------

# Flask uygulamasını başlatma
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
headers = {"x-cg-demo-api-key": API_KEY}

# Mesaj gönderme fonksiyonu
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # Telegram'ın Markdown formatını doğru işlemesi için bazı karakterlerden kaçınma
    safe_text = text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
    payload = {"chat_id": chat_id, "text": safe_text, "parse_mode": "MarkdownV2"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        logging.error(f"Telegram'a mesaj gönderirken hata: {e}")

# Ana "gem avcısı" fonksiyonu
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
            mesaj += f"{i}. *{isim} ({sembol})*\n   Piyasa Değeri: {mc_str}\n"
        return mesaj
    except Exception as e:
        logging.error(f"Arama sırasında hata oluştu: {e}"); return f"❌ Arama sırasında bir hata oluştu. API anahtarınızın doğru olduğundan emin olun."

# Telegram'dan gelen istekleri işleyen ana fonksiyon
@app.route('/', methods=['POST'])
def webhook_handler():
    if request.is_json:
        data = request.get_json()
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        
        mesaj = ""
        
        if text == '/start':
            mesaj = "Merhaba! Arama formatı:\n`/search <kategori> <blokzincir> <piyasa_değeri>`"
            send_telegram_message(chat_id, mesaj)
        elif text == '/kategoriler':
            mesaj = "⭐ *Favori Kategorilerim:*\n\n"
            for isim, cat_id in FAVORI_KATEGORILER.items():
                mesaj += f"*{isim}*\nID: `{cat_id}`\n\n"
            send_telegram_message(chat_id, mesaj)
        elif text == '/blokzincirler':
            mesaj = "*Popüler Blokzincir ID'leri:*\n\n`ethereum`\n`binance-smart-chain`\n`solana`"
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

    return 'OK', 200
