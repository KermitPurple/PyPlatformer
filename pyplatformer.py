import pygame
import pygame_tools as pt

class Platformer(pt.GameScreen):

    def __init__(self):
        pygame.init()
        self.grass = pygame.image.load('assets/grass.png')
        self.dirt = pygame.image.load('assets/dirt.png')
        self.cell_size = pt.Point(16, 16)
        pygame.display.set_icon(self.grass)
        pygame.display.set_caption('Platformer test')
        real_size = pt.Point(800, 600)
        size = pt.Point(real_size.x // 4, real_size.y // 4)
        super().__init__(pygame.display.set_mode(real_size), real_size, size)
        self.map = self.load_map('assets/map.txt')

    def load_map(self, path) -> [int]:
        with open(path, 'r') as f:
            return [[int(char) for char in row if char != '\n'] for row in f]

    def update(self):
        self.screen.fill('skyblue')
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == 1 or cell == 2:
                    self.screen.blit(self.grass if cell == 1 else self.dirt, (j * self.cell_size.x, i * self.cell_size.y))

if __name__ == "__main__":
    Platformer().run()
