import pygame
import pygame_tools as pt
from pygame.locals import *

# Don't know if better to create surface, rect tuple list or map

class Player:

    def __init__(self, pos: pt.Point):
        self.surface = pygame.image.load('assets/player.png')
        self.rect = self.surface.get_rect()
        self.rect.topleft = pos
        self.velocity = pt.Point(0, 0)

    def draw(self, surface: pygame.Surface, cell_size: pt.Point):
        surface.blit(self.surface, ((self.rect.x, self.rect.y), self.rect.size))

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
        pygame.key.set_repeat(1000 // self.frame_rate)
        self.map = self.load_map('assets/map.txt')
        self.player = Player(pt.Point(128, 65))
        self.blocks = []
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == 1 or cell == 2:
                    self.blocks.append((self.grass if cell == 1 else self.dirt, Rect((j * self.cell_size.x, i * self.cell_size.y), self.cell_size)))

    def load_map(self, path) -> [int]:
        with open(path, 'r') as f:
            return [[int(char) for char in row if char != '\n'] for row in f]

    def draw_map(self):
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == 1 or cell == 2:
                    self.screen.blit(self.grass if cell == 1 else self.dirt, (j * self.cell_size.x, i * self.cell_size.y))

    def update(self):
        self.screen.fill('skyblue')
        # self.draw_map()
        for block in self.blocks:
            self.screen.blit(block[0], block[1])
        self.player.draw(self.screen, self.cell_size)
        print(self.player.rect.collidelist([block[1] for block in self.blocks]))

    def key_down(self, event: pygame.event.Event):
        if event.key == K_a:
            self.player.rect.x -= 1
        if event.key == K_d:
            self.player.rect.x += 1
        if event.key == K_s:
            self.player.rect.y += 1

if __name__ == "__main__":
    Platformer().run()
