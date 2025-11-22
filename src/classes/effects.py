import pygame
import random


class EffectsManager:
    def __init__(self):
        """Create an effect"""
        # === PREPARE AUDIO CHANNELS ===
        pygame.mixer.set_num_channels(8)  # plenty of space
        self.music_channel = pygame.mixer.Channel(0)  # dedicated to music
        self.sfx_channel = pygame.mixer.Channel(1)  # dedicated to SFX

        # === LOAD SOUND EFFECTS ===
        self.snd_shoot = pygame.mixer.Sound("src/assets/sounds/shoot.wav")
        self.snd_explosion = pygame.mixer.Sound("src/assets/sounds/explosion.wav")
        self.snd_hit = pygame.mixer.Sound("src/assets/sounds/hit.wav")
        self.snd_gameover = pygame.mixer.Sound("src/assets/sounds/gameover.wav")
        self.snd_wave_clear = pygame.mixer.Sound("src/assets/sounds/wave_clear.wav")
        self.snd_boss_spawn = pygame.mixer.Sound("src/assets/sounds/boss_spawn.wav")
        self.snd_boss_dead = pygame.mixer.Sound("src/assets/sounds/boss_dead.wav")

        # === LOAD BACKGROUND MUSIC AS SOUND (NOT mixer.music) ===
        self.music = pygame.mixer.Sound("src/assets/sounds/sound_theme.wav")
        self.music.set_volume(0.3)

        # Start the music immediately
        self.music_channel.play(self.music, loops=-1)

        # Particles
        self.particles = pygame.sprite.Group()

    # === VISUAL EFFECTS ===
    def explosion(self, x, y, color=(164, 185, 7)):
        """Create a small explosion of particles"""
        for _ in range(10):
            particle = Particle(x, y, color)
            self.particles.add(particle)
        self.sfx_channel.play(self.snd_explosion)

    # === SOUND EFFECTS ===
    def play_shoot(self):
        self.sfx_channel.play(self.snd_shoot)

    def play_explosion(self):
        self.sfx_channel.play(self.snd_explosion)

    def play_hit(self):
        self.sfx_channel.play(self.snd_hit)

    def play_gameover(self):
        self.sfx_channel.play(self.snd_gameover)

    def play_wave_clear(self):
        self.sfx_channel.play(self.snd_wave_clear)

    def play_boss_spawn(self):
        self.sfx_channel.play(self.snd_boss_spawn)

    def play_boss_dead(self):
        self.sfx_channel.play(self.snd_boss_dead)

    # === BACKGROUND MUSIC ===
    def play_music(self, loop=True):
        loops = -1 if loop else 0
        self.music_channel.play(self.music, loops=loops)

    def stop_music(self):
        self.music_channel.stop()

    # === UPDATE ===
    def update(self):
        """Update the particles"""
        self.particles.update()

    def draw(self, screen):
        """Render the particles"""
        self.particles.draw(screen)


class Particle(pygame.sprite.Sprite):
    """Simple animated particles (explosion, shot, etc.)"""

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
