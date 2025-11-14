import pygame
import random

from classes.flight_entity import FlightEntity


# Class representing a classic enemy who moves horizontaly and falls down every time it reaches an edge
class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, image_path, speed=3):

        super().__init__()
        # Load alien sprite
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Horizontal speed
        self.speed = speed

        # Timer for random shoots
        self.shoot_timer = random.randint(1000, 4000)  # in milliseconds
        self.last_shot_time = pygame.time.get_ticks()

    def move(self, screen_width):
        """Move enemy horizontaly"""
        self.rect.x += self.speed

        # If we reach an edge, return true (signal to lower the wave)
        if self.rect.right >= screen_width or self.rect.left <= 0:
            return True
        return False

    def descend(self, distance=20):
        """Make enemy goes down a certain value"""
        self.rect.y += distance

    def edge_reached(self):
        """Make enemy goes down and changes his movement orientation"""
        self.descend(70)
        self.speed *= -1

    def try_to_shoot(self, bullet_group):
        """Make the enemy randomly shoots with his intern timer"""

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_timer:
            bullet = FlightEntity(
                self.rect.centerx, self.rect.bottom, "src/assets/enemy_bullet.png", vy=5
            )
            bullet_group.add(bullet)

            # Reset the timer with a new random duration
            self.last_shot_time = current_time
            self.shoot_timer = random.randint(3000, 8000)  # 3s to 8s between shoot

    def update(self, screen_width):
        edge_reached = self.move(screen_width)
        return edge_reached


class BossEnemy(Enemy):
    def __init__(self, x, y, image_path, speed=2):
        super().__init__(x, y, image_path, speed)
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 20  # Boss has more health

    def shoot(self, bullet_group, bullet_img="src/assets/enemy_bullet.png"):
        """Make the boss shooting in blast mode"""
        for offset in [-30, 0, 30]:  # three bullets: left, center, right
            bullet = FlightEntity(
                x=self.rect.centerx + offset,
                y=self.rect.bottom,
                image_path=bullet_img,
                vy=5,
            )
            bullet_group.add(bullet)

    def take_damage(self, amount):
        """Reduce boss health by the given amount"""
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove boss from all groups

    # Override try_to_shoot to shoot more frequently
    def try_to_shoot(self, bullet_group):
        """Make the boss randomly shoots with his intern timer"""

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_timer:
            self.shoot(bullet_group)

            # Reset the timer with a new random duration
            self.last_shot_time = current_time
            self.shoot_timer = random.randint(800, 2000)  # 0.8s to 2s between shoot

    def update(self, screen_width):
        edge_reached = self.move(screen_width)
        return edge_reached
