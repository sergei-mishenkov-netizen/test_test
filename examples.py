"""
Примеры использования игровой логики.
Демонстрирует различные возможности без GUI.
"""

from logic import (
    GameLogic, Ball, Color, ColorMixer,
    create_predefined_colors, Inventory
)
import time


def example_1_basic_game():
    """Пример 1: Базовая игра с несколькими шариками."""
    print("\n" + "="*60)
    print("ПРИМЕР 1: Базовая игра")
    print("="*60 + "\n")
    
    # Создаем игру
    game = GameLogic(800, 600)
    
    # Добавляем 3 шарика
    colors = create_predefined_colors()
    
    ball1 = Ball(100, 100, 2, 1, 20, colors['red'])
    ball2 = Ball(200, 150, -1, 2, 25, colors['blue'])
    ball3 = Ball(300, 200, 1, -1, 22, colors['green'])
    
    game.add_ball(ball1)
    game.add_ball(ball2)
    game.add_ball(ball3)
    
    print(f"✓ Создано {game.get_ball_count()} шариков")
    print(f"  Шарик 1: позиция ({ball1.x}, {ball1.y}), цвет {ball1.color.to_hex()}")
    print(f"  Шарик 2: позиция ({ball2.x}, {ball2.y}), цвет {ball2.color.to_hex()}")
    print(f"  Шарик 3: позиция ({ball3.x}, {ball3.y}), цвет {ball3.color.to_hex()}")
    
    # Симулируем 5 шагов
    print("\nСимуляция движения...")
    for i in range(5):
        game.update(dt=1.0)
        print(f"  Шаг {i+1}: Шарик 1 теперь в ({ball1.x:.1f}, {ball1.y:.1f})")


def example_2_color_mixing():
    """Пример 2: Демонстрация смешивания цветов."""
    print("\n" + "="*60)
    print("ПРИМЕР 2: Смешивание цветов")
    print("="*60 + "\n")
    
    mixer = ColorMixer()
    colors = create_predefined_colors()
    
    test_pairs = [
        ('red', 'blue', 'фиолетовый'),
        ('red', 'yellow', 'оранжевый'),
        ('blue', 'yellow', 'зеленый'),
        ('red', 'green', 'коричневый/желтый'),
        ('cyan', 'magenta', 'синий'),
    ]
    
    print("Таблица смешивания цветов:\n")
    print(f"{'Цвет 1':<10} {'Hex 1':<10} + {'Цвет 2':<10} {'Hex 2':<10} = {'Результат':<10} {'Ожидается':<15}")
    print("-" * 90)
    
    for color1_name, color2_name, expected in test_pairs:
        color1 = colors[color1_name]
        color2 = colors[color2_name]
        result = mixer.mix_colors(color1, color2)
        
        print(f"{color1_name:<10} {color1.to_hex():<10} + "
              f"{color2_name:<10} {color2.to_hex():<10} = "
              f"{result.to_hex():<10} ({expected})")


def example_3_inventory():
    """Пример 3: Работа с инвентарем."""
    print("\n" + "="*60)
    print("ПРИМЕР 3: Система инвентаря")
    print("="*60 + "\n")
    
    # Создаем инвентарь на 5 слотов
    inventory = Inventory(max_size=5)
    colors = create_predefined_colors()
    
    print(f"Создан инвентарь: {inventory.size()}/{inventory.max_size} шариков")
    print(f"Пуст? {inventory.is_empty()}")
    print(f"Полон? {inventory.is_full()}\n")
    
    # Добавляем шарики
    print("Добавляем шарики в инвентарь:")
    for i, (name, color) in enumerate(list(colors.items())[:6]):
        ball = Ball(0, 0, 0, 0, 20, color)
        success = inventory.add_ball(ball)
        
        if success:
            print(f"  ✓ Добавлен {name} шарик ({color.to_hex()})")
        else:
            print(f"  ✗ Не удалось добавить {name} шарик - инвентарь полон!")
    
    print(f"\nИнвентарь: {inventory.size()}/{inventory.max_size} шариков")
    print(f"Полон? {inventory.is_full()}")
    
    # Извлекаем шарик
    print("\nИзвлекаем последний шарик...")
    ball = inventory.pop_ball()
    if ball:
        print(f"  ✓ Извлечен шарик цвета {ball.color.to_hex()}")
        print(f"  Осталось в инвентаре: {inventory.size()}")


def example_4_collision():
    """Пример 4: Столкновение и смешивание цветов."""
    print("\n" + "="*60)
    print("ПРИМЕР 4: Столкновение шариков")
    print("="*60 + "\n")
    
    game = GameLogic(800, 600)
    colors = create_predefined_colors()
    
    # Создаем два шарика, которые столкнутся
    ball1 = Ball(100, 100, 3, 0, 25, colors['red'])
    ball2 = Ball(200, 100, -3, 0, 25, colors['blue'])
    
    game.add_ball(ball1)
    game.add_ball(ball2)
    
    print(f"Начальные цвета:")
    print(f"  Шарик 1 (красный): {ball1.color.to_hex()}")
    print(f"  Шарик 2 (синий): {ball2.color.to_hex()}")
    print(f"\nШарики двигаются навстречу друг другу...")
    
    # Симулируем до столкновения
    for i in range(20):
        game.update(dt=1.0)
        
        distance = ball1.distance_to(ball2)
        if i % 5 == 0:
            print(f"  Шаг {i}: расстояние = {distance:.1f}")
        
        # Проверяем столкновение
        if ball1.is_touching(ball2):
            print(f"\n✓ Столкновение на шаге {i}!")
            print(f"  Новый цвет обоих шариков: {ball1.color.to_hex()}")
            break


def example_5_delete_zone():
    """Пример 5: Зона удаления."""
    print("\n" + "="*60)
    print("ПРИМЕР 5: Зона удаления")
    print("="*60 + "\n")
    
    game = GameLogic(800, 600)
    
    # Устанавливаем зону удаления в правом нижнем углу
    game.set_delete_zone(700, 500, 100, 100)
    
    print(f"Зона удаления: ({game.delete_zone.x}, {game.delete_zone.y}) "
          f"размер {game.delete_zone.width}x{game.delete_zone.height}")
    
    # Создаем шарики
    colors = create_predefined_colors()
    
    # Шарик вне зоны
    ball1 = Ball(100, 100, 0, 0, 20, colors['red'])
    # Шарик в зоне удаления
    ball2 = Ball(750, 550, 0, 0, 20, colors['blue'])
    # Шарик, который войдет в зону
    ball3 = Ball(650, 550, 5, 0, 20, colors['green'])
    
    game.add_ball(ball1)
    game.add_ball(ball2)
    game.add_ball(ball3)
    
    print(f"\nШариков на поле: {game.get_ball_count()}")
    print(f"  Шарик 1: ({ball1.x}, {ball1.y}) - вне зоны")
    print(f"  Шарик 2: ({ball2.x}, {ball2.y}) - В ЗОНЕ УДАЛЕНИЯ")
    print(f"  Шарик 3: ({ball3.x}, {ball3.y}) - двигается к зоне")
    
    # Обновляем игру
    print("\nОбновление игры (удаление шариков в зоне)...")
    game.update(dt=1.0)
    
    print(f"Шариков осталось: {game.get_ball_count()}")
    
    # Ещё несколько шагов
    for i in range(15):
        game.update(dt=1.0)
        if i % 5 == 4:
            print(f"  Шаг {i+1}: шариков = {game.get_ball_count()}")


def example_6_suck_and_spit():
    """Пример 6: Всасывание и выплевывание шариков."""
    print("\n" + "="*60)
    print("ПРИМЕР 6: Всасывание и выплевывание")
    print("="*60 + "\n")
    
    game = GameLogic(800, 600)
    colors = create_predefined_colors()
    
    # Создаем шарик
    ball = Ball(100, 100, 0, 0, 20, colors['red'])
    game.add_ball(ball)
    
    print(f"Шариков на поле: {game.get_ball_count()}")
    print(f"В инвентаре: {game.get_inventory_count()}")
    print(f"Шарик в позиции ({ball.x}, {ball.y})")
    
    # Всасываем шарик
    print(f"\nВсасываем шарик (клик в позиции {ball.x}, {ball.y})...")
    success = game.suck_ball_at_position(ball.x, ball.y)
    
    if success:
        print(f"  ✓ Шарик всосан!")
        print(f"  Шариков на поле: {game.get_ball_count()}")
        print(f"  В инвентаре: {game.get_inventory_count()}")
    
    # Выплевываем обратно
    print(f"\nВыплевываем шарик в центр экрана...")
    success = game.spit_ball_at_position(400, 300, vx=2, vy=-2)
    
    if success:
        new_ball = game.balls[-1]
        print(f"  ✓ Шарик выплюнут!")
        print(f"  Новая позиция: ({new_ball.x}, {new_ball.y})")
        print(f"  Новая скорость: ({new_ball.vx}, {new_ball.vy})")
        print(f"  Шариков на поле: {game.get_ball_count()}")


def main():
    """Запускает все примеры."""
    print("\n" + "🎮 " * 20)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ИГРОВОЙ ЛОГИКИ")
    print("🎮 " * 20)
    
    examples = [
        example_1_basic_game,
        example_2_color_mixing,
        example_3_inventory,
        example_4_collision,
        example_5_delete_zone,
        example_6_suck_and_spit,
    ]
    
    for i, example in enumerate(examples, 1):
        example()
        
        if i < len(examples):
            input("\nНажмите Enter для следующего примера...")
    
    print("\n" + "="*60)
    print("✓ ВСЕ ПРИМЕРЫ ЗАВЕРШЕНЫ!")
    print("="*60)
    print("\nЧтобы запустить игру с GUI, выполните:")
    print("  python3 game_gui.py\n")


if __name__ == "__main__":
    main()

