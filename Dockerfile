FROM python:3.12-slim
LABEL authors="Shebik"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get -y update; apt-get -y install curl
RUN apt-get -y install unzip;
RUN curl -fsSL https://deno.land/install.sh | sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN alembic upgrade head

RUN mkdir -p res
RUN mkdir -p res/yt-dir
RUN mkdir -p logs

CMD ["python", "bot.py"]
