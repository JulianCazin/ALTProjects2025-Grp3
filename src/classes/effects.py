import pygame
import random


class EffectsManager:
    def __init__(self):
        """Create an effect"""

        # mixer non initialyzed (ex: in tests)
        if not pygame.mixer.get_init():
            self.snd_shoot = pygame.mixer.Sound("src/assets/sounds/shoot.wav")
            self.snd_explosion = self.snd_hit = None
            self.snd_gameover = self.snd_wave_clear = None
            self.snd_boss_spawn = self.snd_boss_dead = None

            return

        # load sounds
        self.snd_shoot = pygame.mixer.Sound("src/assets/sounds/shoot.wav")
        self.snd_explosion = pygame.mixer.Sound("src/assets/sounds/explosion.wav")
        self.snd_hit = pygame.mixer.Sound("src/assets/sounds/hit.wav")
        self.snd_gameover = pygame.mixer.Sound("src/assets/sounds/gameover.wav")
        self.snd_wave_clear = pygame.mixer.Sound("src/assets/sounds/wave_clear.wav")
        self.snd_boss_spawn = pygame.mixer.Sound("src/assets/sounds/boss_spawn.wav")
        self.snd_boss_dead = pygame.mixer.Sound("src/assets/sounds/boss_dead.wav")

        self.particles = pygame.sprite.Group()

        self.snd_explosion.set_volume(0.5)

        # === LOAD BACKGROUND MUSIC ===
        pygame.mixer.music.load("src/assets/sounds/sound_theme.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # play in loop

    # === VISUAL EFFETS  ===
    def explosion(self, x, y, color=(164, 185, 7)):
        """Create a small explosion of particles"""
        for _ in range(10):
            particle = Particle(x, y, color)
            self.particles.add(particle)
        self.snd_explosion.play()

    # === SOUND EFFECTS ===
    def play_shoot(self):
        """Play the sound of a shoot"""
        self.snd_shoot.play()

    def play_explosion(self):
        """Play the sound of an explosion"""
        self.snd_explosion.play()

    def play_hit(self):
        """Play the sound of a hit"""
        self.snd_hit.play()

    def play_gameover(self):
        """Play the sound of a gameover"""
        self.snd_gameover.play()

    def play_wave_clear(self):
        """Play the sound of a cleared wave"""
        self.snd_wave_clear.play()

    def play_boss_spawn(self):
        """Play the sound of a boss spawning"""
        self.snd_boss_spawn.play()

    def play_boss_dead(self):
        """Play the sound of a dead boss"""
        self.snd_boss_dead.play()

    # === BACKGROUND MUSIC ===
    def play_music(self, loop=True):
        """Play background music (loop = True means infinite loop)."""
        loops = -1 if loop else 0
        pygame.mixer.music.play(loops)

    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()

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
        """Create a particle with its x and y coordonates and its color"""
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        # Create the randomness of the particle
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = random.randint(20, 40)

    def update(self):
        """Actions when the particle is updated"""
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= 1
        self.image.set_alpha(max(0, self.life * 6))
        if self.life <= 0:
            self.kill()
