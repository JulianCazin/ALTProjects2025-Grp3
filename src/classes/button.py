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
        border_color=(0, 0, 0),
        border_width=0,  # <-- 0 = no border
    ):
        """Create a button. It has x and y coordonates, a width and a height. 
        A text that by default is 'Button'. A text color, a function on press, a color,
        a hover color, a pressed color, a border radius, a border color and a border width.
        A border width of 0 gives no border to the button"""
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
        """Handle the events of the button"""
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

        # We erase and draw the rectangle
        self.button_surface.fill((0, 0, 0, 0))  # transparent
        pg.draw.rect(
            self.button_surface,
            color,
            (0, 0, self.width, self.height),
            border_radius=self.border_radius,
        )
        # Draw the border (if required)
        if self.border_width > 0:
            pg.draw.rect(
                self.button_surface,
                self.border_color,
                (0, 0, self.width, self.height),
                width=self.border_width,
                border_radius=self.border_radius,
            )

        # Center the text
        self.button_surface.blit(
            self.button_surf,
            [
                self.width / 2 - self.button_surf.get_rect().width / 2,
                self.height / 2 - self.button_surf.get_rect().height / 2,
            ],
        )

    def draw(self, screen):
        """Display the button on the selected screen."""
        screen.blit(self.button_surface, self.button_rect)


class BlinkingText:
    def __init__(
        self, text, font_path, size, pos, color=(255, 255, 255), blink_interval=500
    ):
        """Create a blinking text. Used for announcing a new wave"""
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


class Modal:
    def __init__(self, height, width, x=0, y=0):
        """Create a modal. Used for the game over"""
        self.surface = pg.Surface((width, height), pg.SRCALPHA)
        self.rect = pg.Rect(x, y, width, height)
        self.background_color = (0, 0, 0)
        self.opacity = 255
        self.border_radius = 0

    def set_background_color(self, color):
        """Set the background color of the modal"""
        self.background_color = color
        return self

    def set_opacity(self, opacity):
        """Set the opacity of the modal"""
        self.opacity = opacity
        return self

    def set_border_radius(self, radius):
        """Set the border radius of the modal"""
        self.border_radius = radius
        return self

    def draw(self, surface):
        """Render the modal"""
        self.surface.fill((0, 0, 0, 0))  # clear old content
        self.surface.set_alpha(self.opacity)
        pg.draw.rect(
            self.surface,
            self.background_color,
            self.surface.get_rect(),
            border_radius=self.border_radius,
        )
        surface.blit(self.surface, self.rect.topleft)
