import hashlib
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="LAB5 Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str
    email: str


class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str


PRODUCTS: list[Product] = [
    Product(id=1, name="Kawa", price=12.50),
    Product(id=2, name="Herbata", price=8.00),
    Product(id=3, name="Ciastko", price=5.50),
    Product(id=4, name="Kanapka", price=15.00),
    Product(id=5, name="Sok pomarańczowy", price=9.00),
]

PAYMENTS: list[Payment] = []
USERS: list[User] = []

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


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


@app.post("/register", response_model=UserOut, status_code=201)
def register(req: RegisterRequest) -> UserOut:
    if not EMAIL_REGEX.match(req.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if any(u.username == req.username for u in USERS):
        raise HTTPException(status_code=409, detail="Username already exists")
    if any(u.email == req.email for u in USERS):
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        id=len(USERS) + 1,
        username=req.username,
        email=req.email,
        password_hash=hashlib.sha256(req.password.encode()).hexdigest(),
    )
    USERS.append(user)
    return UserOut(id=user.id, username=user.username, email=user.email)


@app.get("/users", response_model=list[UserOut])
def list_users() -> list[UserOut]:
    return [UserOut(id=u.id, username=u.username, email=u.email) for u in USERS]


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
