import pygame
from homework04.life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.cell_size = cell_size
        super().__init__(life)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.life.cols*self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.life.rows*self.cell_size))
        for y in range(0, self.life.rows*self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.life.cols*self.cell_size, y))

        pass

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for w in range(0, self.life.cols):
            for h in range(0, self.life.rows):
                # print(w//self.cell_size,h//self.cell_size)
                if self.life.curr_generation[h ][w ] == 1:
                    pygame.draw.rect(
                        self.screen, pygame.Color("green"), (w*self.cell_size, h*self.cell_size, self.cell_size, self.cell_size)
                    )
                else:
                    pygame.draw.rect(
                        self.screen, pygame.Color("white"), (w*self.cell_size, h*self.cell_size, self.cell_size, self.cell_size)
                    )
        pass

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen = pygame.display.set_mode((self.life.rows*self.cell_size, self.life.cols*self.cell_size))
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        running = True
        pause=False
        while running:
            # print(123)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if pause:
                        pass
                    pause= not pause
                if event.type == pygame.MOUSEBUTTONUP and pause:
                    pos = pygame.mouse.get_pos()
                    cell_x, cell_y = pos[0] // self.cell_size , pos[1] // self.cell_size
                    if self.life.curr_generation[cell_y][cell_x] == 0:
                        self.life.curr_generation[cell_y][cell_x] = 1
                    else:
                        self.life.curr_generation[cell_y][cell_x] = 0
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(10)
            if not pause:
                self.life.step()


        pygame.quit()
        pass



if __name__ == "__main__":
    life = GameOfLife((50, 50), randomize=True)  # (rows, cols)
    game=GUI(life,cell_size=10)
    game.run()
