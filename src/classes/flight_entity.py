import time
import pygame as pg


class FlightEntity(pg.sprite.Sprite):

    def __init__(self, x, y, image_path, vx=0, vy=-8):
        """Create a flight entity. A flight entity is an entity that falls down.
        It has x and y coordonates, a sprite and x and y speed named vx and vy.
        By default vx is equal to 0 and vy is equal to -8"""
        super().__init__()
        # Load bullet's sprite
        self.image = pg.image.load(image_path).convert_alpha()  # Transparency
        self.image = pg.transform.scale(self.image, (50, 30))  # resize
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


class Bonus(FlightEntity):
    SPREAD_SHOT = "SPREAD_SHOT"
    SHIELD = "SHIELD"

    BONUS_LIST = [SPREAD_SHOT, SHIELD]

    def __init__(self, x, y, image_path, vx=0, vy=8):
        """Create a bonus. It has x and y coordonates, a sprite
        and x and y speed named vx and vy. By default, vx is equal to 0
        and vy is equal to 8"""
        super().__init__(x, y, image_path, vx, vy)
        self.type = self.SPREAD_SHOT
        self.point = 100
        self.durability = 10
        self.one_off_use = True
        self.lifetime = 0
        self.start_time = None
        self.__is_reusable = True
        self.__is_used = False

    def set_type(self, type: str):
        """Set the type of the bonus"""
        if type not in self.BONUS_LIST:
            raise Exception(f"This bonus type ({type}) does not exist.")
        self.type = type

    def set_point(self, point: int):
        """Set the point of the bonus"""
        self.point = point

    def set_durability(self, durability: int):
        """Set the durability of the bonus"""
        if durability == 0:
            raise Exception(f"A durability cannot be 0.")
        if durability < 0:
            raise Exception(f"A durability cannot be negative.")
        self.durability = durability

    def set_one_off_use(self, one_off_use: bool):
        """Set if it's a unique usage"""
        self.one_off_use = one_off_use

    def getting_collected(self):
        """Check if the bonus is getting collected"""
        self.is_reusable = False if self.one_off_use else True


class BonusBuilder:
    def __init__(self, x, y, image_path):
        """Create a BonusBuilder. It has x and y coordonates and a sprite
        It is use to easily create a Bonus with set parameters."""
        self._x = x
        self._y = y
        self._image_path = image_path
        self._vx = 0
        self._vy = 8
        self._type = Bonus.SPREAD_SHOT
        self._point = 100
        self._durability = 10
        self._one_off_use = True

    def with_velocity(self, vx, vy):
        """Set the velocity of the bonus to be created"""
        self._vx = vx
        self._vy = vy
        return self

    def with_type(self, bonus_type):
        """Set the type of the bonus to be created"""
        if bonus_type not in Bonus.BONUS_LIST:
            raise Exception(f"Invalid bonus type: {bonus_type}")
        self._type = bonus_type
        return self

    def with_point(self, point):
        """Set the point of the bonus to be created"""
        self._point = point
        return self

    def with_durability(self, durability):
        """Set the durability of the bonus to be created"""
        if durability <= 0:
            raise Exception("Durability must be positive.")
        self._durability = durability
        return self

    def with_lifetime(self, lifetime):
        """Set the lifetime of the bonus to be created"""
        if lifetime <= 0:
            raise Exception("Lifetime must be positive.")
        self._lifetime = lifetime
        return self

    def one_off(self, is_one_off=True):
        """Set if the bonus to be created will have a unique usage"""
        self._one_off_use = is_one_off
        return self

    def build(self):
        """Build the bonus"""
        bonus = Bonus(self._x, self._y, self._image_path, self._vx, self._vy)
        bonus.set_type(self._type)
        bonus.set_point(self._point)
        bonus.set_durability(self._durability)
        bonus.set_one_off_use(self._one_off_use)
        bonus.lifetime = getattr(self, "_lifetime", 0)
        return bonus


class BonusDirector:
    @staticmethod
    def create_spread_shot_bonus(x, y):
        """Create a spread shot bonus at the coordonates"""
        return (
            BonusBuilder(x, y, "src/assets/triple_bonus.png")
            .with_type(Bonus.SPREAD_SHOT)
            .with_point(300)
            .with_durability(5)
            .one_off(True)
            .with_velocity(0, 6)
            .build()
        )

    @staticmethod
    def create_shield_bonus(x, y):
        """Create a shield bonus at the coordonates"""
        return (
            BonusBuilder(x, y, "src/assets/shield.png")
            .with_type(Bonus.SHIELD)
            .with_point(500)
            .with_durability(1)
            .one_off(False)
            .with_velocity(0, 4)
            .with_lifetime(5)
            .build()
        )
