import sys
import pygame
from .logger import log_state, log_event
from ..config.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_COLOR
from .player import Player
from .asteroid import Asteroid
from .asteroidfield import AsteroidField
from .shot import Shot
from .starfield import StarField
from .star import Star

def main():
    pygame.init()
    
    print(f"\nStarting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen size: {SCREEN_WIDTH} W x {SCREEN_HEIGHT} H\n")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    
    # Score display
    font = pygame.font.SysFont("monospace", 40)
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    stars = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Star.containers = (stars, updatable, drawable)
    StarField.containers = (updatable)

    star_field = StarField()
    player = Player(x = SCREEN_WIDTH/2, y = SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()

    while True:
        log_state()

        # Enable game window's close button to end program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update positions
        updatable.update(dt)

        # Check for collisions
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    score += (100 - asteroid.radius)
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("GAME OVER")
                sys.exit()

        # Render
        screen.fill(SCREEN_COLOR)
        for obj in drawable:
            obj.draw(screen)
        
        # Draw score panel
        score_text = font.render(f"{score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

        # Manage fps
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
