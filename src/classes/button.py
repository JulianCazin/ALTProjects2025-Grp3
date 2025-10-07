import pygame as pg


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        button_text="Button",
        on_click_function=None,
        one_press=False,
        border_radius=0,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click_function = on_click_function
        self.one_press = one_press
        self.already_pressed = False
        self.font = pg.font.SysFont(None, 30)
        self.border_radius = border_radius

        self.fill_colors = { 
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

        self.button_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.button_rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.button_surf = self.font.render(button_text, True, (20, 20, 20))

    def process(self):
        mouse_pos = pg.mouse.get_pos()
        # Dessiner le rectangle avec coins arrondis
        color = self.fill_colors["normal"]

        if self.button_rect.collidepoint(mouse_pos):
            color = self.fill_colors["hover"]
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                color = self.fill_colors["pressed"]
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

        # On centre le texte
        self.button_surface.blit(
            self.button_surf,
            [
                self.width / 2 - self.button_surf.get_rect().width / 2,
                self.height / 2 - self.button_surf.get_rect().height / 2,
            ],
        )
