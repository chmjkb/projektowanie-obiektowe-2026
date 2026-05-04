from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="LAB5 Backend")


class Product(BaseModel):
    id: int
    name: str
    price: float


class PaymentItem(BaseModel):
    product_id: int
    quantity: int


class Payment(BaseModel):
    customer_name: str
    items: list[PaymentItem]
    total: float


PRODUCTS: list[Product] = [
    Product(id=1, name="Kawa", price=12.50),
    Product(id=2, name="Herbata", price=8.00),
    Product(id=3, name="Ciastko", price=5.50),
    Product(id=4, name="Kanapka", price=15.00),
    Product(id=5, name="Sok pomarańczowy", price=9.00),
]

PAYMENTS: list[Payment] = []


@app.get("/products", response_model=list[Product])
def list_products() -> list[Product]:
    return PRODUCTS


@app.post("/payments", response_model=Payment)
def create_payment(payment: Payment) -> Payment:
    PAYMENTS.append(payment)
    return payment


@app.get("/payments", response_model=list[Payment])
def list_payments() -> list[Payment]:
    return PAYMENTS


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
