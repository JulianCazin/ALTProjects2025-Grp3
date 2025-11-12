import random
from classes.button import Button
import pygame as pg

from classes.player import Player
from classes.bullet import Bullet
from classes.enemy import Enemy
from classes.effects import EffectsManager


PLAYER_IMG = "src/assets/vaisseau.png"
ENEMY_IMG = [
    "src/assets/alien_1.png",
    "src/assets/alien_2.png",
    "src/assets/alien_3.png",
    "src/assets/alien_4.png",
]
BULLET_IMG = "src/assets/bullet.png"


class Screen:
    def __init__(self, game):
        self.game = game

        self.background = pg.image.load("src/assets/background.png")
        self.title_font = pg.font.Font("src/assets/font/space_zinzins.ttf", 96)
        self.font = pg.font.Font("src/assets/font/space_zinzins.ttf", 32)
        self.width, self.height = surface_width, surface_height = (
            self.game.screen.get_size()
        )

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.background, self.background.get_rect())


class MenuScreen(Screen):
    def __init__(self, game):
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
        self.game.set_screen(GameScreen(self.game))

    def update(self, dt):
        for button in self.buttons:
            button.process()  # Vérifie hover / clic

    def draw(self, surface):
        super().draw(surface)
        title = self.title_font.render("Space Zinzins", True, (255, 255, 255))

        surface_width, surface_height = surface.get_size()
        title_rect = title.get_rect(center=(surface_width // 2, surface_height // 4))

        surface.blit(title, title_rect)

        for button in self.buttons:
            surface.blit(button.button_surface, (button.x, button.y))


class GameScreen(Screen):
    def __init__(self, game):

        super().__init__(game)

        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.effects = EffectsManager()

        # Joueur
        self.player = Player(
            x=self.width // 2,
            y=self.height - 50,
            speed=5,
            image_path=PLAYER_IMG,
        )
        self.all_sprites.add(self.player)

        self.generate_ennemies()

        self.font_score = pg.font.Font("src/assets/font/space_zinzins.ttf", 36)
        self.font_lives = pg.font.Font("src/assets/font/space_zinzins.ttf", 36)

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot_basic(self.bullets, Bullet, BULLET_IMG)
                if event.key == pg.K_LALT:
                    self.player.shoot_spread(self.bullets, Bullet, BULLET_IMG)

    def generate_ennemies(self):
        # Ennemis
        for row in range(4):
            enemy_img = random.choice(ENEMY_IMG)
            for col in range(8):
                enemy = Enemy(
                    x=80 + col * 80, y=50 + row * 60, image_path=enemy_img, speed=3
                )
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        self.enemy_direction = 1

    def generate_boss(self):
        boss = Enemy(
            x=self.width // 2 - 100,
            y=50,
            image_path="src/assets/boss.png",
            speed=2,
            boss=True,
        )
        self.enemies.add(boss)
        self.all_sprites.add(boss)

    def update(self, dt):
        self.player.update(self.width)
        self.bullets.update()
        self.effects.update()

        # Mise à jour ennemis

        edge_reached = False
        for enemy in self.enemies:
            if enemy.update(self.width):
                edge_reached = True

                # Chaque ennemi essaie de tirer selon son timer interne
            enemy.try_to_shoot(
                self.enemy_bullets, Bullet, "src/assets/enemy_bullet.png"
            )

        if edge_reached:
            for enemy in self.enemies:
                enemy.descend(70)
                enemy.speed *= -1

        # Mise à jour des balles ennemies
        self.enemy_bullets.update()

        # Collisions
        hits = pg.sprite.groupcollide(self.enemies, self.bullets, True, True)
        if hits:
            self.effects.play_explosion()  # play explosion sound
            for enemy in hits:
                self.effects.explosion(enemy.rect.centerx, enemy.rect.centery)
            self.player.score += len(hits) * 10

        # Collision joueur / ennemis
        if pg.sprite.spritecollideany(self.player, self.enemies):
            self.player.lives -= 1
            if self.player.lives <= 0:
                self.game.quit()

        # Collision joueur / balles ennemies
        enemy_hits = pg.sprite.spritecollide(
            self.player, self.enemy_bullets, dokill=True
        )
        if enemy_hits:
            self.effects.play_hit()  # jouer le son de hit
            self.player.lives -= 1
            if self.player.lives <= 0:
                self.game.quit()

        if len(self.enemies) == 0:
            if self.player.lives < 5:
                self.player.lives += 1  # donner une vie bonus
            self.effects.play_wave_clear()  # jouer le son de vague terminée
            self.generate_ennemies()

    def draw(self, surface):
        super().draw(surface)
        self.all_sprites.draw(surface)
        self.bullets.draw(surface)
        self.enemy_bullets.draw(surface)
        self.effects.draw(surface)

        # Score et vies
        score_text = self.font_score.render(
            str(self.player.score), True, (255, 255, 255)
        )
        lives_text = self.font_lives.render(
            str(self.player.lives), True, (255, 255, 255)
        )
        surface.blit(score_text, (10, 10))
        surface.blit(lives_text, (self.width - 120, 10))
