import pytest
from unittest.mock import patch, MagicMock
import pygame

from src.classes.player import Player
from src.classes.flight_entity import Bonus, FlightEntity


# FIXTURES


@pytest.fixture(autouse=True)
def pygame_init():
    """Initialize pygame modules for tests."""
    pygame.init()


@pytest.fixture
def mock_image():
    """Mock pygame.image.load, convert_alpha, and transform.scale."""
    fake_surface = MagicMock(spec=pygame.Surface)
    fake_surface.convert_alpha.return_value = fake_surface

    with patch("pygame.image.load", return_value=fake_surface) as mocked_load, patch(
        "pygame.transform.scale", return_value=fake_surface
    ) as mocked_scale:
        yield {
            "load": mocked_load,
            "scale": mocked_scale,
            "surface": fake_surface,
        }


@pytest.fixture
def player(mock_image):
    return Player(x=400, y=500, speed=5, image_path="fake.png")


# BASIC TESTS


def test_player_initialization(player):
    assert player.lives == 3
    assert player.score == 0
    assert player.speed == 5
    assert isinstance(player.rect, pygame.Rect)
    assert player.image is not None


def test_player_add_score(player):
    player.add_score(50)
    assert player.score == 50


def test_player_hit(player):
    player.player_hit(1)
    assert player.lives == 2


# MOVEMENT TESTS


def test_player_move_left(player, monkeypatch):
    keys = [0] * 1000
    keys[pygame.K_LEFT] = 1
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys)

    old_x = player.rect.x
    player.update(800)
    assert player.rect.x == old_x - player.speed


def test_player_move_right(player, monkeypatch):
    keys = [0] * 1000
    keys[pygame.K_RIGHT] = 1
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys)

    old_x = player.rect.x
    player.update(800)
    assert player.rect.x == old_x + player.speed


# SHOOTING TESTS


def test_player_shoot_basic(player):
    bullet_group = MagicMock()
    bullet_class = MagicMock()
    bullet_img = "bullet.png"

    player.shoot_basic(bullet_group, bullet_class, bullet_img)

    bullet_class.assert_called_once()
    bullet_group.add.assert_called_once()
    player.effect.play_shoot.assert_called_once()


def test_player_shoot_spread(player):
    bullet_group = MagicMock()

    # Fake bonus
    bonus = MagicMock()
    bonus.durability = 3

    with patch("src.classes.player.FlightEntity") as MockBullet, patch(
        "src.classes.player.BULLET_IMG", "fake_bullet.png"
    ):

        player.shoot_spread(bullet_group=bullet_group, bonus=bonus)

        # 3 bullets
        assert MockBullet.call_count == 3
        assert bullet_group.add.call_count == 3

        # durability reduced
        assert bonus.durability == 2

        player.effect.play_shoot.assert_called_once()


# SHIELD TEST


def test_player_shield(player, monkeypatch):
    bonus = MagicMock()
    bonus.start_time = None

    with patch("time.time", return_value=1000):
        player.shield(bonus=bonus)

    assert bonus.start_time == 1000


# BONUS SYSTEM TESTS


def test_player_collect_bonus(player):
    bonus = MagicMock()
    bonus.point = 10

    player.collect_bonus(bonus)

    assert player.score == 10
    assert bonus in player.bonus


def test_player_collect_bonus_inventory_limit(player):
    b1 = MagicMock()
    b2 = MagicMock()
    b3 = MagicMock()
    b4 = MagicMock()

    for b in (b1, b2, b3):
        player.collect_bonus(b)

    assert len(player.bonus) == 3

    # fourth should NOT be added
    player.collect_bonus(b4)
    assert len(player.bonus) == 3
    assert b4 not in player.bonus


def test_player_consume_bonus(player):
    bullet_group = MagicMock()

    # Create a mock SPREAD_SHOT bonus
    bonus = MagicMock()
    bonus.type = Bonus.SPREAD_SHOT
    bonus.durability = 2
    player.bonus.append(bonus)

    with patch.object(player, "shoot_spread") as mock_shoot:
        player.consum_bonus(bullet_group)

        mock_shoot.assert_called_once()
        assert bonus.durability == 2  # durability handled inside shoot_spread


# UPDATE BONUS (shield timeout)


def test_player_update_bonus_shield_expired(player, monkeypatch):
    # mock screen
    screen = MagicMock()
    screen.get_height.return_value = 600

    bonus = MagicMock()
    bonus.type = Bonus.SHIELD
    bonus.start_time = 100
    bonus.lifetime = 5
    bonus.durability = 1
    bonus.image = MagicMock()
    bonus.rect = pygame.Rect(0, 0, 10, 10)

    player.bonus.append(bonus)

    # simulate time passed
    monkeypatch.setattr("time.time", lambda: 200)

    player.update_bonus(screen)

    # durability should now be zero → bonus removed
    assert bonus not in player.bonus
    assert player.almighty is False
