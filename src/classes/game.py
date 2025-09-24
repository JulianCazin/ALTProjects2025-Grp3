import sys
import pygame as pg

WIDTH, HEIGHT = 960, 540
FPS = 60
BG_COLOR = (18, 18, 20)

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Pygame Starter")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

        self.all_sprites = pg.sprite.Group()

        self.font = pg.font.SysFont(None, 22)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    def update(self, dt):
        keys = pg.key.get_pressed()
        self.all_sprites.update(dt, keys)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)

        # Petit overlay d’infos
        fps_text = self.font.render(f"FPS: {self.clock.get_fps():.0f}", True, (220, 220, 220))
        help_text = self.font.render("Déplacements: ZQSD / Flèches • ESC pour quitter", True, (180, 180, 180))
        self.screen.blit(fps_text, (10, 10))
        self.screen.blit(help_text, (10, 32))

        pg.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # secondes
            self.handle_events()
            self.update(dt)
            self.draw()

        self.quit()

    def quit(self):
        pg.quit()
        sys.exit(0)