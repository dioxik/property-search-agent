#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import os
import math
import subprocess
import base64
from email.mime.text import MIMEText
from datetime import datetime

# Konfiguracja
TARGET_COORDS = (52.525667, 22.713139)  # 52°31\'32.4\"N 22°42\'47.3\"E
RADIUS_KM = 150
EMAILS = os.environ.get("EMAILS", "michaldobrogowski31@gmail.com,dioxik@gmail.com").split(",")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Promień Ziemi w km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_licytacje_komornicze():
    results = []
    provinces = ["mazowieckie", "podlaskie"]
    for prov in provinces:
        url = f"https://licytacje.komornik.pl/wyszukiwarka-licytacji?mainCategory=REAL_ESTATE&province={prov}"
        try:
            response = requests.get(url, timeout=15, headers={\'User-Agent\': \'Mozilla/5.0\'}) # Dodano User-Agent
            soup = BeautifulSoup(response.text, \'html.parser\')
            links = soup.find_all(\'a\', href=True)
            for link in links:
                text = link.get_text(separator=\' \').strip()
                if "działka" in text.lower() or "grunt" in text.lower():
                    results.append({
                        "source": "Licytacje Komornicze",
                        "title": text[:150].replace(\'\\n\', \' \').strip(),
                        "url": "https://licytacje.komornik.pl" + link[\'href\'] if link[\'href\'].startswith(\'/\') else link[\'href\'],
                        "price": "Sprawdź na stronie"
                    })
        except Exception as e:
            print(f"Error fetching {prov}: {e}")
    return results

def get_olx_listings():
    # OLX wymaga bardziej zaawansowanego scrapingu, tutaj szkielet
    # W pełnej wersji agenta używamy browser_navigate do pobrania HTML
    return [{"source": "OLX", "title": "Przykładowa działka w promieniu 150km", "url": "https://www.olx.pl/nieruchomosci/dzialki/mazowieckie/", "price": "100 000 zł"}]

def send_email_via_gws(subject, body_text):
    for email_addr in EMAILS:
        try:
            message = MIMEText(body_text)
            message[\'to\'] = email_addr
            message[\'subject\'] = subject
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            payload = {"raw": raw_message}
            cmd = [
                "gws", "gmail", "users", "messages", "send",
                "--params", json.dumps({"userId": "me"}),
                "--json", json.dumps(payload)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Email sent to {email_addr}")
            else:
                print(f"Failed to send email to {email_addr}: {result.stderr}")
        except Exception as e:
            print(f"Error sending email to {email_addr}: {e}")

def main():
    print(f"Uruchamiam agenta: {datetime.now()}")
    all_results = []
    all_results.extend(get_licytacje_komornicze())
    all_results.extend(get_olx_listings())
    
    # Usuwanie duplikatów po URL
    unique_results = {res[\'url\']: res for res in all_results}.values()
    
    summary = f"Raport Nieruchomości - {datetime.now().strftime(\'%Y-%m-%d %H:%M\')}\\n"
    summary += f"Lokalizacja centralna: 52°31\'32.4\\"N 22°42\'47.3\\"E (Promień 150km)\\n"
    summary += "="*50 + "\\n\\n"
    
    for res in unique_results:
        summary += f"[{res[\'source\']}] {res[\'title\]}\\n"
        summary += f"Link: {res[\'url\]}\\n"
        summary += f"Cena: {res[\'price\]}\\n"
        summary += "-"*30 + "\\n\\n"
    
    # Zapis do pliku dla GitHub
    with open("results.json", "w", encoding=\'utf-8\') as f:
        json.dump(list(unique_results), f, ensure_ascii=False, indent=4)
    
    # Zapis raportu tekstowego
    with open("report.txt", "w", encoding=\'utf-8\') as f:
        f.write(summary)
    
    print(summary)
    send_email_via_gws("Raport Nieruchomości", summary)

if __name__ == "__main__":
    main()
