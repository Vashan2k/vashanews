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
    time.sleep(5)
    subprocess.Popen([sys.executable, "main.py", "--loop"])

@app.route("/")
@app.route("/health")
def health():
    return "OK — Telegram News Agent is running", 200

if __name__ == "__main__":
    threading.Thread(target=start_agent, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)