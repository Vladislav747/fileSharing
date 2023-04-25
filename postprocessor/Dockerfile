FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -U --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "main.py"]