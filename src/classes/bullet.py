import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, image_path, vx=0, vy=-8):
        super().__init__()
        # Load bullet's sprite
        self.image = pygame.image.load(image_path).convert_alpha()  # Transparency
        self.image = pygame.transform.scale(self.image, (50, 30))  # resize
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vx = vx
        self.vy = vy

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Reduce hitbox size
        hitbox_scale = 0.5  # 50 % smaller
        self.rect.width = int(self.rect.width * (hitbox_scale**3))
        self.rect.height = int(self.rect.height * hitbox_scale)
        self.rect.centerx = x  # Recenter
        self.rect.bottom = y

    def update(self):
        """Update bullet's position"""
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Delete the bullet if it's outside of the screen
        if self.rect.bottom < 0:
            self.kill()
