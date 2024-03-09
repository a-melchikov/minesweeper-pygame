# piece.py
class Piece:
    def __init__(self, has_bomb):
        """
        Конструктор класса Piece.

        :param has_bomb: Флаг, указывающий, есть ли бомба в данном кусочке.
        """
        self.neighbors = None
        self.num_around = None
        self.has_bomb = has_bomb
        self.clicked = False
        self.flagged = False

    def get_has_bomb(self):
        """Возвращает True, если в этом кусочке есть бомба."""
        return self.has_bomb

    def get_clicked(self):
        """Возвращает True, если этот кусочек был кликнут."""
        return self.clicked

    def get_flagged(self):
        """Возвращает True, если на этот кусочек поставлена флаг."""
        return self.flagged

    def set_neighbors(self, neighbors):
        """
        Устанавливает соседей для данного кусочка и вычисляет количество бомб вокруг.

        :param neighbors: Список соседних кусочков.
        """
        self.neighbors = neighbors
        self.set_num_around()

    def set_num_around(self):
        """Вычисляет количество бомб вокруг данного кусочка."""
        self.num_around = sum(1 for piece in self.neighbors if piece.get_has_bomb())

    def get_num_around(self):
        """Возвращает количество бомб вокруг данного кусочка."""
        return self.num_around

    def toggle_flag(self):
        """Переключает флаг на этом кусочке."""
        self.flagged = not self.flagged

    def click(self):
        """Обрабатывает клик на этом кусочке."""
        self.clicked = True

    def get_neighbors(self):
        """Возвращает соседей данного кусочка."""
        return self.neighbors
