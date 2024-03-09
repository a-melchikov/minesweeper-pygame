# game.py
import pygame
import os
from board import Board
from datetime import datetime, timedelta


class Game:
    def __init__(self, board, screen_size):
        """
        Конструктор класса Game.

        :param board: Объект класса Board, представляющий игровое поле.
        :param screen_size: Размер экрана в формате (width, height).
        """
        self.images = None
        self.screen = None
        self.board = board
        self.screen_size = screen_size
        self.piece_size = (
            self.screen_size[0] // self.board.get_size()[1],
            self.screen_size[1] // self.board.get_size()[0],
        )
        self.played_win_sound = False
        self.played_lose_sound = False
        self.end_time = None
        self.end = True
        self.start_time = None
        self.timer_font = pygame.font.Font(None, 36)
        self.load_images()

    def run(self):
        """
        Запускает игру, обрабатывает события и обновляет экран.

        Игра продолжается, пока пользователь не закроет окно или не выиграет/проиграет.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    right_click = pygame.mouse.get_pressed()[2]
                    self.handle_click(position, right_click)
                elif event.type == pygame.KEYDOWN:
                    if self.board.get_won() or self.board.get_lost():
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_SPACE:
                            running = False
                            return
            if self.end:
                self.draw()
                self.update_timer()
                form_time = self.get_formatted_time()
            pygame.display.flip()
            if self.board.get_won():
                self.show_end_screen(
                    [
                        "Поздравляем! Вы выиграли!",
                        f"Ваш результат: {form_time}",
                        "Нажмите 'R' для перезапуска, 'Space' для возврата в меню.",
                    ]
                )
            if self.board.get_won() and self.end:
                self.play_sound("win.mp3")
                self.end = False
            if self.board.get_lost():
                self.show_end_screen(
                    [
                        "Вы проиграли. Попробуйте еще раз!",
                        "Нажмите 'R' для перезапуска, 'Space' для возврата в меню.",
                    ]
                )
            if self.board.get_lost() and self.end:
                self.play_sound("lose.mp3")
                self.end = False
        pygame.quit()

    def update_timer(self):
        """
        Обновляет значение таймера и отображает его на экране.
        """
        if not self.start_time:
            self.start_time = datetime.now()

        elapsed_time = datetime.now() - self.start_time
        formatted_time = "{:02}:{:02}:{:03}".format(
            (elapsed_time.seconds % 3600) // 60,
            elapsed_time.seconds % 60,
            elapsed_time.microseconds // 1000,
        )

        timer_text = self.timer_font.render(formatted_time, True, (255, 255, 255))
        timer_rect = timer_text.get_rect(topleft=(10, 10))
        pygame.draw.rect(self.screen, (0, 0, 0), timer_rect)
        self.screen.blit(timer_text, timer_rect)

    def get_formatted_time(self):
        """
        Возвращает отформатированное время в формате "00:00:000".
        """

        elapsed_time = datetime.now() - self.start_time
        formatted_time = "{:02}:{:02}:{:03}".format(
            (elapsed_time.seconds % 3600) // 60,
            elapsed_time.seconds % 60,
            elapsed_time.microseconds // 1000,
        )
        return formatted_time

    def reset_game(self):
        """Перезапускает игру."""
        size = self.board.get_size()
        prob = self.board.prob
        self.end_time = None
        self.end = True
        self.start_time = None
        self.board = Board(size=size, prob=prob)

    def show_end_screen(self, messages):
        """
        Показывает экран в конце игры с заданными сообщениями.

        :param messages: Список сообщений.
        """
        font = pygame.font.Font(None, 38)
        rects = []
        for i, message in enumerate(messages):
            text = font.render(message, True, (255, 255, 255))
            rect = text.get_rect(
                center=(
                    self.screen_size[0] // 2,
                    self.screen_size[1] // 2 + 35 * (i - len(messages) // 2),
                )
            )
            rects.append(rect)
            # Рисуем прямоугольник
            pygame.draw.rect(self.screen, (0, 0, 0), rect, border_radius=4)
            # Выводим текст внутри прямоугольника
            self.screen.blit(text, rect)

        pygame.display.flip()

    def draw(self):
        """
        Отрисовывает все кусочки на экране.
        """
        top_left = (0, 0)
        for row in range(self.board.get_size()[0]):
            for col in range(self.board.get_size()[1]):
                piece = self.board.get_piece((row, col))
                image = self.get_image(piece)
                self.screen.blit(image, top_left)
                top_left = top_left[0] + self.piece_size[0], top_left[1]

            top_left = 0, top_left[1] + self.piece_size[1]

    def load_images(self):
        """
        Загружает изображения для кусочков и изменяет их размер согласно размеру экрана.
        """
        self.images = {}
        images_directory = "images"
        for file_name in os.listdir(images_directory):
            if not file_name.endswith(".png"):
                continue
            path = images_directory + r"/" + file_name
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(
                img, (int(self.piece_size[0]), int(self.piece_size[1]))
            )
            self.images[file_name.split(".")[0]] = img

    def get_image(self, piece):
        """
        Возвращает изображение для данного кусочка.

        :param piece: Кусочек, для которого нужно получить изображение.
        :return: Изображение для кусочка.
        """
        string = (
            "bomb-at-clicked-block"
            if piece.get_has_bomb() and piece.get_clicked()
            else (
                str(piece.get_num_around())
                if piece.get_clicked()
                else "flag" if piece.get_flagged() else "empty-block"
            )
        )
        return self.images[string]

    def handle_click(self, position, right_click):
        """
        Обрабатывает клик пользователя на экране.

        :param position: Позиция клика на экране.
        :param right_click: Флаг, указывающий, был ли это правый клик мыши.
        """
        if self.board.get_lost():
            return
        index = position[1] // self.piece_size[1], position[0] // self.piece_size[0]
        piece = self.board.get_piece(index)
        self.board.handle_click(piece, right_click)
        if self.board.get_won() or self.board.get_lost():
            self.draw()

    def play_sound(self, sound_file):
        """
        Воспроизводит звуковой файл.

        :param sound_file: Имя звукового файла.
        """
        sound = pygame.mixer.Sound(os.path.join("sounds", sound_file))
        sound.play()
