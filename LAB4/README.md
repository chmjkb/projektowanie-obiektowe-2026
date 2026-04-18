# LAB4 - Weather API

## Run

```bash
go run main.go
```

Server starts on `http://localhost:8080`

## Endpoints

Get weather for a city:
```bash
curl "http://localhost:8080/weather?city=Warsaw"
```

Get weather for all cities:
```bash
curl "http://localhost:8080/weather/all"
```

## Available cities

Warsaw, Krakow, Gdansk, Wroclaw, Poznan
