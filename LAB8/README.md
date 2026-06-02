# LAB8 — Testy Selenium oraz Playwright dla aplikacji LAB5

Zestaw testów end-to-end pokrywający rejestrację, XSS, koszyk między
kartami, logowanie + podatność CSRF oraz pełny scenariusz E2E w Playwright.

## Struktura

```
LAB8/
├── selenium/        # Python + Selenium WebDriver (zadania 3.0 - 4.5)
└── playwright/      # TypeScript + Playwright (zadanie 5.0)
```

## Uruchomienie testów Selenium

Wymagane: Google Chrome zainstalowany lokalnie (Selenium Manager
sam pobierze odpowiedniego chromedrivera).

Przed uruchomieniem testów uruchom backend oraz frontend aplikacji LAB5:

```bash
# backend
cd LAB5/backend && uv run python main.py

# frontend (w innym terminalu)
cd LAB5/frontend && yarn dev
```

Następnie:

```bash
cd LAB8/selenium
uv sync
uv run pytest -v
```

Domyślnie testy uderzają w `http://localhost:5173` (frontend) i
`http://localhost:8000` (backend). Można nadpisać przez `FRONTEND_URL`
i `BACKEND_URL`.

## Pokrycie

| Plik | Zadanie | Co testuje |
|------|---------|------------|
| `test_registration.py` | 10.3.0 | Walidacja pól obowiązkowych i formatu e-maila w formularzu rejestracji |
| `test_xss.py` | 10.3.5 | Próby wstrzyknięcia XSS - potwierdzają, że React escape'uje wartości w JSX |
| `test_cart_multitab.py` | 10.4.0 | Synchronizacja koszyka między kartami (localStorage + zdarzenie `storage`) |
| `test_csrf.py` | 10.4.5 | Demo podatności CSRF endpointu `/me/email` (brak tokenu CSRF) |
