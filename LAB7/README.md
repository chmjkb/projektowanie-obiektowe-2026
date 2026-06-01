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

## Deployment na Heroku

Pliki konfiguracyjne:

- `Procfile` — komenda startowa dla dyno `web`
- `.swift-version` — wersja Swifta dla buildpacka
- `app.json` — manifest aplikacji (buildpack `vapor-community/heroku-buildpack`,
  addon `heroku-redis:mini`)

Kroki deploymentu (z poziomu katalogu `LAB7/`):

```bash
heroku create lab7-vapor --stack heroku-22 \
  --buildpack https://github.com/vapor-community/heroku-buildpack
heroku addons:create heroku-redis:mini
git subtree push --prefix LAB7 heroku main
heroku ps:scale web=1
heroku open
```

> **Uwaga:** SQLite działa na efemerycznym dysku dyno - dane przepadają
> przy każdym restarcie. Dla realnej produkcji należy dodać addon
> `heroku-postgresql` oraz `FluentPostgresDriver` i przełączyć
> `configure.swift` na sterownik Postgres, gdy obecna jest zmienna
> `DATABASE_URL`.
