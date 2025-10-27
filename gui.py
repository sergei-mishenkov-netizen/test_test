#!/usr/bin/env python3
"""
Точка входа в игру про шарики.
Запускает графический интерфейс игры.
"""

import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Главная функция запуска игры."""
    try:
        # Пытаемся импортировать и запустить GUI
        from game_gui import GameGUI
        
        print("🎮 Запуск игры про шарики...")
        print("Управление:")
        print("  ЛКМ - всосать шарик")
        print("  ПКМ - выплюнуть шарик")
        print("  SPACE - добавить шарик")
        print("  C - очистить поле")
        print("  H - показать/скрыть справку")
        print("  ESC - выход\n")
        
        game = GameGUI()
        game.run()
        
    except ImportError as e:
        print("❌ Ошибка импорта:", e)
        print("\n💡 Попробуйте установить зависимости:")
        print("   pip3 install -r requirements.txt")
        print("\nИли запустите примеры без GUI:")
        print("   python3 examples.py")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Ошибка при запуске игры: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

