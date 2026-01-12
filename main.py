import pygame
from logger import log_state
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)

    player = Player(x = SCREEN_WIDTH/2, y = SCREEN_HEIGHT/2)

    while True:
        log_state()

        # Enable game window's close button to end program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update positions
        updatable.update(dt)

        # Render
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()

        # Manage fps
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
