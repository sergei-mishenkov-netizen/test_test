# Dockerfile для игры про шарики
FROM python:3.11-slim

# Установка системных зависимостей для Pygame
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов
COPY requirements.txt .
COPY logic.py .
COPY game_gui.py .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# По умолчанию запускаем тестирование логики (т.к. GUI требует X11)
CMD ["python", "logic.py"]

