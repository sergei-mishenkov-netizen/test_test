"""
Модуль игровой логики для игры про шарики.
Содержит классы и функции для управления шариками, их движением,
взаимодействием и смешиванием цветов.
"""

import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Color:
    """Класс для представления цвета в формате RGB."""
    r: int  # 0-255
    g: int  # 0-255
    b: int  # 0-255
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Возвращает цвет в виде кортежа (r, g, b)."""
        return (self.r, self.g, self.b)
    
    def to_hex(self) -> str:
        """Возвращает цвет в hex формате."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    @classmethod
    def from_tuple(cls, rgb: Tuple[int, int, int]) -> 'Color':
        """Создает цвет из кортежа (r, g, b)."""
        return cls(rgb[0], rgb[1], rgb[2])
    
    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        return self.r == other.r and self.g == other.g and self.b == other.b


@dataclass
class Ball:
    """Класс для представления шарика."""
    x: float  # Позиция X
    y: float  # Позиция Y
    vx: float  # Скорость по X
    vy: float  # Скорость по Y
    radius: float  # Радиус шарика
    color: Color  # Цвет шарика
    id: int = field(default_factory=lambda: random.randint(0, 1000000))
    
    def move(self, dt: float = 1.0):
        """Двигает шарик согласно его скорости."""
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def distance_to(self, other: 'Ball') -> float:
        """Вычисляет расстояние до другого шарика."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def is_touching(self, other: 'Ball') -> bool:
        """Проверяет, касается ли шарик другого шарика."""
        return self.distance_to(other) <= (self.radius + other.radius)
    
    def is_point_inside(self, px: float, py: float) -> bool:
        """Проверяет, находится ли точка внутри шарика."""
        dx = self.x - px
        dy = self.y - py
        return math.sqrt(dx * dx + dy * dy) <= self.radius
    
    def copy(self) -> 'Ball':
        """Создает копию шарика."""
        return Ball(
            x=self.x,
            y=self.y,
            vx=self.vx,
            vy=self.vy,
            radius=self.radius,
            color=Color(self.color.r, self.color.g, self.color.b),
            id=self.id
        )


class ColorMixer:
    """Класс для смешивания цветов шариков."""
    
    @staticmethod
    def mix_colors(color1: Color, color2: Color) -> Color:
        """
        Смешивает два цвета, создавая интересные результаты.
        Использует нелинейное смешивание для более насыщенных цветов.
        """
        # Используем нелинейное смешивание для более интересных результатов
        # Вместо простого среднего используем взвешенное смешивание
        
        # Определяем яркость каждого цвета
        brightness1 = (color1.r + color1.g + color1.b) / 3
        brightness2 = (color2.r + color2.g + color2.b) / 3
        
        # Если один из цветов очень темный или светлый, меняем веса
        weight1 = 0.5
        weight2 = 0.5
        
        # Используем смешивание в HSV пространстве для лучших результатов
        hsv1 = ColorMixer._rgb_to_hsv(color1)
        hsv2 = ColorMixer._rgb_to_hsv(color2)
        
        # Смешиваем тон (hue) с учетом круговой природы
        h_diff = abs(hsv1[0] - hsv2[0])
        if h_diff > 180:
            # Короткий путь через 0/360
            if hsv1[0] > hsv2[0]:
                new_h = (hsv1[0] + (hsv2[0] + 360)) / 2
            else:
                new_h = (hsv2[0] + (hsv1[0] + 360)) / 2
            new_h = new_h % 360
        else:
            new_h = (hsv1[0] * weight1 + hsv2[0] * weight2)
        
        # Смешиваем насыщенность с усилением (чтобы избежать белого)
        new_s = min(100, (hsv1[1] + hsv2[1]) / 2 * 1.2)  # Увеличиваем насыщенность
        
        # Смешиваем яркость
        new_v = (hsv1[2] + hsv2[2]) / 2
        
        # Преобразуем обратно в RGB
        return ColorMixer._hsv_to_rgb(new_h, new_s, new_v)
    
    @staticmethod
    def _rgb_to_hsv(color: Color) -> Tuple[float, float, float]:
        """Конвертирует RGB в HSV."""
        r, g, b = color.r / 255.0, color.g / 255.0, color.b / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        diff = max_c - min_c
        
        # Hue
        if diff == 0:
            h = 0
        elif max_c == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_c == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360
        
        # Saturation
        s = 0 if max_c == 0 else (diff / max_c) * 100
        
        # Value
        v = max_c * 100
        
        return (h, s, v)
    
    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> Color:
        """Конвертирует HSV в RGB."""
        s = s / 100.0
        v = v / 100.0
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return Color(
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )


@dataclass
class DeleteZone:
    """Зона на экране для удаления шариков."""
    x: float
    y: float
    width: float
    height: float
    
    def contains_point(self, px: float, py: float) -> bool:
        """Проверяет, находится ли точка внутри зоны удаления."""
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)
    
    def contains_ball(self, ball: Ball) -> bool:
        """Проверяет, находится ли шарик в зоне удаления."""
        return self.contains_point(ball.x, ball.y)


class Inventory:
    """Класс для хранения шариков в инвентаре."""
    
    def __init__(self, max_size: Optional[int] = None):
        """
        Инициализирует инвентарь.
        
        Args:
            max_size: Максимальное количество шариков (None = без ограничений)
        """
        self.balls: List[Ball] = []
        self.max_size = max_size
    
    def add_ball(self, ball: Ball) -> bool:
        """
        Добавляет шарик в инвентарь.
        
        Returns:
            True если шарик добавлен, False если инвентарь полон
        """
        if self.max_size is not None and len(self.balls) >= self.max_size:
            return False
        self.balls.append(ball)
        return True
    
    def remove_ball(self, ball: Ball) -> bool:
        """
        Удаляет шарик из инвентаря.
        
        Returns:
            True если шарик удален, False если шарика нет в инвентаре
        """
        if ball in self.balls:
            self.balls.remove(ball)
            return True
        return False
    
    def get_ball_at_index(self, index: int) -> Optional[Ball]:
        """Возвращает шарик по индексу."""
        if 0 <= index < len(self.balls):
            return self.balls[index]
        return None
    
    def pop_ball(self) -> Optional[Ball]:
        """Извлекает последний шарик из инвентаря."""
        if self.balls:
            return self.balls.pop()
        return None
    
    def is_full(self) -> bool:
        """Проверяет, полон ли инвентарь."""
        return self.max_size is not None and len(self.balls) >= self.max_size
    
    def is_empty(self) -> bool:
        """Проверяет, пуст ли инвентарь."""
        return len(self.balls) == 0
    
    def size(self) -> int:
        """Возвращает количество шариков в инвентаре."""
        return len(self.balls)


class GameLogic:
    """Основной класс игровой логики."""
    
    def __init__(self, width: float, height: float):
        """
        Инициализирует игровую логику.
        
        Args:
            width: Ширина игрового поля
            height: Высота игрового поля
        """
        self.width = width
        self.height = height
        self.balls: List[Ball] = []
        self.inventory = Inventory(max_size=10)  # Максимум 10 шариков в инвентаре
        self.delete_zone: Optional[DeleteZone] = None
        self.sucking_radius = 50.0  # Радиус "всасывания" от курсора
        self.color_mixer = ColorMixer()
    
    def set_delete_zone(self, x: float, y: float, width: float, height: float):
        """Устанавливает зону удаления на экране."""
        self.delete_zone = DeleteZone(x, y, width, height)
    
    def add_ball(self, ball: Ball):
        """Добавляет шарик на игровое поле."""
        self.balls.append(ball)
    
    def remove_ball(self, ball: Ball):
        """Удаляет шарик с игрового поля."""
        if ball in self.balls:
            self.balls.remove(ball)
    
    def create_random_ball(self) -> Ball:
        """Создает случайный шарик."""
        x = random.uniform(50, self.width - 50)
        y = random.uniform(50, self.height - 50)
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        radius = random.uniform(15, 30)
        color = Color(
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        return Ball(x, y, vx, vy, radius, color)
    
    def update(self, dt: float = 1.0):
        """
        Обновляет состояние игры.
        
        Args:
            dt: Временной шаг (дельта времени)
        """
        # Двигаем все шарики
        for ball in self.balls:
            ball.move(dt)
            self._handle_boundary_collision(ball)
        
        # Проверяем столкновения и смешиваем цвета
        self._handle_ball_collisions()
        
        # Проверяем, какие шарики в зоне удаления
        if self.delete_zone:
            balls_to_remove = []
            for ball in self.balls:
                if self.delete_zone.contains_ball(ball):
                    balls_to_remove.append(ball)
            
            for ball in balls_to_remove:
                self.remove_ball(ball)
    
    def _handle_boundary_collision(self, ball: Ball):
        """Обрабатывает столкновение шарика с границами экрана."""
        # Отскок от левой/правой границы
        if ball.x - ball.radius < 0:
            ball.x = ball.radius
            ball.vx = abs(ball.vx)
        elif ball.x + ball.radius > self.width:
            ball.x = self.width - ball.radius
            ball.vx = -abs(ball.vx)
        
        # Отскок от верхней/нижней границы
        if ball.y - ball.radius < 0:
            ball.y = ball.radius
            ball.vy = abs(ball.vy)
        elif ball.y + ball.radius > self.height:
            ball.y = self.height - ball.radius
            ball.vy = -abs(ball.vy)
    
    def _handle_ball_collisions(self):
        """Обрабатывает столкновения шариков и смешивание цветов."""
        n = len(self.balls)
        for i in range(n):
            for j in range(i + 1, n):
                ball1 = self.balls[i]
                ball2 = self.balls[j]
                
                if ball1.is_touching(ball2):
                    # Смешиваем цвета
                    new_color = self.color_mixer.mix_colors(ball1.color, ball2.color)
                    ball1.color = new_color
                    ball2.color = new_color
                    
                    # Шарики НЕ отталкиваются (по требованию)
                    # Просто продолжают двигаться
    
    def suck_ball_at_position(self, mouse_x: float, mouse_y: float) -> bool:
        """
        Пытается "всосать" шарик в инвентарь в позиции курсора.
        
        Args:
            mouse_x: Координата X курсора
            mouse_y: Координата Y курсора
            
        Returns:
            True если шарик был всосан, False иначе
        """
        if self.inventory.is_full():
            return False
        
        # Ищем ближайший шарик в радиусе всасывания
        closest_ball = None
        min_distance = self.sucking_radius
        
        for ball in self.balls:
            distance = math.sqrt((ball.x - mouse_x) ** 2 + (ball.y - mouse_y) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_ball = ball
        
        if closest_ball:
            # Всасываем шарик
            self.remove_ball(closest_ball)
            self.inventory.add_ball(closest_ball)
            return True
        
        return False
    
    def spit_ball_at_position(self, mouse_x: float, mouse_y: float, 
                             vx: float = 0, vy: float = 0) -> bool:
        """
        "Выплевывает" шарик из инвентаря в указанную позицию.
        
        Args:
            mouse_x: Координата X для выплевывания
            mouse_y: Координата Y для выплевывания
            vx: Скорость по X (по умолчанию 0)
            vy: Скорость по Y (по умолчанию 0)
            
        Returns:
            True если шарик был выплюнут, False если инвентарь пуст
        """
        if self.inventory.is_empty():
            return False
        
        ball = self.inventory.pop_ball()
        if ball:
            # Устанавливаем новую позицию и скорость
            ball.x = mouse_x
            ball.y = mouse_y
            ball.vx = vx
            ball.vy = vy
            
            # Добавляем шарик обратно на поле
            self.add_ball(ball)
            return True
        
        return False
    
    def get_ball_at_position(self, x: float, y: float) -> Optional[Ball]:
        """
        Возвращает шарик в указанной позиции (если есть).
        
        Args:
            x: Координата X
            y: Координата Y
            
        Returns:
            Ball если найден, None иначе
        """
        for ball in self.balls:
            if ball.is_point_inside(x, y):
                return ball
        return None
    
    def get_balls_in_area(self, x: float, y: float, radius: float) -> List[Ball]:
        """
        Возвращает все шарики в указанной области.
        
        Args:
            x: Центр области X
            y: Центр области Y
            radius: Радиус области
            
        Returns:
            Список шариков в области
        """
        balls_in_area = []
        for ball in self.balls:
            distance = math.sqrt((ball.x - x) ** 2 + (ball.y - y) ** 2)
            if distance <= radius:
                balls_in_area.append(ball)
        return balls_in_area
    
    def get_ball_count(self) -> int:
        """Возвращает количество шариков на поле."""
        return len(self.balls)
    
    def get_inventory_count(self) -> int:
        """Возвращает количество шариков в инвентаре."""
        return self.inventory.size()
    
    def clear_all_balls(self):
        """Удаляет все шарики с поля."""
        self.balls.clear()
    
    def clear_inventory(self):
        """Очищает инвентарь."""
        self.inventory.balls.clear()


# Вспомогательные функции для создания предустановленных цветов
def create_predefined_colors() -> dict:
    """Создает набор предустановленных цветов."""
    return {
        'red': Color(255, 50, 50),
        'green': Color(50, 255, 50),
        'blue': Color(50, 50, 255),
        'yellow': Color(255, 255, 50),
        'cyan': Color(50, 255, 255),
        'magenta': Color(255, 50, 255),
        'orange': Color(255, 165, 50),
        'purple': Color(160, 50, 255),
        'pink': Color(255, 192, 203),
        'lime': Color(191, 255, 50),
    }


if __name__ == "__main__":
    # Пример использования
    print("=== Демонстрация игровой логики ===\n")
    
    # Создаем игру 800x600
    game = GameLogic(800, 600)
    
    # Устанавливаем зону удаления в правом нижнем углу
    game.set_delete_zone(700, 500, 100, 100)
    
    # Создаем несколько случайных шариков
    print("Создаем 5 случайных шариков...")
    for _ in range(5):
        ball = game.create_random_ball()
        game.add_ball(ball)
    
    print(f"Шариков на поле: {game.get_ball_count()}")
    print(f"Шариков в инвентаре: {game.get_inventory_count()}\n")
    
    # Симулируем несколько шагов игры
    print("Симулируем 10 шагов игры...")
    for step in range(10):
        game.update(dt=1.0)
        if step % 3 == 0:
            print(f"  Шаг {step}: {game.get_ball_count()} шариков на поле")
    
    print()
    
    # Пробуем всосать шарик
    if game.balls:
        first_ball = game.balls[0]
        print(f"Всасываем шарик в позиции ({first_ball.x:.1f}, {first_ball.y:.1f})...")
        success = game.suck_ball_at_position(first_ball.x, first_ball.y)
        if success:
            print(f"✓ Шарик всосан! В инвентаре: {game.get_inventory_count()}")
        else:
            print("✗ Не удалось всосать шарик")
    
    print()
    
    # Выплевываем шарик обратно
    if not game.inventory.is_empty():
        print("Выплевываем шарик обратно в центр экрана...")
        success = game.spit_ball_at_position(400, 300, vx=3, vy=-2)
        if success:
            print(f"✓ Шарик выплюнут! На поле: {game.get_ball_count()}")
        else:
            print("✗ Инвентарь пуст")
    
    print()
    
    # Демонстрация смешивания цветов
    print("=== Демонстрация смешивания цветов ===\n")
    mixer = ColorMixer()
    colors = create_predefined_colors()
    
    test_pairs = [
        ('red', 'blue'),
        ('yellow', 'blue'),
        ('red', 'green'),
        ('cyan', 'magenta'),
    ]
    
    for color1_name, color2_name in test_pairs:
        color1 = colors[color1_name]
        color2 = colors[color2_name]
        mixed = mixer.mix_colors(color1, color2)
        print(f"{color1_name.capitalize()} {color1.to_hex()} + {color2_name.capitalize()} {color2.to_hex()} = {mixed.to_hex()}")
    
    print("\n✓ Демонстрация завершена!")

