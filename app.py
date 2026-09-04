"""
app.py — запуск для Render.com
Запускает health-сервер и агента в фоновом режиме
"""
import os
import subprocess
import sys
import threading
import time
from flask import Flask

app = Flask(__name__)

def start_agent():
    """Запускает основного агента в фоне"""
    print("[app] 🚀 Запускаю агента...")
    time.sleep(5)
    process = subprocess.Popen(
        [sys.executable, "main.py", "--loop"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Показываем логи в реальном времени
    for line in process.stdout:
        print(f"[agent] {line.rstrip()}")
    
    process.wait()

@app.route("/")
@app.route("/health")
def health():
    return "OK — Telegram News Agent is running", 200

if __name__ == "__main__":
    print("[app] 🟢 Запуск app.py")
    
    # Запускаем агента в фоновом потоке
    thread = threading.Thread(target=start_agent, daemon=True)
    thread.start()
    print("[app] ✅ Агент запущен в фоне")
    
    port = int(os.environ.get("PORT", 10000))
    print(f"[app] 🌐 Запускаю веб-сервер на порту {port}")
    app.run(host="0.0.0.0", port=port)
