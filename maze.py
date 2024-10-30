import generator_of_maze  # импорт генератора карты лабиринта
import tkinter  # импорт модуля tkinter
from generator_of_maze import EMPTY, WALL, KEY, DOOR  # импорт констант
import time  # импорт модуля time
import datetime  # иморт модуля datetime

WINDOW_BG = 'black'  # задаем цвет бэкграунда окна
PLAYER_COLOR = 'red'  # задаем цвет игрока
MAZE_COLORS = {  # определяем список с цыетами объектов лабиринта
    WALL: 'grey',  # определяем цвет стены
    EMPTY: 'black',  # определяем цвет прохода
    KEY: 'gold',  # определяем цвет ключа
    DOOR: 'brown'  # определяем цвет дверы (выхода)
}
FONT_NAME = 'Impact'  # определяем шрифт текста на конечном экране
FONT_COLOR = 'turquoise1'  # определяем цвет текста на конечном экране


class Game:  # определяем класс Game
    def __init__(self, rows: int, cols: int) -> None:  # определяем конструктор класса
        self.window = tkinter.Tk()  # создаём окно
        self.window.attributes('-fullscreen', True)  # говорим, что окно будет во весь экран
        self.window.bind('<Escape>', lambda event: self.window.destroy())  #  определяем закрытие окна, на esc
        self.window['bg'] = WINDOW_BG,  # присваеваем цвет бэкграуна по константе
        self.cols = cols  # присваеваем атрибуту колонн значение соответствующего аргумента
        self.rows = rows  # присваеваем атрибуту рядов значение соответствующего аргумента
        self.map = None  # создаём отрибут карты
        tile_width = self.window.winfo_screenwidth() // self.cols  # высчитываем ширину одного квадрата на карте
        tile_height = self.window.winfo_screenheight() // self.rows  # высчитываем высоту одного квадрата на карте
        self.tile_size = min(tile_width, tile_height)  # выбираем наименьшее значение из высоты и ширины
        canvas_width = self.tile_size * self.cols  # считаем ширину canvas
        canvas_hight = self.tile_size * self.rows  # считаем высоту canvas
        self.font_size = int(min(canvas_width, canvas_hight) * 0.09)  # высчитываем размер текста
        self.key_id = None  # определяем положение ключа на карте по id
        self.start_time = None  # определяем время начала игры

        self.canvas = tkinter.Canvas(  # создаем canvas
            self.window,  # задаем мастер canvas
            width=self.tile_size * cols,  # задаем ширину canvas
            height=self.tile_size * rows,  # задаем высоту canvas
            highlightthickness=0)  # задаем ширину обводки canvas

        self.canvas.pack(expand=True)  # позиционируем canvas

        self.player = None  # создаем атрибут
        self.window.bind('<Up>', lambda event: self.player.move(-1, 0))  #  определяем движение вверх, на up
        self.window.bind('<Down>', lambda event: self.player.move(1, 0))  #  определяем движение вниз, на down
        self.window.bind('<Right>', lambda event: self.player.move(0, 1))  #  определяем движение вправо, на right
        self.window.bind('<Left>', lambda event: self.player.move(0, -1))  #  определяем движение влево, на left

        self.start()  # вызываем start()
        self.window.mainloop()  # поддерживаем 'жизнь' окна до закрытия

    def start(self) -> None:  # определяем метод start()
        self.start_time = time.time()  # задаем время начала игры
        self.canvas.delete('all')  # очищаем canvas
        self.maze = generator_of_maze.Maze(self.rows, self.cols)  # генерируем лабиринт
        self.map = self.maze.map  # определяем карту лабиринта
        self.player = Player(1, self.rows - 2, PLAYER_COLOR, self)  # создаем экземпляр класса Player
        self.draw_maze()  # вызываем метод draw_maze()
        self.player.draw()  # вызываем метод draw() от класса Player

    def draw_maze(self) -> None:  # определяем метод draw_maze()
        '''отрисовывает на экране лаберинт'''
        row_idx = 0
        for row in self.map:
            col_idx = 0
            for col in row:
                id = self.canvas.create_rectangle(
                    col_idx,
                    row_idx,
                    col_idx + self.tile_size,
                    row_idx + self.tile_size,
                    fill=MAZE_COLORS[col],
                    outline='',
                    )
                if col == KEY:
                    self.key_id = id
                col_idx += self.tile_size
            row_idx += self.tile_size

    def show_screensavers(self) -> None:
        total_microseconds = time.time() - self.start_time
        total_seconds = round(total_microseconds, 2)
        total_time = str(datetime.timedelta(seconds=total_seconds))[0:-4]
        x = self.tile_size * self.cols // 2
        y = self.tile_size * self.rows // 2
        self.canvas.create_text(
            x,
            y,
            fill=FONT_COLOR,
            text=f'{total_time}\nпобеда\nENTER - новая игра\nESC выйти',
            font=(FONT_NAME, self.font_size),
            justify='center'
        )
        self.window.bind('<Return>', lambda event: self.start())  #  определяем начало новой игры с помощью метода start(), на Return


class Player:
    def __init__(self, row: int, col: int, color: str, game: Game) -> None:
        self.col = row
        self.row = col
        self.game = game
        self.size = self.game.tile_size
        self.canvas = self.game.canvas
        self.color = PLAYER_COLOR
        self.is_active = True
        self.has_key = False

    def draw(self) -> None:
        self.game.canvas.create_rectangle(
            self.col * self.size,
            self.row * self.size,
            self.col * self.size + self.size,
            self.row * self.size + self.size,
            fill=self.color,
            outline='',
            tags='player'
        )

    def move(self, d_row: int, d_col: int) -> None:
        if not self.is_active:
            return
        next_col = self.col + d_col
        next_row = self.row + d_row
        if self.game.map[next_row][next_col] == WALL:
            return
        if next_col == self.game.cols - 4 and next_row == 0 and not self.has_key:
            return
        self.col += d_col
        self.row += d_row
        if self.row == self.game.maze.key_row and self.col == self.game.maze.key_col:
            self.has_key = True
            self.canvas.itemconfig(self.game.key_id, fill=MAZE_COLORS[EMPTY])
        self.canvas.delete('player')
        self.draw()
        self.check_victory()

    def check_victory(self) -> None:
        if self.col == self.game.cols - 4 and self.row == 0:
            self.is_active = False
            self.game.show_screensavers()


game = Game(15, 15)
