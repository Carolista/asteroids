import random
import sys

import pygame

from ..config.constants import (
    BLACK,
    FINAL_SCORE_COLOR,
    FONT_SCORE,
    FONT_SPECIAL,
    GAME_OVER_COLOR,
    PROMPT_COLOR,
    SCORE_COLOR,
    SCREEN_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WAVE_COLOR,
)
from .asteroid import Asteroid
from .asteroidfield import AsteroidField
from .logger import log_event, log_state
from .particle import Particle
from .player import Player
from .shot import Shot
from .star import Star
from .starfield import StarField
from .startup import run_startup_script

# TODO: Implement fade in and fade out on wave transition text
# TODO: Create splash screen, larger twinkling stars and larger asteroids with large text and 'Hit Enter to Play'  # noqa: E501
# TODO: Make scoring more sophisticated with streak bonuses (with visual feedback)
# TODO: Add txt or json file to persist high scores and show high score on game over screen
# TODO: Add temporary visual display below score when a high score is passed (NEW HIGH SCORE!)
# TODO: Add bombs and mines
# TODO: Add invincibility powerup and shield powerup
# TODO: Add lives with a 1up powerup


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
    wave_font = pygame.font.Font(FONT_SPECIAL, 80)
    wave_text = wave_font.render(f"WAVE {wave_number}", True, WAVE_COLOR)
    wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
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
    asteroid_field,  # noqa: E501
):
    # Reset for new round
    score = 0
    dt = 0
    shake_intensity = 0.0
    wave_number = 0
    is_transitioning = False
    transition_timer = 0

    # Manage re-rendering and interactive events
    while True:
        log_state()

        # Check for end of wave
        if len(asteroids) == 0 and not is_transitioning:
            is_transitioning = True
            transition_timer = 2.0
            wave_number += 1

        if is_transitioning:
            transition_timer -= dt
            if transition_timer <= 0:
                num_to_spawn = min(2 + wave_number, 10)
                asteroid_field.spawn_wave(num_to_spawn)
                is_transitioning = False

        # Allow game window's close button to end program at any time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Player closed window.\n")
                sys.exit(0)

        # Update positions
        updatable.update(dt)

        # Handle collisions (asteroid/player, asteroid/shot)
        should_end_game, score, shake_intensity = run_collision_check(
            asteroids, shots, player, score, shake_intensity
        )  # noqa: E501

        if should_end_game:
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


def draw_game_over_overlay(screen, final_score):
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Game over text
    game_over_font = pygame.font.Font(FONT_SPECIAL, 60)
    game_over_text = game_over_font.render("G A M E   O V E R", True, GAME_OVER_COLOR)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70))
    screen.blit(game_over_text, game_over_rect)

    # Final score text
    final_score_font = pygame.font.Font(FONT_SCORE, 40)
    final_score_text = final_score_font.render(
        f"FINAL SCORE: {final_score}", True, FINAL_SCORE_COLOR
    )  # noqa: E501
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(final_score_text, final_score_rect)

    # Prompt text
    prompt_font = pygame.font.SysFont("monospace", 32)
    prompt_text = prompt_font.render("Play Again?  Y / N", True, PROMPT_COLOR)
    prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
    screen.blit(prompt_text, prompt_rect)


def replay_or_quit(screen, clock, drawable, final_score):
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

        # Draw game objects at last positions and put directly on screen
        screen.fill(SCREEN_COLOR)
        for obj in drawable:
            obj.draw(screen)

        # Draw overlay for game-over prompt
        draw_game_over_overlay(screen, final_score)

        # Re-render everything
        pygame.display.flip()

        # Optimize CPU for static screen
        clock.tick(30)


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

        # GAMEPLAY LOOP
        while True:
            player, asteroid_field = reset_groups_and_objects(
                updatable, drawable, stars, asteroids, shots, particles
            )  # noqa: E501

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
                asteroid_field,  # noqa: E501, F821
            )

            # Initiate game-over prompt and get response
            play_again = replay_or_quit(screen, clock, drawable, final_score)
            if not play_again:
                return  # End program

    finally:
        print("Exiting program... thank you for playing!\n")
        pygame.quit()


if __name__ == "__main__":
    main()
