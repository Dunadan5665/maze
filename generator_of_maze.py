from random import choice
WALL = '█'
EMPTY = '░'
KEY = 'K'
DOOR = 'D'


class Maze:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows - 2
        self.cols = cols - 2
        self.is_ready = False
        self.map = []
        self.make_walls()
        self.make_path()
        self.make_borders()
        self.make_exit()
        self.key_row = None
        self.key_row = None
        self.make_key()
        self.show_map()
        self.rows = rows + 2
        self.cols = cols + 2

    def make_walls(self) -> None:
        for i in range(self.rows):
            self.map.append([WALL] * self.cols)

    def show_map(self) -> None:
        for row in self.map:
            print(*row, sep='')

    def __str__(self) -> str:
        '''показывает лаберинт в консоли'''
        map = ''
        for row in self.map:
            map += ''.join(row) + '/n'
        return map[:-1] + ''

    def check_path(self) -> None:
        '''если в каждой четной клетке нет стены, лаберинт проходим'''
        for row in range(0, self.rows, 2):
            for col in range(0, self.cols, 2):
                if self.map[row][col] == WALL:
                    return
        self.is_ready = True

    def make_borders(self) -> None:
        '''окружает стенами'''
        for row in self.map:
            row.insert(0, WALL)
            row.append(WALL)
        self.map.insert(0, [WALL] * (self.cols + 2))
        self.map.append([WALL] * (self.cols + 2))

    def make_exit(self) -> None:
        self.map[0][self.cols - 2] = DOOR

    def make_path(self) -> None:
        '''пробивает стену в лаберинте'''
        self.bulldozer_row = choice(range(2, self.rows, 2))
        self.bulldozer_col = choice(range(2, self.cols, 2))
        self.map[self.bulldozer_row][self.bulldozer_col] = EMPTY

        while not self.is_ready:
            all_directions = []
            if self.bulldozer_col < self.cols - 2:
                all_directions.append((0, 2))
            if self.bulldozer_col > 0:
                all_directions.append((0, -2))
            if self.bulldozer_row > 0:
                all_directions.append((-2, 0))
            if self.bulldozer_row < self.rows - 2:
                all_directions.append((2, 0))

            direction = choice(all_directions)

            if self.map[
                self.bulldozer_row + direction[0]
                ][
                    self.bulldozer_col + direction[1]
                    ] == WALL:
                # в любую сторону
                self.map[
                    self.bulldozer_row + direction[0] // 2
                    ][
                        self.bulldozer_col + direction[1] // 2
                        ] = EMPTY
                self.map[
                    self.bulldozer_row + direction[0]
                    ][
                        self.bulldozer_col + direction[1]
                        ] = EMPTY

            self.bulldozer_row += direction[0]
            self.bulldozer_col += direction[1]
            self.check_path()

    def make_key(self):
        self.key_row = choice(range(1, self.rows - 1, 2))
        self.key_col = choice(range(3, self.cols - 2, 2))
        self.map[self.key_row][self.key_col] = KEY
