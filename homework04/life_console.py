import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.addstr(0,0,"X"*(self.life.cols+2))
        for i in range(1, self.life.rows+1):
            screen.addstr(i,0, "X")
            screen.addstr(i, self.life.cols+1, "X")
        screen.addstr(self.life.rows+1,0, "X" * (self.life.cols + 2))
        screen.addstr(self.life.rows+2, 0, "")
        pass

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for w in range(1, self.life.cols+1):
            for h in range(1, self.life.rows+1):
                if self.life.curr_generation[h-1][w-1] == 1:
                    screen.addstr(h, w, "O")
                else:
                    screen.addstr(h, w, ". ")
        pass

    def run(self) -> None:
        screen = curses.initscr()
        screen.nodelay(1)
        # PUT YOUR CODE HERE
        running = True
        while running:
            # print(123)
            self.draw_grid(screen)
            self.draw_borders(screen)
            screen.refresh()
            curses.napms(1000)
            screen.clear()
            self.life.step()
            c=screen.getch()
            if c==ord('q'):
                running=False

        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((10, 10), randomize=True)  # (rows, cols)
    game=Console(life)
    game.run()
