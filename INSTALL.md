# Инструкция по установке и запуску

## Быстрый старт

### 1. Установка Pygame

Установите Pygame одной командой:

```bash
pip3 install pygame
```

Или используйте файл requirements.txt:

```bash
pip3 install -r requirements.txt
```

### 2. Проверка установки

Убедитесь, что Pygame установлен:

```bash
python3 -c "import pygame; print('Pygame версия:', pygame.version.ver)"
```

### 3. Запуск игры

```bash
python3 game_gui.py
```

## Возможные проблемы

### Проблема: ModuleNotFoundError: No module named 'pygame'

**Решение:**
```bash
pip3 install pygame
```

### Проблема: Игра не запускается в виртуальной среде

**Решение:** Создайте и активируйте виртуальное окружение:

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация (macOS/Linux)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск игры
python game_gui.py
```

### Проблема: Низкая производительность

**Решение:** Уменьшите количество начальных шариков в файле `game_gui.py`:

```python
INITIAL_BALLS_COUNT = 5  # Вместо 10
```

## Системные требования

- **Python:** 3.7 или выше
- **ОС:** Windows, macOS, Linux
- **Pygame:** 2.0 или выше
- **Память:** 100+ MB RAM
- **Процессор:** Любой современный процессор

## Дополнительные команды

### Только тестирование логики (без GUI)

```bash
python3 logic.py
```

Эта команда запустит демонстрацию игровой логики в консоли без графического интерфейса.

### Проверка зависимостей

```bash
pip3 list | grep pygame
```

## Docker (опционально)

Если у вас установлен Docker, вы можете использовать Dockerfile:

```bash
docker build -t ball-game .
docker run ball-game
```

*Примечание: Для работы GUI в Docker могут потребоваться дополнительные настройки X11.*

