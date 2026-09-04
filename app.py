import os
import subprocess
import sys
import threading
import time
from flask import Flask

app = Flask(__name__)

def start_agent():
    """Запускает агента и показывает ВСЕ ошибки в логах"""
    print("[app] 🚀 Запускаю агента...")
    time.sleep(3)
    
    # Запускаем агента с принудительным выводом ВСЕГО
    process = subprocess.Popen(
        [sys.executable, "-u", "main.py", "--loop"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    print("[app] ✅ Агент запущен, читаю логи...")
    
    # ВЫВОДИМ ВСЁ, ЧТО ПРИХОДИТ (включая ошибки)
    for line in iter(process.stdout.readline, ''):
        print(f"[agent] {line.rstrip()}")
        sys.stdout.flush()
    
    # Если процесс упал — покажем это
    return_code = process.wait()
    if return_code != 0:
        print(f"[app] ❌ Агент завершился с ошибкой (код {return_code})")

@app.route("/")
@app.route("/health")
def health():
    return "OK — Telegram News Agent is running", 200

if __name__ == "__main__":
    print("[app] 🟢 Запуск app.py")
    
    # Запускаем агента в фоновом потоке
    thread = threading.Thread(target=start_agent, daemon=True)
    thread.start()
    time.sleep(1)
    print("[app] ✅ Агент запущен в фоне")
    
    port = int(os.environ.get("PORT", 10000))
    print(f"[app] 🌐 Запускаю веб-сервер на порту {port}")
    app.run(host="0.0.0.0", port=port)
