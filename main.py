# main.py
import pygame
from game import Game
from board import Board
import sys


def main():
    pygame.init()

    initial_screen_size = (800, 800)
    screen = pygame.display.set_mode(initial_screen_size)
    pygame.display.set_caption("Сапёр - Выбор уровня сложности")

    font = pygame.font.Font("freesansbold.ttf", 48)
    clock = pygame.time.Clock()

    levels = [
        {"name": "Новичок", "size": (8, 8), "prob": 0.1},
        {"name": "Любитель", "size": (16, 16), "prob": 0.15},
        {"name": "Профессионал", "size": (16, 32), "prob": 0.2},
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, level in enumerate(levels):
                    button_rect = pygame.Rect(50, 150 + i * 100, 700, 80)
                    if button_rect.collidepoint(x, y):
                        pygame.display.set_caption(f"Сапёр - {level['name']}")
                        start_game(level, initial_screen_size)

        screen.fill((255, 255, 255))

        text_title = font.render("Выберите уровень сложности", True, (255, 0, 0))
        text_title_rect = text_title.get_rect(center=(initial_screen_size[0] // 2, 50))
        screen.blit(text_title, text_title_rect)

        for i, level in enumerate(levels):
            button_rect = pygame.Rect(50, 150 + i * 100, 700, 80)
            pygame.draw.rect(screen, (200, 200, 200), button_rect)

            text = font.render(level["name"], True, (0, 0, 0))
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(30)


def start_game(level, initial_screen_size):
    size = level["size"]
    prob = level["prob"]
    board = Board(size=size, prob=prob)
    screen_size = initial_screen_size
    game = Game(board=board, screen_size=screen_size)
    game.run()


if __name__ == "__main__":
    main()
