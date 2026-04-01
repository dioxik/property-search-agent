FROM python:3.11-slim-buster

WORKDIR /app

# Instalacja crona i zależności
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ustawienie crona
RUN echo "0 8,18 * * * python /app/agent.py >> /var/log/cron.log 2>&1" | crontab -

# Uruchomienie crona i agenta
CMD ["cron", "-f"]
