from time import sleep
import gspread
import requests
from sheet import session,Orders
from datetime import datetime,date
from starlette.config import Config

config = Config(".env")


gs = gspread.service_account(filename='credits.json')  # подключаем файл с ключами и пр.
sh = gs.open_by_key(config("SHEETS_ID"))  # подключаем таблицу по ID
worksheet = sh.sheet1  # получаем первый 

# получаем данные из таблицы
prev = worksheet.get_all_records()
# Получаем сегодняшнюю дату
last_know_day = date.today().day

# получаем курс доллара
def get_course():
    date = datetime.now().strftime("%d.%m.%Y")
    req = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date))
    for i in req.text.split('<Valute ID="R01235">'):
        if i.find('USD') != -1:
            course = float(i.split('<Value>')[1].split('</Value>')[0].replace(',', '.'))  # получаем курс доллара
    return course

# Хранение курса доллара
course = get_course()

# Обновляем Базу данных
def update_records(records):
    for i in records:
        format = '%d.%m.%Y'
        # Пробуем преобразовать дату в формат datetime
        try:
            date_elem = None if len(i['срок поставки'].split(".")) < 3\
                 else datetime.strptime(i['срок поставки'], format) 
        except:
            print("Ошибка в дате")
            date_elem = None

        price_rub = 0
        # Переводим цену из долларов в рубли
        if (date_elem is not None) and str(i['стоимость,$']).isdigit():
            price_rub = float(i['стоимость,$'])* course
        else:
            price_rub = None
        # Пробуем получить запись из БД
        try:
            record = session.query(Orders).filter(Orders.id == i['№']).first()
        except Exception as e:
            print("Ошибка в id" + str(e))
            session.rollback()
            record = None
        # Если записи нет, то создаем ее
        if record is None:
            print("Добавляем запись")
            # Создаем образ записи
            record = Orders(
                id = i['№'],
                order_numb=i['заказ №'],
                price_usd=i['стоимость,$'],
                price_rub=price_rub,
                date=date_elem
            )
            # Добавляем запись в БД
            try:
                session.add(record)
                session.commit()
                print("Запись добавлена")
            except(Exception) as e:
                session.rollback()
                print('Ошибка записи в БД' + str(e))
                print(record)
        # Если запись есть, то обновляем ее
        else:
            print("Обновляем запись")
            # Обновляем запись
            record.order_numb = i['заказ №']
            record.price_usd = i['стоимость,$']
            record.price_rub = price_rub
            record.date = date_elem
            # Сохраняем изменения
            try:
                session.commit()
                print("Запись обновлена")
            except:
                session.rollback()
                print("Ошибка при обновлении записи")

print("Update db...")
update_records(prev)
print("Update db...OK")

while True:
    # Получаем сегоднящнюю дату и проверяем не изменилась ли она
    today = date.today().day
    if today != last_know_day:
        # Обновляем курс доллара
        course = get_course()
    # Обновляем текущую дату
    last_know_day = today

    print("New round")
    # Получаем данные из таблицы
    current = worksheet.get_all_records()
    # Массив для хранения изменений
    changed_rows = []
    # Получаем размеры массивов
    current_len =len(current)
    prev_len = len(prev)
    # Получаем длину наибольшего массива
    end = max(current_len, prev_len)
    i = 0
    # Перебираем массивы
    while i < end:

        end = max(current_len, prev_len)
        current_len =len(current)
        prev_len = len(prev)
        # Проверка корректности id введенного опльзователем в текущей записи
        first = True
        try:
            if str(current[i]['№']).isdigit():
                first = True
            else:
                first = False
        except:
            first = True
        # Проверка корректности id введенного опльзователем в прошлой записи
        second = True
        try:
            if str(prev[i]['№']).isdigit():
                second = True
            else:
                second = False
        except:
            second = True
        # Если id введен корректно, то проверяем наличие изменений, если нет , то переходим к следующей записи
        if not (first and second):
            print("Index error")
            i+=1
            continue
        # Проверяем не вышли ли мы за пределы массива
        if i < min(current_len, prev_len):
            # Проверяем равны ли записи
            if current[i] != prev[i]:
                # Проверяем не удалил ли пользователь запись
                if int(current[i]['№']) != int(prev[i]['№']):
                    print("Delete")
                    # Удаляем запись из БД
                    session.query(Orders).filter(Orders.id == prev[i]['№']).delete()
                    session.commit()
                    prev.pop(i)
                    continue
                # Если запись не удалил, то добавляем ее в массив изменений
                else:
                    changed_rows.append(current[i])
                    print("Changed")
        # Проверем не удалил ли пользователь еще записи
        elif prev_len > current_len:
            print("Delete")
            session.query(Orders).filter(Orders.id == prev[i]['№']).delete()
            session.commit()
            prev.pop(i)
            continue
        elif current_len  == prev_len:
            i+=1
            continue
        # Если размер нового массива больше, то добавляем новые записи в БД
        else:
            print("Add")
            changed_rows.append(current[i])
        i+=1
    # print(changed_rows)
    # Обновляем массив с прошлыми записями
    update_records(changed_rows)
    # Обновляем массив с прошлыми записями
    prev = current
    # Засыпаем на 10 секунд
    sleep(10)