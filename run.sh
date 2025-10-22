#!/bin/bash


# 1️⃣ Proje root klasörüne git
cd "$(dirname "$0")/backend" || exit

pip install --no-cache-dir sqlalchemy-utils

# 2️⃣ FastAPI server'ı arka planda başlat
# Windows için start kullanıyoruz
echo "Starting FastAPI server..."
start "" python -m uvicorn run_all:app --reload --port 8000

# 3️⃣ Server'ın açılmasını biraz bekle
sleep 15

# 4️⃣ PyQt GUI scriptini çalıştır
cd ../frontend || exit
echo "Starting PyQt application..."
python main.py
