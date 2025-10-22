import pygame
import random


class EffectsManager:
    def __init__(self):
        # Charger les sons
        self.snd_shoot = pygame.mixer.Sound("src/assets/sounds/shoot.wav")
        self.snd_explosion = pygame.mixer.Sound("src/assets/sounds/explosion.wav")
        self.snd_hit = pygame.mixer.Sound("src/assets/sounds/hit.wav")
        # self.snd_gameover = pygame.mixer.Sound("src/assets/sounds/gameover.wav")
        self.snd_wave_clear = pygame.mixer.Sound("src/assets/sounds/wave_clear.wav")
        # self.snd_boss_spawn = pygame.mixer.Sound("src/assets/sounds/boss_spawn.wav")
        # self.snd_boss_dead = pygame.mixer.Sound("src/assets/sounds/boss_dead.wav")

        self.particles = pygame.sprite.Group()

        self.snd_explosion.set_volume(0.2)

    # === EFFETS VISUELS ===
    def explosion(self, x, y, color=(255, 100, 0)):
        """Crée une petite explosion de particules"""
        for _ in range(10):
            particle = Particle(x, y, color)
            self.particles.add(particle)
        self.snd_explosion.play()

    def hit_flash(self, sprite):
        """Fait clignoter un sprite brièvement"""
        flash = pygame.Surface(sprite.rect.size)
        flash.fill((255, 255, 255))
        flash.set_alpha(100)
        sprite.image.blit(flash, (0, 0))

    # === EFFETS SONORES ===
    def play_shoot(self):
        self.snd_shoot.play()

    def play_explosion(self):
        self.snd_explosion.play()

    def play_hit(self):
        self.snd_hit.play()

    def play_gameover(self):
        self.snd_gameover.play()

    def play_wave_clear(self):
        self.snd_wave_clear.play()

    def play_boss_spawn(self):
        self.snd_boss_spawn.play()

    def play_boss_dead(self):
        self.snd_boss_dead.play()

    # === MISE À JOUR ===
    def update(self):
        self.particles.update()

    def draw(self, screen):
        self.particles.draw(screen)


class Particle(pygame.sprite.Sprite):
    """Simple particule animée (explosion, tir, etc.)"""

    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = random.randint(20, 40)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= 1
        self.image.set_alpha(max(0, self.life * 6))
        if self.life <= 0:
            self.kill()
