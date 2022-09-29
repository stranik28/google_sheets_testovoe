FROM python:3.8-slim AS compile-image

RUN apt-get update && \
    apt-get install -y --no-install-recommends

WORKDIR /bot
COPY . /bot

RUN pip install --upgrade pip &&  \
    pip install -r requirements.txt

CMD [ "python3", "bot.py" ]