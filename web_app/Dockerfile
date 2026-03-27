FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
WORKDIR /app/backend
CMD gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:${PORT:-8080} server:app
