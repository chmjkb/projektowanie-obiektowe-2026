# LAB7 — Vapor + Fluent + Leaf + Redis

Aplikacja w Vaporze (Swift) wykorzystująca Fluent (SQLite) jako ORM,
Leaf jako silnik szablonów oraz Redis jako warstwę cache dla listy produktów.

## Wymagania

- Swift 5.9+ (testowane na 6.3)
- Redis (lokalnie domyślnie `redis://localhost:6379`)

```bash
brew install redis
brew services start redis    # lub: redis-server --daemonize yes
```

Adres Redisa można nadpisać zmienną `REDIS_URL`. Aplikacja działa też
bez Redisa — wywołania cache są opakowane w `try?`, więc cache miss
po prostu trafia do bazy.

## Uruchomienie lokalne

```bash
cd LAB7
swift run
```

Aplikacja wystartuje na `http://localhost:8080`.

## Endpoints

- `GET /` — strona główna
- `GET /products`, `/products/new`, `/products/:id`, `/products/:id/edit`
  oraz `POST /products`, `POST /products/:id`, `POST /products/:id/delete`
- `GET /categories`, analogicznie

Lista produktów jest cache'owana w Redisie na 60s i automatycznie
unieważniana przy create / update / delete.
