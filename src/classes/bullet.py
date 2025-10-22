import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, image_path, vx=0, vy=-8):
        super().__init__()
        # Charger l’image de la balle
        self.image = pygame.image.load(image_path).convert_alpha()  # Transparence
        self.image = pygame.transform.scale(self.image, (50, 30))  # redimensionner
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vx = vx
        self.vy = vy

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Réduction de la hitbox
        hitbox_scale = 0.5  # 50 % plus petite
        self.rect.width = int(self.rect.width * (hitbox_scale**3))
        self.rect.height = int(self.rect.height * hitbox_scale)
        self.rect.centerx = x  # recaler le centre
        self.rect.bottom = y

    def update(self):
        """Met à jour la position de la balle"""
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Supprimer la balle si elle sort de l’écran
        if self.rect.bottom < 0:
            self.kill()
