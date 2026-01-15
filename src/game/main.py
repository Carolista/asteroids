import sys

import pygame

from ..config.constants import (
    BLACK,
    FONT_GAME_OVER,
    GAME_OVER_COLOR,
    PROMPT_COLOR,
    SCORE_COLOR,
    SCREEN_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from .asteroid import Asteroid
from .asteroidfield import AsteroidField
from .logger import log_event, log_state
from .particle import Particle
from .player import Player
from .shot import Shot
from .star import Star
from .starfield import StarField
from .textcontent import startup_text


def reset_groups_and_objects(updatable, drawable, stars, asteroids, shots, particles):
    updatable.empty()
    drawable.empty()
    stars.empty()
    asteroids.empty()
    shots.empty()
    particles.empty()

    # Once created these two will be managed through their containers
    star_field = StarField()  # noqa: F841
    asteroid_field = AsteroidField()  # noqa: F841

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    return player


def run_collision_check(asteroids, shots, player, score):
    shooter_collision_detected = False
    for asteroid in asteroids:
        for shot in shots:
            if shot.collides_with(asteroid):
                log_event("asteroid_shot")
                for _ in range(10):
                    p = Particle(shot.position.x, shot.position.y)  # noqa: F841
                shot.kill()
                asteroid.split()
                score += 100 - asteroid.radius
        if player.collides_with(asteroid):
            log_event("player_hit")
            shooter_collision_detected = True
            break
    return shooter_collision_detected, score


def draw_screen_and_objects(screen, drawable):
    screen.fill(SCREEN_COLOR)  # Clear screen
    for obj in drawable:
        obj.draw(screen)


def draw_score_panel(screen, score):
    score_font = pygame.font.SysFont("monospace", 40)
    score_text = score_font.render(f"{score}", True, SCORE_COLOR)
    screen.blit(score_text, (10, 10))


def play_round(screen, clock, updatable, drawable, stars, asteroids, shots, particles):
    # Reset for new round
    player = reset_groups_and_objects(updatable, drawable, stars, asteroids, shots, particles)
    score = 0
    dt = 0

    # Manage re-rendering and interactive events
    while True:
        log_state()

        # Allow game window's close button to end program at any time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Player closed window.\n")
                sys.exit(0)

        # Update positions
        updatable.update(dt)

        # Handle collisions (asteroid/player, asteroid/shot)
        should_end_game, score = run_collision_check(asteroids, shots, player, score)

        if should_end_game:
            return  # Continue to game-over prompt

        # Update screen, drawables, and score displays
        draw_screen_and_objects(screen, drawable)
        draw_score_panel(screen, score)

        # Re-render
        pygame.display.flip()

        # Manage fps
        dt = clock.tick(60) / 1000


def draw_game_over_overlay(screen):
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # GAME OVER text
    game_over_font = pygame.font.Font(FONT_GAME_OVER, 60)
    game_over_text = game_over_font.render("GAME OVER", True, GAME_OVER_COLOR)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # TODO: Add final score text

    # Prompt text
    prompt_font = pygame.font.SysFont("monospace", 30)
    prompt_text = prompt_font.render("Play again? Y / N", True, PROMPT_COLOR)
    prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(prompt_text, prompt_rect)


def replay_or_quit(screen, clock, drawable):
    while True:
        # Listen for player interactivity
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

        # Draw game field at last positions
        draw_screen_and_objects(screen, drawable)

        # Draw overlay for game-over prompt
        draw_game_over_overlay(screen)

        # Re-render everything
        pygame.display.flip()

        # Optimize CPU for static screen
        clock.tick(30)


def main():
    pygame.init()

    print(startup_text)  # console output

    # TODO: Create splash screen

    try:
        # Misc Variables
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        # Groups
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        stars = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        particles = pygame.sprite.Group()

        # Containers
        StarField.containers = updatable
        Star.containers = (stars, updatable, drawable)
        AsteroidField.containers = updatable
        Asteroid.containers = (asteroids, updatable, drawable)
        Player.containers = (updatable, drawable)
        Shot.containers = (shots, updatable, drawable)
        Particle.containers = (particles, updatable, drawable)

        # GAMEPLAY LOOP
        while True:
            # Run game until player and an asteroid collide
            play_round(screen, clock, updatable, drawable, stars, asteroids, shots, particles)

            # Initiate game-over prompt and get response
            play_again = replay_or_quit(screen, clock, drawable)
            if not play_again:
                return  # End program

    finally:
        print("Exiting program... thank you for playing!\n")
        pygame.quit()


if __name__ == "__main__":
    main()
