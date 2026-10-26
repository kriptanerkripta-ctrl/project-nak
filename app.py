import os
import requests
from flask import Flask, jsonify, render_template_string, request
from yookassa import Configuration, Payment

app = Flask(__name__)

# Настройка ключей доступа
REPLICATE_API_TOKEN = "r8_9v2R81omNH8OeYiUYGKnSDc3izXmK4T2bJtxt"

# Настройка ЮKassa
Configuration.account_id = "1504768"
Configuration.secret_key = "Live_hQMZagCPNRrDPrsmDwbtbbV3nY6IxSkC1pevtwEOSJs"

# Простой шаблон интерфейса (Project Nak)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Project Nak 🚀</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; text-align: center; padding: 50px; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: inline-block; }
        button { background: #6772e5; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 6px; cursor: pointer; }
        button:hover { background: #5469d4; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Project Nak 🚀</h1>
        <p>AI-Конструктор карточек для Wildberries и Ozon</p>
        <form action="/create-payment" method="POST">
            <button type="submit">Оплатить генерацию (100 ₽) ⭐</button>
        </form>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
  return render_template_string(HTML_TEMPLATE)


@app.route("/create-payment", methods=["POST"])
def create_payment():
  try:
    # Создание платежа через ЮKassa
    payment = Payment.create({
        "amount": {"value": "100.00", "currency": "RUB"},
        "confirmation": {
            "type": "redirect",
            "return_url": request.host_url,
        },
        "capture": True,
        "description": "Генерация инфографики Project Nak",
    })
    # Перенаправление пользователя на страницу оплаты ЮKassa
    return jsonify({"confirmation_url": payment.confirmation.confirmation_url})
  except Exception as e:
    return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
