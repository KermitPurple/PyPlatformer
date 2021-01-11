import pygame
import pygame_tools as pt
from pygame.locals import *

# Don't know if better to create surface, rect tuple list or map

class Player:

    def __init__(self, pos: pt.Point):
        self.surface = pygame.image.load('assets/player.png')
        self.size = pt.Point._make(self.surface.get_size())
        self.pos = pos
        self.velocity = pt.Point(0, 0)

    def get_rect(self):
        return Rect(self.pos, self.size)

    def update(self, blocks: [(pygame.Surface, Rect)], gravity: float):
        self.pos = self.pos._replace(x = self.pos.x + self.velocity.x)
        for index in self.get_rect().collidelistall([block[1] for block in blocks]):
            if self.velocity.x > 0:
                self.pos = self.pos._replace(x = blocks[index][1].left - self.size.x)
            elif self.velocity.x < 0:
                self.pos = self.pos._replace(x  = blocks[index][1].right)
        self.pos = self.pos._replace(y = self.pos.y + self.velocity.y)
        for index in self.get_rect().collidelistall([block[1] for block in blocks]):
            if self.velocity.y > 0:
                self.pos = self.pos._replace(y = blocks[index][1].top - self.size.y)
                self.velocity = self.velocity._replace(y = 0)
            elif self.velocity.y < 0:
                self.pos = self.pos._replace(y = blocks[index][1].bottom)
                self.velocity = self.velocity._replace(y = 0)
        self.velocity = pt.Point(0, self.velocity.y + gravity)

    def draw(self, surface: pygame.Surface, cell_size: pt.Point):
        surface.blit(self.surface, ((self.pos.x, self.pos.y), self.size))

    def jump(self):
        self.velocity = self.velocity._replace(y = self.velocity.y - 4)

class Platformer(pt.GameScreen):

    def __init__(self):
        pygame.init()
        self.grass = pygame.image.load('assets/grass.png')
        self.dirt = pygame.image.load('assets/dirt.png')
        self.cell_size = pt.Point(16, 16)
        pygame.display.set_icon(self.grass)
        pygame.display.set_caption('Platformer test')
        real_size = pt.Point(1000, 600)
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
        #     self.player.velocity = self.player.velocity._replace(y = -self.player.velocity.y)
        # else:
        #     self.player.velocity = self.player.velocity._replace(y = self.player.velocity.y + 0.2)
        self.player.update(self.blocks, 0.2)

    def key_down(self, event: pygame.event.Event):
        if event.key == K_a:
            self.player.velocity = self.player.velocity._replace(x = self.player.velocity.x - 1)
        elif event.key == K_d:
            self.player.velocity = self.player.velocity._replace(x = self.player.velocity.x + 1)
        elif event.key == K_w:
            self.player.jump()

if __name__ == "__main__":
    Platformer().run()
