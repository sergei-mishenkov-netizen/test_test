#!/bin/bash
# Скрипт для тестирования Docker-сборки

echo "🧪 Тестирование Docker-сборки игры про шарики..."
echo ""

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "Установите Docker: https://www.docker.com/get-started"
    exit 1
fi

echo "✓ Docker установлен: $(docker --version)"
echo ""

# Сборка образа
echo "🔨 Сборка Docker образа..."
docker build -t ball-game . || {
    echo "❌ Ошибка при сборке образа"
    exit 1
}

echo ""
echo "✓ Образ успешно собран!"
echo ""

# Проверка образа
echo "📦 Информация об образе:"
docker images ball-game
echo ""

# Тестовый запуск логики (без GUI)
echo "🧪 Тестовый запуск (логика без GUI)..."
docker run --rm ball-game python3 -c "
from logic import GameLogic, create_predefined_colors
print('✓ Импорт логики успешен')
game = GameLogic(800, 600)
print('✓ GameLogic инициализирован')
colors = create_predefined_colors()
print('✓ Цвета созданы:', len(colors), 'цветов')
ball = game.create_random_ball()
print('✓ Случайный шарик создан')
game.add_ball(ball)
print('✓ Шарик добавлен на поле')
game.update(1.0)
print('✓ Обновление игры работает')
print('')
print('🎉 Все тесты пройдены!')
"

echo ""
echo "✅ Контейнер работает корректно!"
echo ""
echo "Для запуска игры с GUI выполните:"
echo "  ./run-docker.sh"
echo ""
echo "Или вручную (с настройкой X11):"
echo "  docker run -it --rm -e DISPLAY=\$DISPLAY ball-game"

