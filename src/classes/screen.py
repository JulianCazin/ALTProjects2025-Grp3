import random
from time import sleep
from classes.button import BlinkingText, Button, Modal
import pygame as pg

from classes.player import Player
from classes.flight_entity import BonusDirector, FlightEntity
from classes.enemy import Enemy, BossEnemy
from classes.effects import EffectsManager


PLAYER_IMG = "src/assets/vaisseau.png"
ENEMY_IMG = [
    "src/assets/alien_1.png",
    "src/assets/alien_2.png",
    "src/assets/alien_3.png",
    "src/assets/alien_4.png",
]
BULLET_IMG = "src/assets/bullet.png"

FONT = "src/assets/font/space_zinzins.ttf"


class Screen:
    def __init__(self, game):
        """Create the basic screen"""
        self.game = game

        self.background = pg.image.load("src/assets/background.png")
        self.title_font = pg.font.Font(FONT, 96)
        self.font = pg.font.Font(FONT, 32)
        self.width, self.height = surface_width, surface_height = (
            self.game.screen.get_size()
        )

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        "Put elements on the screen"
        surface.blit(self.background, self.background.get_rect())


class MenuScreen(Screen):
    def __init__(self, game):
        """Create the menu's screen"""
        super().__init__(game)
        button_width = 350
        button_height = 60

        x_center = self.width // 2 - button_width // 2
        y_center = self.height // 2 - button_height // 2

        self.start_button = Button(
            x=x_center,
            y=y_center - 40,
            width=button_width,
            height=button_height,
            border_radius=16,
            button_text="PLAY",
            on_click_function=self.start_game,
        )
        self.quit_button = Button(
            x=x_center,
            y=y_center + 40,
            width=button_width,
            height=button_height,
            border_radius=16,
            button_text="QUIT",
            text_color=(255, 255, 255),
            color=(255, 255, 255, 0),
            border_color=(255, 255, 255),
            border_width=6,
            on_click_function=self.game.quit,
        )

        self.buttons = [self.start_button, self.quit_button]

    def start_game(self):
        """Launch the game"""
        self.game.set_screen(GameScreen(self.game))

    def update(self, dt):
        """Actions to do when an update occured"""
        for button in self.buttons:
            button.process()

    def draw(self, surface):
        """Put elements on the screen"""
        super().draw(surface)
        title = self.title_font.render("Space Zinzins", True, (255, 255, 255))

        surface_width, surface_height = surface.get_size()
        title_rect = title.get_rect(center=(surface_width // 2, surface_height // 4))

        surface.blit(title, title_rect)

        for button in self.buttons:
            surface.blit(button.button_surface, (button.x, button.y))


class GameScreen(Screen):
    def __init__(self, game):
        """Create the game's screen"""
        super().__init__(game)

        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.effects = EffectsManager()
        self.bonus = pg.sprite.Group()
        self.wave = 1

        self.effects.play_music()

        # Player
        self.player = Player(
            x=self.width // 2,
            y=self.height - 50,
            image_path=PLAYER_IMG,
            speed=5,
        )
        self.all_sprites.add(self.player)

        self.waiting_next_wave = False
        self.next_wave_start_time = 0
        self.wait_duration = 2000  # in ms (2 secondes)
        self.wave_text = BlinkingText(
            "NEXT WAVE",
            FONT,
            72,
            (self.width // 2, self.height // 2),
            blink_interval=400,
        )
        self.game_over_text = BlinkingText(
            "GAME OVER",
            FONT,
            72,
            (self.width // 2, self.height // 2),
            blink_interval=600,
        )
        self.is_game_over = False

        self.generate_ennemies(self.wave)

        self.font_score = pg.font.Font(FONT, 36)
        self.font_lives = pg.font.Font(FONT, 36)

    def handle_events(self, events):
        "Handle events that could occurs in the screen"
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot_basic(self.bullets, FlightEntity, BULLET_IMG)
                if event.key == pg.K_LALT:
                    self.player.consum_bonus(self.bullets)

    def generate_ennemies(self, wave):
        """Generate the enemys & boss every 3 waves"""
        boss_wave = wave % 3 == 0
        if boss_wave:
            self.generate_boss()
        for row in range(4):
            enemy_img = random.choice(ENEMY_IMG)
            for col in range(8):
                enemy = Enemy(x=80 + col * 80, y=50 + row * 60, image_path=enemy_img)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        self.enemy_direction = 1

    def generate_boss(self):
        """Generate the boss object & add him to corresponding groups"""
        boss = BossEnemy(
            x=self.width // 2 - 100,
            y=50,
            image_path="src/assets/boss.png",
            speed=2,
        )
        self.effects.play_boss_spawn()
        self.enemies.add(boss)
        self.all_sprites.add(boss)

    def clear_sprites(self):
        """Clear all sprites of the screen"""
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.enemies.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)

    def update(self, dt):
        """Actions to do when an update occured"""
        if self.is_game_over:
            return

        if self.waiting_next_wave:
            self.clear_sprites()
            self.wave_text.update()
            if pg.time.get_ticks() - self.next_wave_start_time > self.wait_duration:
                self.waiting_next_wave = False
                self.generate_ennemies(wave=self.wave)
            return

        self.player.update(self.width)
        self.bullets.update()
        self.bonus.update()

        # Bonus generation
        self.maybe_spawn_bonus()
        self.effects.update()

        edge_reached = False

        # Enemies
        for enemy in self.enemies:
            if enemy.update(self.width):
                edge_reached = True

            enemy.try_to_shoot(self.enemy_bullets)

        if edge_reached:
            for enemy in self.enemies:
                enemy.edge_reached()

        self.enemy_bullets.update()

        # Collisions enemy / bullets
        hits = pg.sprite.groupcollide(
            self.enemies, self.bullets, dokilla=False, dokillb=True
        )

        if hits:
            for enemys in hits:
                enemys.enemy_hit(1)
                self.effects.explosion(enemys.rect.centerx, enemys.rect.centery)
            self.player.add_score(len(hits) * 10)

        # Collisions enemy / player
        if (
            pg.sprite.spritecollideany(self.player, self.enemies)
            and not self.player.almighty
        ):
            self.player.player_hit(1)

        # Collisions player / enemy bullets
        enemy_hits = pg.sprite.spritecollide(
            self.player, self.enemy_bullets, dokill=True
        )
        if enemy_hits and not self.player.almighty:

            self.effects.play_hit()  # play hit sound
            self.player.player_hit(1)

        # when all enemies are defeated (wave cleared)
        if len(self.enemies) == 0 and not self.waiting_next_wave:
            if self.player.lives < 5:
                self.player.lives += 1  # give a bonus life
            self.wave += 1
            self.waiting_next_wave = True
            self.effects.play_wave_clear()  # play wave clear sound
            self.next_wave_start_time = pg.time.get_ticks()

        # Collision player / bonus
        bonus_hits = pg.sprite.spritecollide(self.player, self.bonus, dokill=True)
        if bonus_hits:
            self.player.collect_bonus(bonus_hits[0])
            bonus_hits[0].getting_collected()

        if self.player.lives <= 0:
            self.effects.play_gameover()  # play game over sound
            self.effects.stop_music()
            self.is_game_over = True

    def draw(self, surface):
        """Put elements on the screen"""
        super().draw(surface)
        self.all_sprites.draw(surface)
        self.bullets.draw(surface)
        self.enemy_bullets.draw(surface)
        self.bonus.draw(surface)
        self.player.update_bonus(surface)
        self.effects.draw(surface)

        score_text = self.font_score.render(
            str(self.player.score), True, (255, 255, 255)
        )
        lives_text = self.font_lives.render(
            str(self.player.lives), True, (255, 255, 255)
        )
        surface.blit(score_text, (25, 25))
        surface.blit(lives_text, (self.width - 120, 25))

        if self.waiting_next_wave:
            self.wave_text.draw(surface)

        if self.is_game_over:
            self.game_over_modal(surface)

    def maybe_spawn_bonus(self):
        """Generate bonus randomly based on conditions."""

        MAX_BONUS_ON_SCREEN = 2

        BONUS_SPAWN_CHANCE = 1 / 600

        if len(self.bonus) >= MAX_BONUS_ON_SCREEN:
            return

        if random.random() > BONUS_SPAWN_CHANCE:
            return

        bonus_type = random.choices(
            [BonusDirector.create_shield_bonus, BonusDirector.create_spread_shot_bonus],
            weights=[0.4, 0.6],
        )[0]

        time_bonus = bonus_type(0, 0)

        if not time_bonus.one_off_use and not time_bonus._Bonus__is_reusable:
            return

        x = random.randint(100, self.width - 100)
        y = 0

        bonus = bonus_type(x, y)
        self.bonus.add(bonus)

    def game_over_modal(self, surface):
        """Put the game over modal on the sceen"""
        height = self.game.screen.get_height()
        width = self.game.screen.get_width()
        modal = (
            Modal(height=height, width=width, x=0, y=0)
            .set_background_color((0, 0, 0))
            .set_opacity(160)
        )
        x = self.game.screen.get_width() // 2 - 350 - 25
        y = self.game.screen.get_height() // 2 + 50
        replay_button = Button(
            x=x,
            y=y,
            width=350,
            height=60,
            border_radius=16,
            button_text="REPLAY",
            on_click_function=lambda: self.game.set_screen(GameScreen(self.game)),
        )
        x = self.game.screen.get_width() // 2 + 25
        menu_button = Button(
            x=x,
            y=y,
            width=350,
            height=60,
            border_radius=16,
            button_text="MAIN MENU",
            text_color=(255, 255, 255),
            color=(255, 255, 255, 0),
            border_color=(255, 255, 255),
            border_width=6,
            on_click_function=lambda: self.game.set_screen(MenuScreen(self.game)),
        )

        replay_button.process()
        menu_button.process()

        modal.draw(surface)
        self.game_over_text.draw(surface)
        surface.blit(replay_button.button_surface, (replay_button.x, replay_button.y))
        surface.blit(menu_button.button_surface, (menu_button.x, menu_button.y))
