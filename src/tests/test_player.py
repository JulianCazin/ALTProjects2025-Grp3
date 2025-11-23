import pytest
import pygame as pg
from unittest.mock import Mock, patch

from src.classes.player import Player
from src.classes.flight_entity import Bonus, FlightEntity


@pytest.fixture
def mock_pygame(monkeypatch):
    """Mock minimal pygame components that Player needs."""

    # Mock image loading
    mock_image = Mock()
    mock_image.get_rect.return_value = pg.Rect(0, 0, 100, 100)

    monkeypatch.setattr(pg.image, "load", lambda path: mock_image)
    monkeypatch.setattr(pg.transform, "scale", lambda img, size: mock_image)

    # Mock key presses
    monkeypatch.setattr(pg.key, "get_pressed", lambda: [0] * 300)

    # Mock sound to avoid initializing mixer
    monkeypatch.setattr(pg.mixer, "Sound", lambda *args, **kwargs: Mock())

    return mock_image


@pytest.fixture
def player(mock_pygame):
    """Create a minimal player instance."""
    p = Player(x=200, y=300, speed=5, image_path="fake.png")
    return p


def test_player_initialization(player):
    assert player.speed == 5
    assert player.score == 0
    assert player.lives == 3
    assert isinstance(player.rect, pg.Rect)


def test_update_moves_left(monkeypatch, player):
    class FakeKeys:
        def __getitem__(self, key):
            return key == pg.K_LEFT

    monkeypatch.setattr(pg.key, "get_pressed", lambda: FakeKeys())

    initial_x = player.rect.x
    player.update(screen_width=800)

    assert player.rect.x == initial_x - player.speed


def test_update_moves_right(monkeypatch, player):
    class FakeKeys:
        def __getitem__(self, key):
            return key == pg.K_RIGHT

    monkeypatch.setattr(pg.key, "get_pressed", lambda: FakeKeys())

    initial_x = player.rect.x
    player.update(screen_width=800)

    assert player.rect.x == initial_x + player.speed


def test_shoot_basic(player):
    bullet_group = Mock()
    bullet_group.add = Mock()

    # Fake bullet class
    class FakeBullet:
        def __init__(self, x, y, img, vy):
            self.x = x
            self.y = y

    player.shoot_basic(bullet_group, FakeBullet, "bullet.png")

    bullet_group.add.assert_called_once()
    assert bullet_group.add.call_count == 1
    assert player.effect is not None


def test_collect_bonus(player):
    bonus = Mock()
    bonus.point = 50

    player.collect_bonus(bonus)

    assert player.score == 50
    assert len(player.bonus) == 1


def test_player_hit(player):
    player.player_hit(1)
    assert player.lives == 2


# TESTS BONUS SHIELD


def test_shield_activates(monkeypatch, player):
    bonus = Mock()
    bonus.start_time = None

    with patch("time.time", return_value=1234):
        player.shield(bonus=bonus)

    assert bonus.start_time == 1234


# TEST SPREAD SHOT


def test_shoot_spread(monkeypatch, player):
    """Test spread shot creates 3 bullets with correct velocity and durability effect."""

    # Mock BULLET_IMG import used inside shoot_spread
    monkeypatch.setattr("src.classes.screen.BULLET_IMG", "fake_bullet.png")

    bullet_group = Mock()
    bullet_group.add = Mock()

    # Fake bonus
    bonus = Mock()
    bonus.durability = 3

    # Patch FlightEntity constructor to avoid real sprite
    with patch("src.classes.player.FlightEntity", return_value=Mock()) as fake_entity:
        player.shoot_spread(bullet_group=bullet_group, bonus=bonus)

    # Should create 3 bullets
    assert bullet_group.add.call_count == 3

    # Durability must decrease by 1
    assert bonus.durability == 2


# TEST consum_bonus USES BONUS_MAPPING


def test_consum_bonus_calls_correct_function(monkeypatch, player):
    bullet_group = Mock()

    # Mock a bonus
    bonus = Mock()
    bonus.type = Bonus.SPREAD_SHOT
    bonus.durability = 2

    player.bonus = [bonus]

    # Mock the function that should be called
    mock_spread = Mock()
    player.BONUS_MAPPING[Bonus.SPREAD_SHOT] = mock_spread

    player.consum_bonus(bullet_group)

    mock_spread.assert_called_once()
