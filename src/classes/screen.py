import random
from time import sleep
from classes.button import BlinkingText, Button
import pygame as pg

from classes.player import Player
from classes.flight_entity import BonusDirector, FlightEntity
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

FONT = "src/assets/font/space_zinzins.ttf"


class Screen:
    def __init__(self, game):
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
        self.bonus = pg.sprite.Group()

        # Joueur
        self.player = Player(
            x=self.width // 2,
            y=self.height - 50,
            speed=5,
            image_path=PLAYER_IMG,
        )
        self.all_sprites.add(self.player)

        self.waiting_next_wave = False
        self.next_wave_start_time = 0
        self.wait_duration = 2000  # en ms (2 secondes)
        self.wave_text = BlinkingText(
            "NEXT WAVE",
            "src/assets/font/space_zinzins.ttf",
            72,
            (self.width // 2, self.height // 2),
            blink_interval=400,
        )

        self.generate_ennemies()

        self.font_score = pg.font.Font(FONT, 36)
        self.font_lives = pg.font.Font(FONT, 36)

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot_basic(self.bullets, FlightEntity, BULLET_IMG)
                if event.key == pg.K_LALT:
                    self.player.consum_bonus(self.bullets)

    def generate_ennemies(self):
        # Ennemis
        for row in range(4):
            enemy_img = random.choice(ENEMY_IMG)
            for col in range(8):
                enemy = Enemy(x=80 + col * 80, y=50 + row * 60, image_path=enemy_img)
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

    def clear_sprites(self):
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.enemies.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)

    def update(self, dt):
        # Si on attend la prochaine vague, on ne met pas à jour le gameplay
        if self.waiting_next_wave:
            self.clear_sprites()
            self.wave_text.update()
            # Vérifie si le délai est écoulé
            if pg.time.get_ticks() - self.next_wave_start_time > self.wait_duration:
                self.waiting_next_wave = False
                self.generate_ennemies()
            return

        self.player.update(self.width)
        self.bullets.update()
        self.bonus.update()

        # Bonus generation
        self.maybe_spawn_bonus()
        self.effects.update()

        # Mise à jour ennemis
        edge_reached = False
        for enemy in self.enemies:
            if enemy.update(self.width):
                edge_reached = True

                # Chaque ennemi essaie de tirer selon son timer interne
            enemy.try_to_shoot(self.enemy_bullets)

        if edge_reached:
            for enemy in self.enemies:
                enemy.edge_reached()

        # Mise à jour des balles ennemies
        self.enemy_bullets.update()

        # Collisions
        hits = pg.sprite.groupcollide(self.enemies, self.bullets, True, True)
        if hits:
            self.effects.play_explosion()  # play explosion sound
            for enemy in hits:
                self.effects.explosion(enemy.rect.centerx, enemy.rect.centery)
            self.player.add_score(len(hits) * 10)

        if (
            pg.sprite.spritecollideany(self.player, self.enemies)
            and not self.player.almighty
        ):
            self.player.player_hit(1)
            if self.player.lives <= 0:
                self.game.quit()

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
            self.waiting_next_wave = True
            self.effects.play_wave_clear()  # play wave clear sound
            self.next_wave_start_time = pg.time.get_ticks()

        # Collision player / bonus
        bonus_hits = pg.sprite.spritecollide(self.player, self.bonus, dokill=True)
        if bonus_hits:
            self.player.collect_bonus(bonus_hits[0])
            bonus_hits[0].getting_collected()

    def draw(self, surface):
        super().draw(surface)
        self.all_sprites.draw(surface)
        self.bullets.draw(surface)
        self.enemy_bullets.draw(surface)
        self.bonus.draw(surface)
        self.player.update_bonus(surface)
        self.effects.draw(surface)

        # Score and lives
        score_text = self.font_score.render(
            str(self.player.score), True, (255, 255, 255)
        )
        lives_text = self.font_lives.render(
            str(self.player.lives), True, (255, 255, 255)
        )
        surface.blit(score_text, (10, 10))
        surface.blit(lives_text, (self.width - 120, 10))

        # --- Affiche le texte clignotant entre deux vagues ---
        if self.waiting_next_wave:
            self.wave_text.draw(surface)

    def maybe_spawn_bonus(self):
        """Génère aléatoirement un bonus selon certaines conditions."""

        # Limite du nombre de bonus actifs
        MAX_BONUS_ON_SCREEN = 2

        # Probabilité de génération à chaque frame (1/600 ≈ ~1 bonus toutes les 10s à 60FPS)
        BONUS_SPAWN_CHANCE = 1 / 600

        # Si déjà trop de bonus présents → on ne génère pas
        if len(self.bonus) >= MAX_BONUS_ON_SCREEN:
            return

        # Test de probabilité
        if random.random() > BONUS_SPAWN_CHANCE:
            return

        # Sélection aléatoire du type de bonus
        bonus_type = random.choices(
            [BonusDirector.create_shield_bonus, BonusDirector.create_spread_shot_bonus],
            weights=[0.4, 0.6],  # 40% shield, 60% spread shot
        )[0]

        # Création temporaire pour vérifier ses propriétés
        temp_bonus = bonus_type(0, 0)  # on crée juste pour lire ses attributs

        # Conditions de génération
        if not temp_bonus.one_off_use and not temp_bonus._Bonus__is_reusable:
            # Si c’est un bonus non réutilisable déjà utilisé → on ne le génère pas
            return

        # Coordonnées aléatoires pour l’apparition
        x = random.randint(100, self.width - 100)
        y = 0  # juste au-dessus de l’écran

        # Création réelle du bonus
        bonus = bonus_type(x, y)
        self.bonus.add(bonus)
