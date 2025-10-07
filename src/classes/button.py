import pygame as pg

class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        buttonText="Button",
        text_color=(0, 0, 0, 255),
        onclickFunction=None,
        onePress=False,
        color=(255, 255, 255, 255),
        hover_color=(102, 102, 102, 255),
        pressed_color=(51, 51, 51, 255),
        border_radius=0,
        border_color=(0, 0, 0),     # <-- couleur de la bordure
        border_width=0              # <-- épaisseur de la bordure (0 = pas de bordure)
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.font = pg.font.SysFont(None, 30)
        self.text_color=text_color
        self.color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width

        self.buttonSurface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = self.font.render(buttonText, True, self.text_color)

    def process(self):
        mousePos = pg.mouse.get_pos()
        color = self.color

        if self.buttonRect.collidepoint(mousePos):
            color = self.hover_color
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                color = self.pressed_color
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        # Efface le contenu précédent (transparent)
        self.buttonSurface.fill((0, 0, 0, 0))

        # Dessine le fond
        pg.draw.rect(
            self.buttonSurface,
            color,
            (0, 0, self.width, self.height),
            border_radius=self.border_radius,
        )

        # Dessine la bordure (si demandée)
        if self.border_width > 0:
            pg.draw.rect(
                self.buttonSurface,
                self.border_color,
                (0, 0, self.width, self.height),
                width=self.border_width,
                border_radius=self.border_radius,
            )

        # Centre le texte
        self.buttonSurface.blit(
            self.buttonSurf,
            [
                self.width / 2 - self.buttonSurf.get_rect().width / 2,
                self.height / 2 - self.buttonSurf.get_rect().height / 2,
            ],
        )

    def draw(self, screen):
        """Affiche le bouton sur l’écran cible."""
        screen.blit(self.buttonSurface, self.buttonRect)
