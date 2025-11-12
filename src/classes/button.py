import pygame as pg


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        button_text="Button",
        text_color=(0, 0, 0, 255),
        on_click_function=None,
        one_press=False,
        color=(255, 255, 255, 255),
        hover_color=(102, 102, 102, 255),
        pressed_color=(51, 51, 51, 255),
        border_radius=0,
        border_color=(0, 0, 0),  # <-- couleur de la bordure
        border_width=0,  # <-- épaisseur de la bordure (0 = pas de bordure)
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click_function = on_click_function
        self.one_press = one_press
        self.already_pressed = False
        self.font = pg.font.SysFont(None, 30)
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width

        self.button_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.button_rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.button_surf = self.font.render(button_text, True, self.text_color)

    def process(self):
        mousePos = pg.mouse.get_pos()
        color = self.color

        if self.button_rect.collidepoint(mousePos):
            color = self.hover_color
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                color = self.pressed_color
                if self.one_press:
                    self.on_click_function()
                elif not self.already_pressed:
                    self.on_click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

        # On efface et on dessine le rectangle
        self.button_surface.fill((0, 0, 0, 0))  # transparent
        pg.draw.rect(
            self.button_surface,
            color,
            (0, 0, self.width, self.height),
            border_radius=self.border_radius,
        )
        # Dessine la bordure (si demandée)
        if self.border_width > 0:
            pg.draw.rect(
                self.button_surface,
                self.border_color,
                (0, 0, self.width, self.height),
                width=self.border_width,
                border_radius=self.border_radius,
            )

        # Centre le texte
        self.button_surface.blit(
            self.button_surf,
            [
                self.width / 2 - self.button_surf.get_rect().width / 2,
                self.height / 2 - self.button_surf.get_rect().height / 2,
            ],
        )

    def draw(self, screen):
        """Affiche le bouton sur l’écran cible."""
        screen.blit(self.button_surface, self.button_rect)


class BlinkingText:
    def __init__(
        self, text, font_path, size, pos, color=(255, 255, 255), blink_interval=500
    ):
        self.font = pg.font.Font(font_path, size)
        self.text_surface = self.font.render(text, True, color)
        self.rect = self.text_surface.get_rect(center=pos)
        self.blink_interval = blink_interval  # en ms
        self.visible = True
        self.last_toggle = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_toggle >= self.blink_interval:
            self.visible = not self.visible
            self.last_toggle = now

    def draw(self, surface):
        if self.visible:
            surface.blit(self.text_surface, self.rect)
