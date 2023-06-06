FROM python:3.7-slim
WORKDIR /app

RUN python -m pip install --upgrade pip

COPY ../ ./

RUN pip3 install -r requirements.txt --no-cache-dir

ENV PYTHONPATH foodgram

CMD gunicorn foodgram.wsgi:application --bind 0:8000
