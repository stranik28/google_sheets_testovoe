# google_sheets_testovoe

1. Запуск осуществляется через docker-compose Linux(docker-compose up --build) </br>
2. Бэкенд хостится на порту  8000 </br>
3. Postgres поднимается на 5433(для внешнего подключения) </br>
4. Что бы получить доступ к телеграмм боту нужно отправить из нужного чата /start (о просроченных поствках бот сообщает каждый день в 1:21(можно поменять)  бот(https://t.me/carl_my_bot) </br>
5. Google sheets для которого настроена программа(https://docs.google.com/spreadsheets/d/15zTJUSn4KSDwgF5TsRyZuR-PTm8sr9Bj6Tj9u6TcOo4/edit?usp=sharing) </br>

<b>Коментарии  решению</b>
1. Время выполнения ~ 4-5 часов </br>
2. Курс доллара берется по курсу дня добваления </br>
3. Ссылка на документацию бека http://0.0.0.0:8000/docs#/ </br>
4. Данные их Google sheets обновляются каждые 10 секунд </br>
5. Некоректно введенные строки, могут не вноситься/не обновляться в базе данных, пока не будут коректными </br>
