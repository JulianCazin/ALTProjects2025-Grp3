import sys
from src.classes.button import BlinkingText
from src.classes.screen import MenuScreen
import pygame as pg

WIDTH, HEIGHT = 960, 540
FPS = 60
BG_COLOR = (18, 18, 20)


class Game:
    def __init__(self):
        """Create the game"""
        pg.init()
        pg.display.set_caption("Space Zinzins")

        self.clock = pg.time.Clock()
        self.running = True
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # fixed window

        self.current_screen = MenuScreen(self)

    def set_screen(self, screen):
        """Set the current screen"""
        self.current_screen = screen

    def run(self):
        """Run the game"""
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
        """Quit the game"""
        pg.quit()
        sys.exit()

        self.all_sprites = pg.sprite.Group()

        self.current_screen = MenuScreen(self)

        pg.display.flip()
