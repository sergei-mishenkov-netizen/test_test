"""
Графический интерфейс для игры про шарики.
Использует Pygame для визуализации и управления игрой.
"""

import pygame
import sys
from typing import Tuple
from logic import GameLogic, Ball, Color, create_predefined_colors

# Импортируем настройки (можно использовать config.py для настройки)
try:
    from config import *
except ImportError:
    # Если config.py не найден, используем значения по умолчанию
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    FPS = 60
    INITIAL_BALLS_COUNT = 70
    
    # Цвета интерфейса
    BG_COLOR = (255, 255, 255)
    DELETE_ZONE_COLOR = (255, 200, 200)
    DELETE_ZONE_BORDER = (200, 100, 100)
    INVENTORY_BG = (240, 240, 240)
    INVENTORY_BORDER = (150, 150, 150)
    TEXT_COLOR = (50, 50, 50)
    SUCK_RADIUS_COLOR = (100, 100, 255, 50)
    SHOW_HELP_ON_START = True


class GameGUI:
    """Класс графического интерфейса игры."""
    
    def __init__(self):
        """Инициализирует графический интерфейс."""
        pygame.init()
        
        # Создаем окно
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        title = globals().get('WINDOW_TITLE', 'Игра про шарики')
        pygame.display.set_caption(title)
        
        # Часы для контроля FPS
        self.clock = pygame.time.Clock()
        
        # Инициализируем игровую логику
        self.game = GameLogic(WINDOW_WIDTH, WINDOW_HEIGHT - 100)  # Оставляем место для инвентаря
        
        # Настраиваем зону удаления (правый нижний угол игрового поля)
        delete_zone_size = 120
        self.game.set_delete_zone(
            WINDOW_WIDTH - delete_zone_size - 10,
            WINDOW_HEIGHT - 100 - delete_zone_size - 10,
            delete_zone_size,
            delete_zone_size
        )
        
        # Параметры инвентаря
        self.inventory_y = WINDOW_HEIGHT - 95
        self.inventory_height = 90
        
        # Шрифты
        self.font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        # Состояние мыши
        self.mouse_down = False
        self.right_mouse_down = False
        
        # Создаем начальные шарики
        self._create_initial_balls()
        
        # Для отображения инструкций
        self.show_help = globals().get('SHOW_HELP_ON_START', True)
        
    def _create_initial_balls(self):
        """Создает начальные шарики на поле."""
        predefined_colors = create_predefined_colors()
        color_list = list(predefined_colors.values())
        
        for i in range(INITIAL_BALLS_COUNT):
            ball = self.game.create_random_ball()
            # Используем предустановленные цвета для более ярких шариков
            if i < len(color_list):
                ball.color = color_list[i]
            self.game.add_ball(ball)
    
    def run(self):
        """Основной игровой цикл."""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Дельта времени в секундах
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        self.mouse_down = True
                    elif event.button == 3:  # Правая кнопка мыши
                        self.right_mouse_down = True
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_down = False
                    elif event.button == 3:
                        self.right_mouse_down = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.show_help = not self.show_help
                    elif event.key == pygame.K_SPACE:
                        # Добавить новый случайный шарик
                        ball = self.game.create_random_ball()
                        self.game.add_ball(ball)
                    elif event.key == pygame.K_c:
                        # Очистить все шарики
                        self.game.clear_all_balls()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Обработка управления мышью
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if self.mouse_down and mouse_y < WINDOW_HEIGHT - 100:
                # Левая кнопка - всасывание шарика
                self.game.suck_ball_at_position(mouse_x, mouse_y)
            
            if self.right_mouse_down and mouse_y < WINDOW_HEIGHT - 100:
                # Правая кнопка - выплевывание шарика
                # Вычисляем скорость от центра экрана к курсору
                center_x, center_y = WINDOW_WIDTH // 2, (WINDOW_HEIGHT - 100) // 2
                vx = (mouse_x - center_x) * 0.05
                vy = (mouse_y - center_y) * 0.05
                self.game.spit_ball_at_position(mouse_x, mouse_y, vx, vy)
                # Небольшая задержка между выплевываниями
                pygame.time.wait(100)
            
            # Обновление игровой логики
            self.game.update(dt * 60)  # Нормализуем dt для логики
            
            # Отрисовка
            self._draw()
        
        pygame.quit()
        sys.exit()
    
    def _draw(self):
        """Отрисовывает все элементы игры."""
        # Фон
        self.screen.fill(BG_COLOR)
        
        # Разделительная линия между игровым полем и инвентарем
        pygame.draw.line(
            self.screen,
            INVENTORY_BORDER,
            (0, WINDOW_HEIGHT - 100),
            (WINDOW_WIDTH, WINDOW_HEIGHT - 100),
            2
        )
        
        # Зона удаления
        self._draw_delete_zone()
        
        # Шарики на игровом поле
        self._draw_balls()
        
        # Радиус всасывания (если зажата левая кнопка мыши)
        if self.mouse_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y < WINDOW_HEIGHT - 100:
                self._draw_suck_radius(mouse_x, mouse_y)
        
        # Инвентарь
        self._draw_inventory()
        
        # Информация и помощь
        self._draw_info()
        
        if self.show_help:
            self._draw_help()
        
        # Обновление экрана
        pygame.display.flip()
    
    def _draw_balls(self):
        """Отрисовывает все шарики на поле."""
        for ball in self.game.balls:
            # Рисуем шарик
            pygame.draw.circle(
                self.screen,
                ball.color.to_tuple(),
                (int(ball.x), int(ball.y)),
                int(ball.radius)
            )
            
            # Небольшая обводка для лучшей видимости
            pygame.draw.circle(
                self.screen,
                self._darken_color(ball.color),
                (int(ball.x), int(ball.y)),
                int(ball.radius),
                2
            )
            
            # Блик для объемности
            highlight_offset = int(ball.radius * 0.3)
            pygame.draw.circle(
                self.screen,
                (255, 255, 255, 180),
                (int(ball.x - highlight_offset), int(ball.y - highlight_offset)),
                int(ball.radius * 0.3)
            )
    
    def _draw_delete_zone(self):
        """Отрисовывает зону удаления шариков."""
        if self.game.delete_zone:
            zone = self.game.delete_zone
            
            # Фон зоны
            pygame.draw.rect(
                self.screen,
                DELETE_ZONE_COLOR,
                (zone.x, zone.y, zone.width, zone.height)
            )
            
            # Граница зоны
            pygame.draw.rect(
                self.screen,
                DELETE_ZONE_BORDER,
                (zone.x, zone.y, zone.width, zone.height),
                3
            )
            
            # Текст "DELETE"
            text = self.font.render("DELETE", True, DELETE_ZONE_BORDER)
            text_rect = text.get_rect(
                center=(zone.x + zone.width // 2, zone.y + zone.height // 2)
            )
            self.screen.blit(text, text_rect)
            
            # Иконка корзины (упрощенная)
            center_x = int(zone.x + zone.width // 2)
            center_y = int(zone.y + zone.height // 2 + 25)
            pygame.draw.rect(
                self.screen,
                DELETE_ZONE_BORDER,
                (center_x - 15, center_y - 10, 30, 20),
                2
            )
    
    def _draw_inventory(self):
        """Отрисовывает панель инвентаря."""
        # Фон инвентаря
        pygame.draw.rect(
            self.screen,
            INVENTORY_BG,
            (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100)
        )
        
        # Заголовок
        title_text = self.font.render(
            f"Инвентарь ({self.game.get_inventory_count()}/{self.game.inventory.max_size})",
            True,
            TEXT_COLOR
        )
        self.screen.blit(title_text, (10, WINDOW_HEIGHT - 95))
        
        # Отрисовка шариков в инвентаре
        slot_size = 60
        slot_margin = 10
        start_x = 10
        start_y = WINDOW_HEIGHT - 60
        
        for i in range(self.game.inventory.max_size):
            slot_x = start_x + i * (slot_size + slot_margin)
            
            # Рисуем слот
            pygame.draw.rect(
                self.screen,
                (220, 220, 220),
                (slot_x, start_y, slot_size, slot_size),
                0
            )
            pygame.draw.rect(
                self.screen,
                INVENTORY_BORDER,
                (slot_x, start_y, slot_size, slot_size),
                2
            )
            
            # Если в слоте есть шарик
            if i < len(self.game.inventory.balls):
                ball = self.game.inventory.balls[i]
                center_x = slot_x + slot_size // 2
                center_y = start_y + slot_size // 2
                
                # Масштабируем радиус под размер слота
                display_radius = min(slot_size // 2 - 5, ball.radius)
                
                # Рисуем шарик
                pygame.draw.circle(
                    self.screen,
                    ball.color.to_tuple(),
                    (center_x, center_y),
                    int(display_radius)
                )
                
                # Обводка
                pygame.draw.circle(
                    self.screen,
                    self._darken_color(ball.color),
                    (center_x, center_y),
                    int(display_radius),
                    2
                )
    
    def _draw_suck_radius(self, mouse_x: int, mouse_y: int):
        """Отрисовывает радиус всасывания вокруг курсора."""
        # Создаем полупрозрачную поверхность
        radius_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(
            radius_surface,
            SUCK_RADIUS_COLOR,
            (mouse_x, mouse_y),
            int(self.game.sucking_radius)
        )
        self.screen.blit(radius_surface, (0, 0))
        
        # Граница радиуса
        pygame.draw.circle(
            self.screen,
            (100, 100, 255),
            (mouse_x, mouse_y),
            int(self.game.sucking_radius),
            2
        )
    
    def _draw_info(self):
        """Отрисовывает информацию о игре."""
        # Количество шариков на поле
        ball_count_text = self.small_font.render(
            f"Шариков на поле: {self.game.get_ball_count()}",
            True,
            TEXT_COLOR
        )
        self.screen.blit(ball_count_text, (WINDOW_WIDTH - 200, 10))
        
        # FPS
        fps_text = self.small_font.render(
            f"FPS: {int(self.clock.get_fps())}",
            True,
            TEXT_COLOR
        )
        self.screen.blit(fps_text, (WINDOW_WIDTH - 200, 35))
    
    def _draw_help(self):
        """Отрисовывает справку по управлению."""
        help_texts = [
            "Управление:",
            "ЛКМ - всосать шарик",
            "ПКМ - выплюнуть шарик",
            "SPACE - добавить шарик",
            "C - очистить поле",
            "H - показать/скрыть справку",
            "ESC - выход"
        ]
        
        # Фон для справки
        help_bg_rect = pygame.Rect(10, 10, 220, len(help_texts) * 25 + 10)
        help_surface = pygame.Surface((help_bg_rect.width, help_bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(help_surface, (255, 255, 255, 200), help_surface.get_rect())
        self.screen.blit(help_surface, (help_bg_rect.x, help_bg_rect.y))
        
        pygame.draw.rect(self.screen, INVENTORY_BORDER, help_bg_rect, 2)
        
        # Текст справки
        for i, text in enumerate(help_texts):
            if i == 0:
                rendered_text = self.font.render(text, True, TEXT_COLOR)
            else:
                rendered_text = self.small_font.render(text, True, TEXT_COLOR)
            self.screen.blit(rendered_text, (20, 15 + i * 25))
    
    def _darken_color(self, color: Color) -> Tuple[int, int, int]:
        """Затемняет цвет для создания обводки."""
        factor = 0.7
        return (
            int(color.r * factor),
            int(color.g * factor),
            int(color.b * factor)
        )


def main():
    """Главная функция запуска игры."""
    game_gui = GameGUI()
    game_gui.run()


if __name__ == "__main__":
    main()

