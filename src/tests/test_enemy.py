import pytest
import pygame
from unittest.mock import patch, MagicMock

from src.classes.enemy import Enemy, BossEnemy


@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    pygame.display.set_mode((1, 1))  # minimal display for tests
    yield
    pygame.quit()


@pytest.fixture
def mock_image():
    """Mock pygame.image.load so no real file is read."""
    with patch("pygame.image.load") as mocked_load, patch(
        "pygame.transform.scale"
    ) as mocked_scale:

        surf = pygame.Surface((10, 10)).convert_alpha()
        mocked_load.return_value = surf
        mocked_scale.return_value = surf

        yield


@pytest.fixture
def enemy(mock_image):
    return Enemy(x=50, y=50, image_path="fake.png", speed=5)


@pytest.fixture
def boss(mock_image):
    return BossEnemy(x=100, y=100, image_path="fake.png", speed=2)


# TEST Enemy CLASS


def test_enemy_initialization(enemy):
    assert enemy.rect.x == 50
    assert enemy.rect.y == 50
    assert enemy.speed == 5
    assert enemy.health == 1


def test_enemy_move_no_edge(enemy):
    screen_width = 800
    result = enemy.move(screen_width)
    assert result is False
    assert enemy.rect.x == 55  # moved by speed


def test_enemy_move_hits_right_edge(enemy):
    enemy.rect.x = 790  # 790 + 10 = 800 (right edge)
    result = enemy.move(800)
    assert result is True


def test_enemy_descend(enemy):
    enemy.descend(40)
    assert enemy.rect.y == 90


def test_enemy_edge_reached(enemy):
    old_speed = enemy.speed
    old_y = enemy.rect.y

    enemy.edge_reached()

    assert enemy.rect.y == old_y + 70
    assert enemy.speed == -old_speed


def test_enemy_hit_survives(enemy):
    died = enemy.enemy_hit(0.5)
    assert died is False
    assert enemy.health == 0.5


def test_enemy_hit_death(enemy):
    # Mock explosion effect
    enemy.effects.play_explosion = MagicMock()

    died = enemy.enemy_hit(1)
    assert died is True
    assert enemy.health <= 0
    enemy.effects.play_explosion.assert_called_once()


def test_enemy_try_to_shoot(enemy):
    bullet_group = pygame.sprite.Group()

    with patch("pygame.time.get_ticks", return_value=5000):
        enemy.last_shot_time = 0
        enemy.shoot_timer = 1000  # so shooting is allowed

        enemy.try_to_shoot(bullet_group)

    assert len(bullet_group) == 1  # shot once


# TEST BossEnemy CLASS


def test_boss_initialization(boss):
    assert boss.health == 5
    assert boss.rect.x == 100
    assert boss.rect.y == 100


def test_boss_shoot(boss):
    bullet_group = pygame.sprite.Group()

    boss.shoot(bullet_group)

    assert len(bullet_group) == 3  # three bullets


def test_boss_try_to_shoot(boss):
    bullet_group = pygame.sprite.Group()

    with patch("pygame.time.get_ticks", return_value=5000):
        boss.last_shot_time = 0
        boss.shoot_timer = 500  # allow shooting

        boss.try_to_shoot(bullet_group)

    assert len(bullet_group) == 3  # boss shoots 3 bullets each time
