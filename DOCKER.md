# 🐳 Запуск игры в Docker

Это руководство описывает, как запустить игру про шарики в Docker-контейнере с полной поддержкой графического интерфейса.

---

## Быстрый старт

### 1️⃣ Сборка образа

```bash
docker build -t ball-game .
```

### 2️⃣ Запуск (автоматический)

Используйте скрипт, который автоматически определит вашу платформу:

```bash
./run-docker.sh
```

**Или** используйте Docker Compose:

```bash
docker-compose up
```

---

## Подробные инструкции для разных платформ

### 🍎 macOS

#### Требования
- Docker Desktop
- XQuartz (X11 сервер для macOS)

#### Установка XQuartz

```bash
brew install --cask xquartz
```

После установки:
1. Запустите XQuartz
2. Откройте Настройки XQuartz → Безопасность
3. Включите "Разрешить соединения от сетевых клиентов"
4. Перезапустите Mac (или выйдите и войдите снова)

#### Запуск игры

```bash
# Разрешите подключение к X11
xhost + localhost

# Соберите образ
docker build -t ball-game .

# Запустите контейнер
docker run -it --rm \
  -e DISPLAY=host.docker.internal:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ball-game
```

#### Автоматический запуск

```bash
./run-docker.sh
```

---

### 🐧 Linux

#### Требования
- Docker
- X11 (обычно уже установлен)

#### Запуск игры

```bash
# Разрешите Docker подключаться к X11
xhost +local:docker

# Соберите образ
docker build -t ball-game .

# Запустите контейнер
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --net=host \
  ball-game

# После завершения (опционально)
xhost -local:docker
```

#### Автоматический запуск

```bash
./run-docker.sh
```

---

### 🪟 Windows (WSL2)

#### Требования
- Docker Desktop с WSL2 backend
- X-сервер для Windows (VcXsrv или Xming)

#### Установка VcXsrv

1. Скачайте и установите [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Запустите XLaunch
3. Выберите "Multiple windows"
4. Выберите "Start no client"
5. **ВАЖНО**: Отметьте "Disable access control"
6. Сохраните конфигурацию для будущих запусков

#### Запуск игры

```bash
# В WSL2 терминале

# Получите IP адрес хоста WSL
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

# Соберите образ
docker build -t ball-game .

# Запустите контейнер
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  ball-game
```

#### Автоматический запуск

```bash
./run-docker.sh
```

#### Альтернатива: Xming

Если используете Xming:
1. Установите [Xming](https://sourceforge.net/projects/xming/)
2. Запустите Xming
3. Используйте те же команды, что и для VcXsrv

---

## Docker Compose

Для упрощенного управления используйте Docker Compose.

### Файл docker-compose.yml уже создан

```bash
# Сборка и запуск
docker-compose up

# Запуск в фоновом режиме
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Пересборка
docker-compose up --build
```

---

## Структура Dockerfile

### Что включено:

1. **Базовый образ**: Python 3.11 slim
2. **Системные библиотеки**:
   - SDL2 (для Pygame)
   - X11 (для графического вывода)
   - Xvfb (виртуальный framebuffer, опционально)
3. **Python зависимости**: Pygame 2.5.2+
4. **Файлы проекта**: logic.py, game_gui.py, gui.py, config.py
5. **Переменные окружения**:
   - `SDL_VIDEODRIVER=x11`
   - `DISPLAY=:0`
   - `PYTHONUNBUFFERED=1`

### Точка входа

По умолчанию запускается `gui.py`, который:
- Выводит инструкции в консоль
- Запускает графическое окно игры
- Обрабатывает ошибки с понятными сообщениями

---

## Решение проблем

### Проблема: "cannot open display"

**Причина**: Контейнер не может подключиться к X-серверу

**Решение для macOS**:
```bash
# Проверьте, запущен ли XQuartz
ps aux | grep XQuartz

# Перезапустите XQuartz
killall XQuartz
open -a XQuartz

# Разрешите подключения
xhost + localhost
```

**Решение для Linux**:
```bash
# Разрешите подключение
xhost +local:docker

# Проверьте переменную DISPLAY
echo $DISPLAY
```

**Решение для Windows/WSL2**:
```bash
# Убедитесь, что VcXsrv запущен
# Проверьте DISPLAY
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
echo $DISPLAY
```

---

### Проблема: Черный экран или зависание

**Решение**:
```bash
# Остановите все контейнеры
docker stop $(docker ps -aq)

# Очистите
docker system prune -f

# Пересоберите образ
docker build --no-cache -t ball-game .
```

---

### Проблема: Медленная работа в контейнере

**Причина**: Ограничения производительности при работе через X11

**Решение**:
- Уменьшите количество шариков в `config.py` (INITIAL_BALLS_COUNT)
- Уменьшите FPS (например, до 30)
- Рассмотрите запуск игры напрямую на хосте

---

### Проблема: Права доступа к X11

**Для Linux**:
```bash
# Временное решение
xhost +

# После работы верните ограничения
xhost -
```

**Безопасное решение**:
```bash
# Только для локальных подключений Docker
xhost +local:docker
```

---

## Запуск без GUI (только логика)

Если GUI не работает, можете запустить демонстрацию логики:

```bash
docker run -it --rm ball-game python3 logic.py
```

Или интерактивные примеры:

```bash
docker run -it --rm ball-game python3 examples.py
```

---

## Очистка

### Удалить образ

```bash
docker rmi ball-game
```

### Удалить все неиспользуемые данные

```bash
docker system prune -a
```

---

## Дополнительные опции

### Запуск с измененной конфигурацией

Создайте свой `config.py` и смонтируйте его:

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/my-config.py:/app/config.py \
  ball-game
```

### Запуск с сохранением логов

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/logs:/app/logs \
  ball-game 2>&1 | tee game.log
```

---

## Производительность

### Ожидаемые характеристики в Docker:

- **FPS**: 45-60 (зависит от системы)
- **Задержка**: ~10-30ms (через X11)
- **Рекомендуемое количество шариков**: 10-15

### Для максимальной производительности:

Запускайте игру напрямую на хосте:
```bash
python3 gui.py
```

---

## Полезные команды

```bash
# Просмотр логов контейнера
docker logs ball-game

# Войти в запущенный контейнер
docker exec -it ball-game bash

# Проверить использование ресурсов
docker stats ball-game

# Список запущенных контейнеров
docker ps

# Остановить контейнер
docker stop ball-game
```

---

## Заключение

Docker позволяет запустить игру в изолированной среде, но для полной производительности и лучшего опыта рекомендуется запуск напрямую на хосте.

**Рекомендуемый порядок**:
1. Попробуйте `python3 gui.py` на хосте
2. Если нужна изоляция, используйте `./run-docker.sh`
3. Для сложных сценариев используйте `docker-compose`

---

Последнее обновление: 27 октября 2025

