from random import choice

WALL = '█'
EMPTY = '░'

rows = int(input('Введите кол-во рядов: '))
cols = int(input('Введите кол-во колонн: '))


class Maze:
    def __init__(self, wall=WALL, rows=rows, cols=cols) -> None:
        self.wall = wall
        self.rows = rows
        self.cols = cols
        self.is_ready = False
        self.map = self.create_map()
        self.make_path()
        self.show_map()

    def create_map(self) -> list:
        '''Создаёт карту лабиринта, наполненную стенами'''
        map = []
        for i in range(self.rows):
            map.append([self.wall] * self.cols)
        return map

    def show_map(self) -> None:
        '''Показывает карту лабиринта в консоли'''
        for row in self.map:
            print(*row, sep='')

    def make_path(self) -> None:
        '''
        Пробивает стены лабиринта - делает его проходимым
        Ставит бульдозер в случайную четную клетку не на краю
        Бульдозер сразу ломает стену в той клетке, где появился
        В цикле бульдозера:
            выбирает направление из четырех возможных
            делает 2 шага
            выберает новое направление

        '''
        self.bulldozer_row = choice(range(2, self.rows, 2))
        self.bulldozer_col = choice(range(2, self.cols, 2))
        self.map[self.bulldozer_row][self.bulldozer_col] = EMPTY

        while not self.is_ready:
            directions = []
            if self.bulldozer_col < self.cols - 2:
                directions.append((0, 2))
            if self.bulldozer_col > 0:
                directions.append((0, -2))
            if self.bulldozer_row > 0:
                directions.append((-2, 0))
            if self.bulldozer_row < self.rows - 2:
                directions.append((2, 0))

            mazedirection = choice(directions)

            if self.map[self.bulldozer_row + mazedirection[0]][
                self.bulldozer_col + mazedirection[1]
            ] == WALL:
                self.map[self.bulldozer_row + mazedirection[0] // 2][
                    self.bulldozer_col + mazedirection[1] // 2
                ] = EMPTY
                self.map[self.bulldozer_row + mazedirection[0]][
                    self.bulldozer_col + mazedirection[1]
                ] = EMPTY
            self.bulldozer_row += mazedirection[0]
            self.bulldozer_col += mazedirection[1]

            if self.check_is_ready():
                self.is_ready = True

        self.create_walls()
        self.make_exit()

    def check_is_ready(self) -> bool:
        '''
        Проверяет, не стал ли лабиринт проходимым
        Т.е. все чётные клетки пустые
        '''
        for i in range(0, self.rows, 2):
            for j in range(0, self.cols, 2):
                if self.map[i][j] != EMPTY:
                    return False
        return True

    def create_walls(self):
        '''
        Окружает внутренний лабиринт вне стенами
        '''
        self.map.insert(0, [self.wall] * self.cols)
        self.map.append([self.wall] * self.cols)
        for i in self.map:
            self.map[self.map.index(i)].append(self.wall)
            self.map[self.map.index(i)].insert(0, self.wall)

        if self.rows % 2 == 0:
            self.map[self.rows + 1].clear()

        if self.cols % 2 == 0:
            for i in range(self.rows + 1):
                self.map[i].pop()
            if self.rows % 2 != 0:
                self.map[self.rows + 1].pop()

    def make_exit(self) -> None:
        if self.cols % 2 != 0:
            self.map[0][self.cols] = EMPTY

        elif self.cols % 2 == 0:
            self.map[0][self.cols - 1] = EMPTY
