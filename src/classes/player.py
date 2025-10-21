import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image_path):
        super().__init__()
        # Charger le sprite du joueur
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))  # redimensionner
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # variables de jeu
        self.speed = speed
        self.lives = 3
        self.score = 0

    # fonctions de mouvement et d’action
    def update(self, screen_width):
        """Met à jour la position du joueur selon les touches pressées"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    # fonction de tir basique
    def shoot_basic(self, bullet_group, bullet_class, bullet_img):
        """Créer une bullet et ajouter au groupe bullets"""
        bullet = bullet_class(self.rect.centerx, self.rect.top, bullet_img)
        bullet_group.add(bullet)

    # fonction de tir en éventail

    def shoot_spread(self, bullet_group, bullet_class, bullet_img):
        """
        Crée trois balles en éventail :
        - gauche → diagonale haut-gauche
        - milieu → tout droit vers le haut
        - droite → diagonale haut-droite
        """
        bullets_data = [
            {"offset": -15, "vx": -3, "vy": -8},  # diagonale gauche
            {"offset": 0, "vx": 0, "vy": -8},  # tout droit
            {"offset": 15, "vx": 3, "vy": -8},  # diagonale droite
        ]

        for data in bullets_data:
            bullet = bullet_class(
                x=self.rect.centerx + data["offset"],
                y=self.rect.top,
                image_path=bullet_img,
                vx=data["vx"],
                vy=data["vy"],
            )
            bullet_group.add(bullet)

    # fonctions d’affichage
    def draw(self, screen):
        """Affiche le joueur sur le screen"""
        screen.blit(self.image, self.rect)
