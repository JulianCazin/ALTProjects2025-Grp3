import pygame
import random


# Classe représentant un ennemi classic qui se déplace horizontalement et descend d'un cran à chaque bord atteint
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, speed=2, boss=False):
        super().__init__()
        # Charger l’image de l’alien
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.boss = boss

        # Vitesse horizontale
        self.speed = speed

        # Timer pour tirs aléatoires
        self.shoot_timer = random.randint(1000, 4000)  # en millisecondes
        self.last_shot_time = pygame.time.get_ticks()

    def move(self, screen_width):
        """Déplace l'ennemi horizontalement"""
        self.rect.x += self.speed

        # Si on atteint un bord, renvoyer True (signal pour descendre la vague)
        if self.rect.right >= screen_width or self.rect.left <= 0:
            return True
        return False

    def descend(self, distance=20):
        """Fait descendre l'ennemi d'un cran"""
        self.rect.y += distance

    def boss_shoot(self, bullet_group, bullet_class, bullet_img):
        """Fait tirer le boss en mode rafale"""
        for offset in [-30, 0, 30]:  # trois tirs en éventail
            bullet = bullet_class(
                x=self.rect.centerx + offset,
                y=self.rect.bottom,
                image_path=bullet_img,
                vy=5,
            )
            bullet_group.add(bullet)

    def try_to_shoot(self, bullet_group, bullet_class, bullet_img):
        """Fait tirer l'ennemi de façon aléatoire selon son timer interne"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_timer:
            bullet = bullet_class(self.rect.centerx, self.rect.bottom, bullet_img, vy=5)
            bullet_group.add(bullet)

            # Réinitialiser le timer avec un nouveau délai aléatoire
            self.last_shot_time = current_time
            self.shoot_timer = random.randint(3000, 8000)  # 3s à 8s entre tirs

    def update(self, screen_width):
        edge_reached = self.move(screen_width)
        return edge_reached
