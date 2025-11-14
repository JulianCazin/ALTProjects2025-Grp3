import time
import pygame as pg

from classes.flight_entity import Bonus, FlightEntity

MAX_BONUS_INVENTORY = 3
from classes.effects import EffectsManager


class Player(pg.sprite.Sprite):

    def __init__(self, x, y, speed, image_path):
        super().__init__()
        self.BONUS_MAPPING = {
            Bonus.SPREAD_SHOT: self.shoot_spread,
            Bonus.SHIELD: self.shield,
        }
        # Load player's sprite
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (100, 100))  # resize
        self.rect = self.image.get_rect(center=(x, y))
        old_center = self.rect.center
        self.rect.inflate_ip(-self.rect.width * 0.3, -self.rect.height * 0.3)
        self.rect.center = old_center
        self.effect = EffectsManager()

        # game variables
        self.speed = speed
        self.lives = 3
        self.score = 0
        self.almighty = False
        self.bonus = []
        self.bonus_group = pg.sprite.Group()

    # movements and actions functions
    def update(self, screen_width):
        """Update player's position according to the keys pressed"""
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    # Basic shooting function
    def shoot_basic(self, bullet_group, bullet_class, bullet_img):
        """Create a bullet and add to the bullets group"""
        bullet = bullet_class(self.rect.centerx, self.rect.top, bullet_img)
        bullet_group.add(bullet)
        self.effect.play_shoot()

    # Spread shooting function

    def shoot_spread(self, *args, **kwargs):
        """
        Create three spreaded bullets :
        - left → diagonal up-left
        - middle → straight line
        - right → diagonal up-right
        """
        from classes.screen import BULLET_IMG

        bullet_group = kwargs.get("bullet_group", None)
        bonus = kwargs.get("bonus", None)

        self.effect.play_shoot()
        bullets_data = [
            {"offset": -15, "vx": -3, "vy": -8},  # diagonal left
            {"offset": 0, "vx": 0, "vy": -8},  # straight line
            {"offset": 15, "vx": 3, "vy": -8},  # diagonal right
        ]

        for data in bullets_data:
            bullet = FlightEntity(
                x=self.rect.centerx + data["offset"],
                y=self.rect.top,
                image_path=BULLET_IMG,
                vx=data["vx"],
                vy=data["vy"],
            )
            bullet_group.add(bullet)
        bonus.durability -= 1

    def shield(self, *args, **kwargs):
        if not self.almighty:
            bonus = kwargs.get("bonus", None)
            bonus.start_time = time.time()

    def add_score(self, score):
        self.score += score

    # decrease the life's number of the player when he is hit by an ennemi
    # before decrease we have to verify than the
    def player_hit(self, dammage):
        self.lives -= dammage

    # Display function
    def update_bonus(self, screen):
        """Display the player on the screen"""
        offset = 20
        for index, bonus in enumerate(self.bonus):
            screen.blit(
                bonus.image,
                (
                    10,
                    screen.get_height() - (bonus.rect.height + offset) * (index + 1),
                ),
            )

        current_bonus = self.bonus[0] if len(self.bonus) > 0 else None
        if current_bonus:
            if current_bonus.type == Bonus.SHIELD:
                if current_bonus.start_time:
                    self.image.set_alpha(128)
                    self.almighty = True
                    if (
                        current_bonus.lifetime > 0
                        and (time.time() - current_bonus.start_time)
                        >= current_bonus.lifetime
                    ):
                        current_bonus.durability = 0
                        self.image.set_alpha(255)
                        self.almighty = False
            else:
                self.image.set_alpha(255)

            if current_bonus.durability == 0:
                self.bonus.remove(current_bonus)
                current_bonus.kill()

    def collect_bonus(self, bonus):
        self.score += bonus.point
        if len(self.bonus) < MAX_BONUS_INVENTORY:
            self.bonus.append(bonus)

    def consum_bonus(self, bullet_group):
        if len(self.bonus) > 0:
            current_bonus = self.bonus[0]
            if current_bonus.durability > 0:
                self.BONUS_MAPPING[current_bonus.type](
                    bullet_group=bullet_group, bonus=current_bonus
                )
