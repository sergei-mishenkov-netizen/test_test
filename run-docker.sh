#!/bin/bash
# Скрипт для запуска игры в Docker-контейнере с поддержкой GUI

echo "🎮 Запуск игры про шарики в Docker..."

# Определяем операционную систему
OS="$(uname -s)"

case "${OS}" in
    Linux*)
        echo "Платформа: Linux"
        echo "Настройка X11..."
        xhost +local:docker
        
        echo "Запуск контейнера..."
        docker run -it --rm \
          -e DISPLAY=$DISPLAY \
          -v /tmp/.X11-unix:/tmp/.X11-unix \
          --net=host \
          ball-game
        
        echo "Очистка X11..."
        xhost -local:docker
        ;;
        
    Darwin*)
        echo "Платформа: macOS"
        
        # Проверка установлен ли XQuartz
        if ! command -v xquartz &> /dev/null; then
            echo "⚠️  XQuartz не установлен!"
            echo "Установите его командой: brew install --cask xquartz"
            echo "Затем перезапустите терминал и повторите запуск."
            exit 1
        fi
        
        echo "Настройка X11..."
        xhost + localhost
        
        echo "Запуск контейнера..."
        docker run -it --rm \
          -e DISPLAY=host.docker.internal:0 \
          -v /tmp/.X11-unix:/tmp/.X11-unix \
          ball-game
        ;;
        
    MINGW*|MSYS*|CYGWIN*)
        echo "Платформа: Windows"
        echo "Убедитесь, что X-сервер (VcXsrv или Xming) запущен!"
        
        # Получаем IP адрес WSL
        WSL_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
        export DISPLAY=$WSL_IP:0
        
        echo "Используется DISPLAY=$DISPLAY"
        echo "Запуск контейнера..."
        docker run -it --rm \
          -e DISPLAY=$DISPLAY \
          ball-game
        ;;
        
    *)
        echo "❌ Неизвестная операционная система: ${OS}"
        exit 1
        ;;
esac

echo "✅ Завершено!"

