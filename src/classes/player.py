import pygame
from classes.effects import EffectsManager


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image_path):
        super().__init__()
        # Load player's sprite
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))  # resize
        self.rect = self.image.get_rect(center=(x, y))
        old_center = self.rect.center
        self.rect.inflate_ip(-self.rect.width * 0.3, -self.rect.height * 0.3)
        self.rect.center = old_center
        self.effect = EffectsManager()

        # game variables
        self.speed = speed
        self.lives = 3
        self.score = 0

    # movements and actions functions
    def update(self, screen_width):
        """Update player's position according to the keys pressed"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    # Basic shooting function
    def shoot_basic(self, bullet_group, bullet_class, bullet_img):
        """Create a bullet and add to the bullets group"""
        bullet = bullet_class(self.rect.centerx, self.rect.top, bullet_img)
        bullet_group.add(bullet)
        self.effect.play_shoot()  # jouer le son de tir

    # Spread shooting function

    def shoot_spread(self, bullet_group, bullet_class, bullet_img):
        """
        Create three spreaded bullets :
        - left → diagonal up-left
        - middle → straight line
        - right → diagonal up-right
        """
        self.effect.play_shoot()  # jouer le son de tir
        bullets_data = [
            {"offset": -15, "vx": -3, "vy": -8},  # diagonal left
            {"offset": 0, "vx": 0, "vy": -8},  # straight line
            {"offset": 15, "vx": 3, "vy": -8},  # diagonal right
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

    def add_score(self, score):
        self.score += score

    # decrease the life's number of the player when he is hit by an ennemi
    # before decrease we have to verify than the 
    def player_hit(self, dammage):
        self.lives -= dammage
        if self.lives <= 0:
            self.game.quit()
            

    # Display function
    def draw(self, screen):
        """Display the player on the screen"""
        screen.blit(self.image, self.rect)


