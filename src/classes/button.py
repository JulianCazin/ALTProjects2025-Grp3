import pygame as pg


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        buttonText="Button",
        onclickFunction=None,
        onePress=False,
        border_radius=0,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.font = pg.font.SysFont(None, 30)
        self.border_radius = border_radius

        self.fillColors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

        self.buttonSurface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))

    def process(self):
        mousePos = pg.mouse.get_pos()
        # Dessiner le rectangle avec coins arrondis
        color = self.fillColors["normal"]

        if self.buttonRect.collidepoint(mousePos):
            color = self.fillColors["hover"]
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                color = self.fillColors["pressed"]
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        # On efface et on dessine le rectangle
        self.buttonSurface.fill((0, 0, 0, 0))  # transparent
        pg.draw.rect(
            self.buttonSurface,
            color,
            (0, 0, self.width, self.height),
            border_radius=self.border_radius,
        )

        # On centre le texte
        self.buttonSurface.blit(
            self.buttonSurf,
            [
                self.width / 2 - self.buttonSurf.get_rect().width / 2,
                self.height / 2 - self.buttonSurf.get_rect().height / 2,
            ],
        )
