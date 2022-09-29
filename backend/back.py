from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sheet import Orders, session
from sqlalchemy.sql import func


class OrderSchema(BaseModel):
    id: int
    order_numb: int
    price_usd: float
    price_rub: float
    date: datetime

app = FastAPI(
    title="Sales sheet",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/all")
def all():
    '''Вывод всех заказов'''
    all = session.query(Orders).all()
    return all

@app.get("/summary_rub")
def recoginze_rub():
    '''Вывод суммы всех заказов в рублях'''
    summary = round((session.query(func.sum(Orders.price_rub)).scalar()),2)
    return {"Summary":summary}

@app.get("/summary_usd")
def recoginze_usd():
    '''Вывод суммы всех заказов в долларах'''
    summary = round((session.query(func.sum(Orders.price_usd)).scalar()),2)
    return {"Summary":summary}