import random

import pygame

from ..config.constants import (
    FONT_SCORE,
    FONT_TITLE,
    HIGH_SCORES_FILE,
    SCORE_COLOR,
    SCREEN_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WAVE_COLOR,
)
from ..config.funcs import handle_exit
from .effects.fade import Fade
from .entities.asteroid import Asteroid
from .entities.asteroidfield import AsteroidField
from .entities.particle import Particle
from .entities.player import Player
from .entities.shot import Shot
from .entities.star import Star
from .entities.starfield import StarField
from .screens.gameover import GameOverScreen
from .screens.splash import SplashScreen
from .systems.highscores import HighScoreManager
from .systems.logger import log_event, log_state
from .systems.startup import run_startup_script

# TODO: Make scoring more sophisticated with streak bonuses (with visual feedback)
# TODO: Add temporary visual display below score when a high score is passed (NEW HIGH SCORE!)
# TODO: Add bombs, mines, and shockwaves
# TODO: Add invincibility powerup and shield powerup
# TODO: Add lives along with a 1-up powerup


def reset_groups_and_objects(updatable, drawable, stars, asteroids, shots, particles):
    updatable.empty()
    drawable.empty()
    stars.empty()
    asteroids.empty()
    shots.empty()
    particles.empty()

    # Managed through its container
    star_field = StarField()  # noqa: F841

    asteroid_field = AsteroidField()

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    return player, asteroid_field


def run_collision_check(asteroids, shots, player, score, shake_intensity):
    shooter_collision_detected = False
    for asteroid in asteroids:
        for shot in shots:
            if shot.collides_with(asteroid):
                log_event("asteroid_shot")
                shake_intensity = asteroid.radius / 5
                for _ in range(10):
                    p = Particle(shot.position.x, shot.position.y)  # noqa: F841
                shot.kill()
                asteroid.split()
                score += 100 - int(asteroid.radius)
        if player.collides_with(asteroid):
            log_event("player_hit")
            shake_intensity = 20
            shooter_collision_detected = True
            break
    return shooter_collision_detected, score, shake_intensity


def draw_game_surface_and_objects(screen, game_surface, drawable, shake_intensity):
    game_surface.fill(SCREEN_COLOR)  # Clear screen
    for obj in drawable:
        obj.draw(game_surface)

    offset = pygame.Vector2(0, 0)

    if shake_intensity > 0:
        offset.x = random.uniform(-shake_intensity, shake_intensity)
        offset.y = random.uniform(-shake_intensity, shake_intensity)
        shake_intensity -= 0.5  # Decay shake over time

    screen.fill("black")
    screen.blit(game_surface, offset)
    return shake_intensity


def draw_score_panel(screen, score):
    score_font = pygame.font.Font(FONT_SCORE, 40)
    score_text = score_font.render(f"{score}", True, SCORE_COLOR)
    screen.blit(score_text, (10, 10))


def draw_wave_text(screen, wave_number):
    wave_font = pygame.font.Font(FONT_TITLE, 80)
    wave_text = wave_font.render(f"WAVE {wave_number}", True, WAVE_COLOR)
    wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150))
    screen.blit(wave_text, wave_rect)


def play_round(
    screen,
    game_surface,
    clock,
    player,
    updatable,
    drawable,
    asteroids,
    shots,
    asteroid_field,
    fade,
    first_wave=False,  # noqa: E501
):
    # Reset for new round
    score = 0
    dt = 0
    shake_intensity = 0.0
    wave_number = 0
    is_transitioning = False
    wave_text_shown = first_wave  # Skip wave text for first wave

    # Manage re-rendering and interactive events
    while True:
        log_state()

        # Check for end of wave
        if len(asteroids) == 0 and not is_transitioning:
            is_transitioning = True
            wave_number += 1
            wave_text_shown = False

        if is_transitioning and not wave_text_shown:
            # Show wave text with fade in/out
            wave_font = pygame.font.Font(FONT_TITLE, 80)
            wave_text = wave_font.render(f"WAVE {wave_number}", True, WAVE_COLOR)
            position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150)

            # Take snapshot of current game state
            shake_intensity = draw_game_surface_and_objects(
                screen, game_surface, drawable, shake_intensity
            )
            draw_score_panel(screen, score)
            pygame.display.flip()

            # Fade wave text in and out
            fade.fade_text_in_out(screen, wave_text, position, hold_duration=0.5)

            # Now spawn asteroids
            num_to_spawn = min(2 + wave_number, 10)
            asteroid_field.spawn_wave(num_to_spawn)
            is_transitioning = False
            wave_text_shown = True

        # Allow game window's close button to end program at any time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_exit()

        # Update positions
        updatable.update(dt)

        # Handle collisions (asteroid/player, asteroid/shot)
        should_end_game, score, shake_intensity = run_collision_check(
            asteroids, shots, player, score, shake_intensity
        )  # noqa: E501

        if should_end_game:
            # Fade out before game over
            fade.fade_out(screen, game_surface, drawable, clock)
            return score  # Continue to game-over prompt

        # Update screen, drawables, and score displays
        shake_intensity = draw_game_surface_and_objects(
            screen, game_surface, drawable, shake_intensity
        )  # noqa: E501
        draw_score_panel(screen, score)

        # If between waves
        if is_transitioning:
            draw_wave_text(screen, wave_number)

        # Re-render
        pygame.display.flip()

        # Manage fps
        dt = clock.tick(60) / 1000


def main():
    pygame.init()

    try:
        # Misc Variables
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
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

        run_startup_script()  # console output

        # Initialize high score manager
        high_score_manager = HighScoreManager(HIGH_SCORES_FILE)

        # Initialize fade effect
        fade = Fade(duration=0.5)

        # Show splash screen
        splash = SplashScreen(high_score_manager)
        should_play = splash.run(screen, game_surface, clock)
        if not should_play:
            return  # User quit from splash screen

        # Reset containers after splash screen (splash modifies class-level containers)
        Star.containers = (stars, updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)

        # GAMEPLAY LOOP
        first_game = True
        while True:
            player, asteroid_field = reset_groups_and_objects(
                updatable, drawable, stars, asteroids, shots, particles
            )  # noqa: E501

            # Fade in from black to gameplay (only on first game)
            if first_game:
                fade.fade_in(screen, game_surface, drawable, clock)
                first_game = False

            # Run game until player and an asteroid collide
            final_score = play_round(
                screen,
                game_surface,
                clock,
                player,
                updatable,
                drawable,
                asteroids,
                shots,
                asteroid_field,
                fade,
                first_wave=True,  # noqa: E501, F821
            )

            # Initiate game-over screen and get response
            game_over_screen = GameOverScreen(final_score, high_score_manager, fade)
            play_again = game_over_screen.run(screen, game_surface, clock)

            # Reset containers after game-over screen
            # (game-over screen modifies class-level containers)
            Star.containers = (stars, updatable, drawable)
            Asteroid.containers = (asteroids, updatable, drawable)

            if not play_again:
                return  # End program

    finally:
        print("Exiting program... thank you for playing!\n")
        pygame.quit()


if __name__ == "__main__":
    main()
