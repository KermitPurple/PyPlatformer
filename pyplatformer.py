import pygame
import pygame_tools as pt
from pygame.locals import *

# Don't know if better to create surface, rect tuple list or map
# TODO: refractor

class Player(pygame.sprite.Sprite):

    def __init__(self, pos: pt.Point):
        super().__init__()
        self.surface = pygame.image.load('assets/player.png')
        self.rect = self.surface.get_rect()
        self.rect.topleft = pos
        self.velocity = pt.Point(0, 0)
        self.can_jump = True

    def get_rect(self):
        return self.rect

    def update(self, blocks: [(pygame.Surface, Rect)], gravity: float):
        self.rect.x += self.velocity.x
        if self.velocity.y > 0:
            self.can_jump = False
        for index in self.get_rect().collidelistall([block.rect for block in blocks]):
            if self.velocity.x > 0: # hit wall on right
                self.rect.right = blocks.sprites()[index].rect.left
            elif self.velocity.x < 0: # hit wall on left
                self.rect.left = blocks.sprites()[index].rect.right
        self.rect.y += self.velocity.y
        for index in self.get_rect().collidelistall([block.rect for block in blocks]):
            if self.velocity.y > 0: # hit floor
                self.rect.bottom = blocks.sprites()[index].rect.top
                self.velocity = self.velocity._replace(y = 0)
                self.can_jump = True
            elif self.velocity.y < 0: # hit ceiling
                self.rect.top = blocks.sprites()[index].rect.bottom
                self.velocity = self.velocity._replace(y = 0)
        self.velocity = pt.Point(0, self.velocity.y + gravity)
        if self.velocity.y > 6:
            self.velocity = self.velocity._replace(y = 6)

    def draw(self, surface: pygame.Surface, cell_size: pt.Point, offset: pt.Point):
        surface.blit(self.surface, ((self.rect.x + offset.x, self.rect.y + offset.y), self.rect.size))

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
        self.bg1_rect = Rect(20, 20, 100, 100)
        self.bg1 = pygame.Surface(self.bg1_rect.size)
        self.bg1.fill((12, 150, 12))
        self.bg2_rect = Rect(50, 50, 200, 100)
        self.bg2 = pygame.Surface(self.bg2_rect.size)
        self.bg2.fill((12, 200, 12))

    def draw_paralax(self, surface: pygame.Surface, dest: pt.Point, scale: pt.Point, offset: pt.Point = None):
        if not offset:
            offset = self.camera_offset
        self.screen.blit(surface, (dest.x + offset.x / scale.x, dest.y + offset.y / scale.y))

    def update_camera_offset(self):
        self.camera_offset.x += (self.window_size.x / 2 - self.player.rect.x - self.camera_offset.x) / self.scroll_speed
        self.camera_offset.y += (self.window_size.y / 2 - self.player.rect.y - self.camera_offset.y) / self.scroll_speed

    def get_int_offset(self):
        return pt.Point(int(self.camera_offset.x), int(self.camera_offset.y))

    def update(self):
        self.screen.fill('skyblue')
        self.update_camera_offset()
        self.draw_paralax(self.bg1, self.bg1_rect, pt.Point(20, 20))
        self.draw_paralax(self.bg2, self.bg2_rect, pt.Point(2, 2))
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
