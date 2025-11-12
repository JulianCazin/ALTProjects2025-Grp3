import sys
from classes.button import BlinkingText
from classes.screen import MenuScreen
import pygame as pg

WIDTH, HEIGHT = 960, 540
FPS = 60
BG_COLOR = (18, 18, 20)


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Space Zinzins")

        self.clock = pg.time.Clock()
        self.running = True
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # fenetre fixe

        self.current_screen = MenuScreen(self)

    def set_screen(self, screen):
        self.current_screen = screen

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False

            self.current_screen.handle_events(events)
            self.current_screen.update(dt)
            self.current_screen.draw(self.screen)

            pg.display.flip()

        self.quit()

    def quit(self):
        pg.quit()
        sys.exit()

        self.all_sprites = pg.sprite.Group()

        self.current_screen = MenuScreen(self)

        pg.display.flip()
