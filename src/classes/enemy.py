import pygame


# Classe représentant un ennemi classic qui se déplace horizontalement et descend d'un cran à chaque bord atteint
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, speed=2):
        super().__init__()
        # Charger l’image de l’alien
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Vitesse horizontale
        self.speed = speed

    def move(self, screen_width):
        """Déplace l'ennemi horizontalement"""
        self.rect.x += self.speed

        # Si on atteint un bord, renvoyer True (signal pour descendre la vague)
        if self.rect.right >= screen_width or self.rect.left <= 0:
            return True
        return False

    def shoot(self, bullet_group, bullet_class, bullet_img):
        """Créer une bullet et ajouter au groupe bullets"""
        bullet = bullet_class(self.rect.centerx, self.rect.bottom, bullet_img, speed=5)
        bullet_group.add(bullet)

    def descend(self, distance=20):
        """Fait descendre l'ennemi d'un cran"""
        self.rect.y += distance

    def update(self, screen_width):
        """Met à jour le mouvement de l'ennemi"""
        edge_reached = self.move(screen_width)
        return edge_reached  # sert au Game Manager

    def draw(self, screen):
        """Affiche l'ennemi à l'écran"""
        screen.blit(self.image, self.rect)
