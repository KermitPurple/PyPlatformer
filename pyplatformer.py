import pygame
import pygame_tools as pt
from pygame.locals import *

# Don't know if better to create surface, rect tuple list or map
# TODO: refractor

class Player:

    def __init__(self, pos: pt.Point):
        self.surface = pygame.image.load('assets/player.png')
        self.size = pt.Point._make(self.surface.get_size())
        self.pos = pos
        self.velocity = pt.Point(0, 0)
        self.can_jump = True

    def get_rect(self):
        return Rect(self.pos, self.size)

    def update(self, blocks: [(pygame.Surface, Rect)], gravity: float):
        self.pos = self.pos._replace(x = self.pos.x + self.velocity.x)
        if self.velocity.y > 0:
            self.can_jump = False
        for index in self.get_rect().collidelistall([block[1] for block in blocks]):
            if self.velocity.x > 0:
                self.pos = self.pos._replace(x = blocks[index][1].left - self.size.x)
            elif self.velocity.x < 0:
                self.pos = self.pos._replace(x  = blocks[index][1].right)
        self.pos = self.pos._replace(y = self.pos.y + self.velocity.y)
        for index in self.get_rect().collidelistall([block[1] for block in blocks]):
            if self.velocity.y > 0: # hit floor
                self.pos = self.pos._replace(y = blocks[index][1].top - self.size.y)
                self.velocity = self.velocity._replace(y = 0)
                self.can_jump = True
            elif self.velocity.y < 0:
                self.pos = self.pos._replace(y = blocks[index][1].bottom)
                self.velocity = self.velocity._replace(y = 0)
        self.velocity = pt.Point(0, self.velocity.y + gravity)
        if self.velocity.y > 6:
            self.velocity = self.velocity._replace(y = 6)

    def draw(self, surface: pygame.Surface, cell_size: pt.Point, offset: pt.Point):
        surface.blit(self.surface, ((self.pos.x + offset.x, self.pos.y + offset.y), self.size))

    def jump(self):
        if self.can_jump:
            self.velocity = self.velocity._replace(y = -4)
            self.can_jump = False

class Platformer(pt.GameScreen):

    def __init__(self):
        pygame.init()
        self.cell_size = pt.Point(16, 16)
        self.world = pt.World(
                'assets/map.txt',
                {
                    0: None,
                    1: pygame.image.load('assets/grass.png'),
                    2: pygame.image.load('assets/dirt.png'),
                    },
                self.cell_size,
                )
        pygame.display.set_icon(pygame.image.load('assets/grass.png'))
        pygame.display.set_caption('Platformer test')
        real_size = pt.Point(1000, 600)
        size = pt.Point(real_size.x // 4, real_size.y // 4)
        super().__init__(pygame.display.set_mode(real_size), real_size, size)
        pygame.key.set_repeat(1000 // self.frame_rate)
        self.player = Player(pt.Point(128, 65))
        self.blocks = self.world.blocks
        self.camera_offset = pt.Point(5, 5)
        self.scroll_speed = 15

    def update_camera_offset(self):
        self.camera_offset = pt.Point(self.camera_offset.x + (self.window_size.x / 2 - self.player.pos.x - self.camera_offset.x) / self.scroll_speed, self.camera_offset.y + (self.window_size.y / 2 - self.player.pos.y - self.camera_offset.y) / self.scroll_speed)

    def get_int_offset(self):
        return pt.Point(int(self.camera_offset.x), int(self.camera_offset.y))

    def update(self):
        self.screen.fill('skyblue')
        self.update_camera_offset()
        self.world.draw_blocks(self.screen, offset = self.get_int_offset())
        self.player.draw(self.screen, self.cell_size, self.get_int_offset())
        self.player.update(self.blocks, 0.2)
        self.keyboard_input()

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.player.velocity = self.player.velocity._replace(x = -2)
        if keys[K_d]:
            self.player.velocity = self.player.velocity._replace(x = 2)
        if keys[K_w]:
            self.player.jump()

if __name__ == "__main__":
    Platformer().run()
