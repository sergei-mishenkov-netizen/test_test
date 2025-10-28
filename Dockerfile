# Dockerfile для игры про шарики с поддержкой GUI
FROM python:3.11-slim

# Установка системных зависимостей для Pygame и X11
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    python3-dev \
    # Зависимости для X11
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY requirements.txt .
COPY logic.py .
COPY game_gui.py .
COPY gui.py .
COPY config.py .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Переменные окружения для Pygame и X11
ENV SDL_VIDEODRIVER=x11
ENV DISPLAY=:0
ENV PYTHONUNBUFFERED=1

# Делаем gui.py исполняемым
RUN chmod +x gui.py

# Точка входа - запуск игры через gui.py
CMD ["python3", "gui.py"]

