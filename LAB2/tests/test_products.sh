#!/bin/bash

BASE_URL="${BASE_URL:-http://localhost:8000}/api/products"

echo "=== Testowanie endpointów Product ==="

echo ""
echo "--- POST /api/products (Tworzenie) ---"
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 2999.99, "description": "Wydajny laptop do pracy"}')
echo "$CREATE_RESPONSE"

PRODUCT_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "Utworzony produkt ID: $PRODUCT_ID"

echo ""
echo "--- POST /api/products (Drugi produkt) ---"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mysz bezprzewodowa", "price": 149.99}'

echo ""
echo ""
echo "--- GET /api/products (Lista wszystkich) ---"
curl -s -X GET "$BASE_URL"

echo ""
echo ""
echo "--- GET /api/products/$PRODUCT_ID (Pojedynczy produkt) ---"
curl -s -X GET "$BASE_URL/$PRODUCT_ID"

echo ""
echo ""
echo "--- PUT /api/products/$PRODUCT_ID (Aktualizacja) ---"
curl -s -X PUT "$BASE_URL/$PRODUCT_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Pro", "price": 3499.99, "description": "Zaktualizowany opis"}'

echo ""
echo ""
echo "--- GET /api/products/$PRODUCT_ID (Po aktualizacji) ---"
curl -s -X GET "$BASE_URL/$PRODUCT_ID"

echo ""
echo ""
echo "--- DELETE /api/products/$PRODUCT_ID (Usuwanie) ---"
curl -s -X DELETE "$BASE_URL/$PRODUCT_ID"

echo ""
echo ""
echo "--- GET /api/products (Po usunięciu) ---"
curl -s -X GET "$BASE_URL"

echo ""
echo ""
echo "--- GET /api/products/9999 (Nieistniejący produkt - oczekiwany błąd 404) ---"
curl -s -X GET "$BASE_URL/9999"

echo ""
echo ""
echo "=== Testy zakończone ==="
