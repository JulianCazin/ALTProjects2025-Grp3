import pygame as pg

class Screen:
    def __init__(self, game):
        self.game = game

        self.background = pg.image.load('src/assets/background.png')

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.background, self.background.get_rect())


class MenuScreen(Screen):
    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.game.set_screen(GameScreen(self.game))

    def draw(self, surface):
        super().draw(surface)
        text = self.game.font.render("Appuie sur Entrée pour jouer", True, (255,255,255))
        surface.blit(text, (100, 100))


class GameScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.all_sprites = pg.sprite.Group()

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self, surface):
        super().draw(surface)
        self.all_sprites.draw(surface)
