# LAB7 — Vapor + Fluent + Leaf + Redis

Aplikacja w Vaporze (Swift) wykorzystująca Fluent jako ORM (SQLite),
Leaf jako silnik szablonów oraz Redis jako warstwę cache.

## Uruchomienie lokalne

```bash
cd LAB7
swift run
```

Aplikacja wystartuje na `http://localhost:8080`.

## Endpoints

- `GET /products` — lista produktów (JSON)
- `POST /products` — utworzenie produktu
- `GET /products/:id` — szczegóły produktu
- `PUT /products/:id` — aktualizacja produktu
- `DELETE /products/:id` — usunięcie produktu
