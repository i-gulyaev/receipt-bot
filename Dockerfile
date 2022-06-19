FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

RUN mkdir /build
COPY . /build

RUN python3 -m pip install --upgrade pip build \
    && python3 -m pip install /build \
    && rm -rf /build

CMD ["python", "-m", "receipt_bot.bot"]
