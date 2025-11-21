import pytest
import pygame as pg
from unittest.mock import Mock

from src.classes.flight_entity import FlightEntity
from src.classes.flight_entity import Bonus, BonusBuilder, BonusDirector


# FIXTURE : Mock pygame to avoid loading real images


@pytest.fixture(autouse=True)
def mock_pygame(monkeypatch):
    """Mock pygame image loading + transforms."""

    mock_image = Mock()
    mock_image.get_rect.return_value = pg.Rect(0, 0, 100, 100)

    monkeypatch.setattr(pg.image, "load", lambda path: mock_image)
    monkeypatch.setattr(pg.transform, "scale", lambda img, size: mock_image)

    return mock_image


#               TESTS POUR FLIGHTENTITY


def test_flightentity_init(mock_pygame):
    ent = FlightEntity(50, 100, "fake.png", vx=5, vy=-3)

    assert ent.vx == 5
    assert ent.vy == -3
    assert ent.rect.centerx == 50
    assert ent.rect.bottom == 100

    # Hitbox reduction happened
    assert ent.rect.width < 100
    assert ent.rect.height < 100


def test_flightentity_update_moves():
    ent = FlightEntity(10, 200, "fake.png", vx=3, vy=-4)
    old_x = ent.rect.x
    old_y = ent.rect.y

    ent.update()

    assert ent.rect.x == old_x + 3
    assert ent.rect.y == old_y - 4


def test_flightentity_kill_when_offscreen(monkeypatch):
    ent = FlightEntity(0, 0, "fake.png", vy=-10)

    ent.kill = Mock()
    ent.rect.bottom = -1  # Force it offscreen

    ent.update()
    ent.kill.assert_called_once()


#                       TESTS BONUS


def test_bonus_default_values():
    b = Bonus(10, 10, "img.png")

    assert b.type == Bonus.SPREAD_SHOT
    assert b.point == 100
    assert b.durability == 10
    assert b.one_off_use is True


def test_bonus_set_type_valid():
    b = Bonus(0, 0, "img.png")
    b.set_type(Bonus.SHIELD)
    assert b.type == Bonus.SHIELD


def test_bonus_set_type_invalid():
    b = Bonus(0, 0, "img.png")
    with pytest.raises(Exception):
        b.set_type("INVALID")


def test_bonus_set_durability_valid():
    b = Bonus(0, 0, "img.png")
    b.set_durability(7)
    assert b.durability == 7


def test_bonus_set_durability_invalid_zero():
    b = Bonus(0, 0, "img.png")
    with pytest.raises(Exception):
        b.set_durability(0)


def test_bonus_set_durability_invalid_negative():
    b = Bonus(0, 0, "img.png")
    with pytest.raises(Exception):
        b.set_durability(-5)


def test_bonus_set_one_off_use():
    b = Bonus(0, 0, "img.png")
    b.set_one_off_use(False)
    assert b.one_off_use is False


def test_bonus_getting_collected():
    b = Bonus(0, 0, "img.png")
    b.set_one_off_use(True)
    b.getting_collected()
    assert b.is_reusable is False


#                   TESTS BONUSBUILDER


def test_builder_sets_velocity():
    builder = BonusBuilder(10, 20, "img.png")
    builder.with_velocity(5, 9)
    bonus = builder.build()

    assert bonus.vx == 5
    assert bonus.vy == 9


def test_builder_sets_type_valid():
    builder = BonusBuilder(0, 0, "img.png")
    builder.with_type(Bonus.SHIELD)
    bonus = builder.build()

    assert bonus.type == Bonus.SHIELD


def test_builder_sets_type_invalid():
    builder = BonusBuilder(0, 0, "img.png")
    with pytest.raises(Exception):
        builder.with_type("NOT_A_TYPE")


def test_builder_sets_point():
    b = BonusBuilder(0, 0, "img.png").with_point(777).build()
    assert b.point == 777


def test_builder_sets_durability_valid():
    b = BonusBuilder(0, 0, "img.png").with_durability(3).build()
    assert b.durability == 3


def test_builder_sets_durability_invalid():
    builder = BonusBuilder(0, 0, "img.png")
    with pytest.raises(Exception):
        builder.with_durability(0)


def test_builder_sets_lifetime():
    b = BonusBuilder(0, 0, "img.png").with_lifetime(5).build()
    assert b.lifetime == 5


def test_builder_lifetime_invalid():
    builder = BonusBuilder(0, 0, "img.png")
    with pytest.raises(Exception):
        builder.with_lifetime(0)


def test_builder_one_off_flag():
    b = BonusBuilder(0, 0, "img.png").one_off(False).build()
    assert b.one_off_use is False


#                   TESTS BONUSDIRECTOR


def test_bonus_director_spread_shot():
    b = BonusDirector.create_spread_shot_bonus(50, 60)

    assert b.type == Bonus.SPREAD_SHOT
    assert b.point == 300
    assert b.durability == 5
    assert b.one_off_use is True
    assert b.vx == 0
    assert b.vy == 6


def test_bonus_director_shield():
    b = BonusDirector.create_shield_bonus(20, 30)

    assert b.type == Bonus.SHIELD
    assert b.point == 500
    assert b.durability == 1
    assert b.one_off_use is False
    assert b.lifetime == 5
    assert b.vx == 0
    assert b.vy == 4
