# базовый образ
FROM python:3.11

# рабочая папка
WORKDIR /app

# копируем зависимости
COPY requirements.txt .

# устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# копируем проект
COPY . .

# команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]