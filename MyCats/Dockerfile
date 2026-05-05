FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir reqirements.txt

COPY . .

CMD ["sh', '-c', 'python manage.py migrate && gunicorn MyCats.wsgi:application --bind 0.0.0.0:8000"]