FROM python:3.12

RUN python --version

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    --no-cache-dir \
    --prefer-binary \
    --index-url https://pypi.org/simple/ \
    --trusted-host pypi.org

COPY . .

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
