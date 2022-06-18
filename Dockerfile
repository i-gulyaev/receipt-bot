FROM python:3.10

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf requirements.txt

COPY ./app /app

ENV PYTHONPATH=/app

CMD ["python", "-m", "app.bot"]
