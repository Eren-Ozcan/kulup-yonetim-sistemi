# Python tabanlı bir imaj kullan
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli sistem bağımlılıklarını yükle
# 'libpq-dev' PostgreSQL bağlantısı için gerekli
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Gereksinimler dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Cloud Run için gerekli portu aç
EXPOSE 8080

# Giriş noktasını belirt (Flask uygulamasını çalıştır)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
