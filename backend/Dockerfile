FROM python:3.8-slim AS compile-image

RUN apt-get update && \
    apt-get install -y --no-install-recommends

WORKDIR /backend
COPY . /backend

RUN pip install --upgrade pip &&  \
    pip install -r requirements.txt
    
CMD ["uvicorn", "back:app", "--host", "0.0.0.0", "--port", "8000"]