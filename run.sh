#!/bin/bash


# 1️⃣ Proje root klasörüne git
cd "$(dirname "$0")/API" || exit

# 2️⃣ FastAPI server'ı arka planda başlat
# Windows için start kullanıyoruz
echo "Starting FastAPI server..."
start "" python -m uvicorn LoginApi:app --reload --port 8001
start "" python -m uvicorn MentorApi:app --reload --port 8000
start "" python -m uvicorn InterviewsApi:app --reload --port 8002

# 3️⃣ Server'ın açılmasını biraz bekle
sleep 3

# 4️⃣ PyQt GUI scriptini çalıştır
cd ..
echo "Starting PyQt application..."
python main.py
