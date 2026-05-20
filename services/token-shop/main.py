import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Token Shop Services")

# Tokens awarded per unit of money spent
token_price: int = 10

# stores purchases: code -> {money: int, used: bool}
purchases: dict[str, dict] = {}


class BuyRequest(BaseModel):
    username: str
    money: int


class RedeemRequest(BaseModel):
    code: str


class PriceUpdate(BaseModel):
    price: int


@app.post("/buy")
def buy(body: BuyRequest):
    """Issue a unique secret code representing a purchase."""
    code = str(uuid.uuid4())
    purchases[code] = {"money": body.money, "used": False}
    return {"secret":  code}


@app.post("/redeem")
def redeem(body: RedeemRequest):
    """Validate a code and return how many tokens to award. Marks code as used."""
    purchase = purchases.get(body.code)
    if not purchase:
        raise HTTPException(status_code=404, detail="Code not found")
    if purchase["used"]:
        raise HTTPException(status_code=400, detail="Code already used")
    purchase["used"] = True
    return {"tokens": purchase["money"] * token_price}


@app.get("/price")
def get_price():
    """Return the current token price (tokens per unit of money)."""
    return {"price": token_price}


@app.put("/price")
def set_price(body: PriceUpdate):
    """Update the token price (admin only)"""
    global token_price
    token_price = body.price
    return {"price": token_price}