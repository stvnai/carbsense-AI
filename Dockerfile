FROM python:3.12.11-slim

WORKDIR /carbsense

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "--threads", "2", "--preload", "-b", "0.0.0.0:8000", "run:app"]









