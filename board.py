# board.py
from piece import Piece
from random import random


class Board:
    def __init__(self, size, prob):
        """
        Конструктор класса Board.

        :param size: Размер доски в формате (rows, columns).
        :param prob: Вероятность появления бомбы в каждом кусочке.
        """
        self.board = None
        self.size = size
        self.prob = prob
        self.lost = False
        self.won = False
        self.num_clicked = 0
        self.num_non_bombs = 0
        self.set_board()

    def set_board(self):
        """Инициализирует доску, заполняя ее кусочками с бомбами и устанавливает соседей для каждого кусочка."""
        self.board = []
        for row in range(self.size[0]):
            row_pieces = []
            for col in range(self.size[1]):
                has_bomb = random() < self.prob
                if not has_bomb:
                    self.num_non_bombs += 1
                piece = Piece(has_bomb)
                row_pieces.append(piece)
            self.board.append(row_pieces)
        self.set_neighbors()

    def set_neighbors(self):
        """Устанавливает соседей для каждого кусочка на доске."""
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece((row, col))
                neighbors = self.get_list_of_neighbors((row, col))
                piece.set_neighbors(neighbors)

    def get_list_of_neighbors(self, index):
        """Возвращает список соседей для данного индекса на доске."""
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                out_of_bounds = (
                    row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                )
                same = row == index[0] and col == index[1]
                if same or out_of_bounds:
                    continue
                neighbors.append(self.get_piece((row, col)))
        return neighbors

    def get_size(self):
        """Возвращает размер доски в формате (rows, columns)."""
        return self.size

    def get_piece(self, index):
        """Возвращает кусочек на доске по заданному индексу."""
        return self.board[index[0]][index[1]]

    def handle_click(self, piece, flag):
        """
        Обрабатывает клик на данном кусочке.

        :param piece: Кусочек, на который произошел клик.
        :param flag: Флаг, указывающий, был ли это клик правой кнопкой мыши (ставится флаг).
        """
        if piece.get_clicked() or (not flag and piece.get_flagged()):
            return
        if flag:
            piece.toggle_flag()
            return
        piece.click()
        if piece.get_has_bomb():
            self.lost = True
            return
        self.num_clicked += 1
        if piece.get_num_around() != 0:
            return
        for neighbor in piece.get_neighbors():
            if not neighbor.get_has_bomb() and not neighbor.get_clicked():
                self.handle_click(neighbor, False)

    def get_lost(self):
        """
        Возвращает True, если игрок проиграл.
        При проигрыше открываются все поля.
        """
        if self.lost:
            self.reveal_all()
        return self.lost

    def get_won(self):
        """
        Возвращает True, если игрок выиграл.
        При выигрыше открываются все поля.
        """
        if self.num_non_bombs == self.num_clicked:
            self.reveal_all()
            self.won = True
        return self.won

    def reveal_all(self):
        """Открывает все бомбы на доске."""
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece((row, col))
                if piece.get_has_bomb():
                    piece.click()
