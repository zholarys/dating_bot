FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip instal --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
