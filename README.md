# Property Search Agent 🏠🔍

Autonomiczny agent Python do wyszukiwania działek i nieruchomości w promieniu 150 km od punktu **52°31'32.4"N 22°42'47.3"E**.

## Funkcje
- 🕒 **Harmonogram**: Działa 2 razy dziennie (8:00 i 18:00 UTC) za pomocą crona w kontenerze Docker.
- 🌐 **Źródła**: Przeszukuje licytacje komornicze (mazowieckie, podlaskie), OLX i inne.
- 📧 **Powiadomienia**: Wysyła podsumowanie na e-mail (wymaga konfiguracji GWS).
- 📂 **Wyniki**: Publikuje najnowsze znaleziska w plikach `results.json` i `report.txt`.

## Konfiguracja Docker Compose

1.  **Sklonuj repozytorium**:
    ```bash
    git clone https://github.com/dioxik/property-search-agent.git
    cd property-search-agent
    ```

2.  **Utwórz plik `.env`** (w tym samym katalogu co `docker-compose.yml`) i dodaj zmienne środowiskowe:
    ```
    GWS_TOKEN=TwojTokenGWS
    EMAILS=michaldobrogowski31@gmail.com,dioxik@gmail.com
    ```
    *   `GWS_TOKEN`: Token autoryzacyjny dla Google Workspace CLI (gws). Aby go uzyskać, musisz skonfigurować `gws` CLI lokalnie i autoryzować dostęp do Gmaila. Następnie możesz użyć `gws auth print-access-token` lub podobnej metody, aby uzyskać token. **Pamiętaj, aby chronić ten token!**
    *   `EMAILS`: Lista adresów e-mail oddzielonych przecinkami, na które będą wysyłane raporty.

3.  **Uruchom kontener Docker Compose**:
    ```bash
    docker-compose up --build -d
    ```
    Agent będzie działał w tle i uruchamiał się automatycznie o 8:00 i 18:00 UTC.

4.  **Sprawdź logi**:
    ```bash
    docker-compose logs -f property-agent
    ```

## Lokalizacja centralna
- Współrzędne: 52.525667, 22.713139
- Promień: 150 km

## Autor
Agent stworzony przez Manus AI na zlecenie użytkownika.
