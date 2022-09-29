from sqlalchemy import Integer, \
    Column, DateTime, Numeric, create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from starlette.config import Config
from sqlalchemy.orm import Session

config = Config(".env")

Base = declarative_base()

engine = create_engine("postgresql+psycopg2://{}:{}@db:5432/{}".format(
    config("POSTGRES_USER"),
    config("POSTGRES_PASSWORD"),
    config("POSTGRES_DB")
))

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_numb = Column(Integer)
    price_usd = Column(Numeric)
    price_rub = Column(Numeric)
    date = Column(DateTime)

Base.metadata.create_all(engine)

session = Session(bind=engine)

# print(session.query(Orders).all())




