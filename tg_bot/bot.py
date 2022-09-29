import asyncio
import aioschedule
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram import Dispatcher, types
from sheet import session, Orders
import datetime
from starlette.config import Config

config = Config(".env")
bot = Bot(token=config("TELEGRAM_TOKEN"))

dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
chats = []

# Добавление чата в список  
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chats.append(message.chat.id)
    await bot.send_message(message.chat.id, "Ваш чат успешно добавлен в список рассылки")

# Отправка сообщения всем пользователям из списка
@dp.message_handler()
async def choose_your_dinner():
    orders = session.query(Orders).filter(Orders.date < datetime.date.today()).all()
    orders_id = [("Номер заказа : "+ str(order.order_numb)) for order in orders]
    for user in set(chats):
        await bot.send_message(chat_id = user, text = "Хей🖖 кажется пропущены следующие заказы: {}".format(orders_id))

# Запуск рассылки
async def scheduler():
    aioschedule.every().day.at("01:21").do(choose_your_dinner)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(dp): 
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp,on_startup=on_startup)