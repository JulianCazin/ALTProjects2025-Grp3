from classes.button import Button
import pygame as pg


class Screen:
    def __init__(self, game):
        self.game = game
        self.background = pg.image.load("src/assets/background.png")
        self.title_font = pg.font.Font("src/assets/font/space_zinzins.ttf", 96)
        self.font = pg.font.Font("src/assets/font/space_zinzins.ttf", 32)
        self.width, self.height = surface_width, surface_height = (
            self.game.screen.get_size()
        )

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.background, self.background.get_rect())


class MenuScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        button_width = 350
        button_height = 60

        x_center = self.width // 2 - button_width // 2
        y_center = self.width // 2 - button_width // 2

        self.start_button = Button(
            x=x_center,
            y=self.height // 6 + self.height // 6,
            width=button_width,
            height=button_height,
            border_radius=16,
            buttonText="Jouer",
            onclickFunction=self.start_game,
        )
        self.quit_button = Button(
            x=x_center,
            y=self.height // 6 + self.height // 6 + 120,
            width=button_width,
            height=button_height,
            border_radius=16,
            buttonText="Quitter",
            onclickFunction=self.game.quit,
        )

        self.buttons = [self.start_button, self.quit_button]

    def start_game(self):
        self.game.set_screen(GameScreen(self.game))

    def update(self, dt):
        for button in self.buttons:
            button.process()  # Vérifie hover / clic

    def draw(self, surface):
        super().draw(surface)
        title = self.title_font.render("Space Zinzins", True, (255, 255, 255))

        surface_width, surface_height = surface.get_size()
        title_rect = title.get_rect(center=(surface_width // 2, surface_height // 4))

        surface.blit(title, title_rect)

        for button in self.buttons:
            surface.blit(button.buttonSurface, (button.x, button.y))


class GameScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.all_sprites = pg.sprite.Group()

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self, surface):
        super().draw(surface)
        text = self.font.render("Ecran jeu", True, (255, 255, 255))
        surface.blit(text, (100, 100))
        self.all_sprites.draw(surface)
