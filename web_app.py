from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import requests

app = Flask(__name__)

# Telegram настройки
TOKEN = "8538568514:AAGvZOIUNdfpB788Z2MHhKh2SjU3GarVbUg"
CHAT_ID = "1197635963"

print("\n🔍 ТЕСТ TELEGRAM")
print("="*40)

# Проверяем соединение
try:
    # Проверка бота
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    r = requests.get(url)
    print(f"Статус: {r.status_code}")
    print(f"Ответ: {r.json()}")
    
    # Отправляем тестовое сообщение
    print("\n📤 Отправляю тестовое сообщение...")
    msg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    msg_data = {
        "chat_id": CHAT_ID,
        "text": "🔄 Тест от бота " + str(datetime.now())
    }
    r2 = requests.post(msg_url, data=msg_data)
    print(f"Статус отправки: {r2.status_code}")
    print(f"Ответ отправки: {r2.json()}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("="*40 + "\n")

# Создание БД
conn = sqlite3.connect('bookings.db')
conn.execute('''CREATE TABLE IF NOT EXISTS bookings
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT, phone TEXT, service TEXT,
              date TEXT, time TEXT)''')
conn.close()

@app.route('/')
def home():
    return '''
    <h1>Booking System</h1>
    <form action="/book" method="post">
        Name: <input name="name"><br>
        Phone: <input name="phone"><br>
        <input type="submit" value="Book">
    </form>
    '''

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    phone = request.form['phone']
    
    # Сохраняем
    conn = sqlite3.connect('bookings.db')
    conn.execute("INSERT INTO bookings (name, phone, date, time) VALUES (?, ?, ?, ?)",
                 (name, phone, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M")))
    conn.commit()
    conn.close()
    
    # Отправляем в Telegram
    msg = f"✅ Новая бронь!\nИмя: {name}\nТелефон: {phone}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)
    
    return "Готово! Проверь Telegram!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)