import pygame
import sys
import random
import os
import shutil
from boss import spawn_boss, boss_shoot, update_boss_bullets
from player import Player
from upgrade import reward_menu
from enemy import (
    spawn_police_car,
    update_police_cars,
    draw_police_cars,
    police_cars_shoot,
    check_police_car_collision,
)

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forklift Road Drive")

# Colors
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 204, 0)
BLACK = (0, 0, 0)
CYEAN = (0, 255, 255)
RED = (255, 0, 0)

# Load images
road_image = pygame.image.load("pictures/ROAD.png")
road_image = pygame.transform.scale(road_image, (WIDTH, HEIGHT))

bullet_image = pygame.image.load("pictures/RPGAMMO.png")
bullet_image = pygame.transform.scale(bullet_image, (60, 60))

police_car_image = pygame.image.load("pictures/police_car.png")
police_car_width, police_car_height = 120, 120
police_car_image = pygame.transform.scale(police_car_image, (police_car_width, police_car_height))

police_bullet_image = pygame.image.load("pictures/bullet.png")
police_bullet_image = pygame.transform.scale(police_bullet_image, (30, 30))

heart_image = pygame.image.load("pictures/heart.png")
heart_image = pygame.transform.scale(heart_image, (50, 50))

# Initialize player
player = Player(WIDTH // 2, HEIGHT - 150, 90, 150, 5, 100)

# Initialize game variables
clock = pygame.time.Clock()
running = True
road_scroll_y = 0

# Police car variables
police_cars = []
police_spawn_timer = 0
police_spawn_delay = 90
police_bullets = []

# Heart variables
hearts = []
hearts_timer = 0

# Bullet variables
bullets = []
rocket_cooldown = 0
rocket_cooldown_duration = 20

# Boss variables
bosses = []
boss_bullets = []
boss_spawned = False

# Round variables
current_round = 1
round_active = True
police_cars_to_spawn = 15
police_cars_destroyed = 0
police_cars_required = 15
round_time_limit = 180
round_timer = round_time_limit * 60

# Score and highscore
score = 0
highscore_file = "mobilgame/highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
else:
    highscore = 0

font = pygame.font.SysFont(None, 48)

# Main menu
def main_menu():
    menu_running = True

    forklift_menu_image = pygame.image.load("pictures/forklift.png")
    forklift_menu_image = pygame.transform.scale(forklift_menu_image, (player.width, player.height))

    button_width = 200
    button_height = 60
    play_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 100, button_width, button_height)
    quit_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)

    while menu_running:
        screen.fill(GRAY)

        screen.blit(forklift_menu_image, (WIDTH // 2 - player.width // 2, HEIGHT // 2 - 250))

        pygame.draw.rect(screen, WHITE, play_button_rect)
        pygame.draw.rect(screen, WHITE, quit_button_rect)

        font = pygame.font.SysFont(None, 48)
        play_text = font.render("Play", True, BLACK)
        quit_text = font.render("Quit", True, BLACK)
        screen.blit(play_text, (play_button_rect.x + button_width // 2 - play_text.get_width() // 2,
                                play_button_rect.y + button_height // 2 - play_text.get_height() // 2))
        screen.blit(quit_text, (quit_button_rect.x + button_width // 2 - quit_text.get_width() // 2,
                                quit_button_rect.y + button_height // 2 - quit_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_x, mouse_y):
                    menu_running = False
                elif quit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

main_menu()

# Game loop
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.move(mouse_x, mouse_y, WIDTH, HEIGHT)

    # Scroll the road
    road_scroll_y += 5
    if road_scroll_y >= HEIGHT:
        road_scroll_y = 0
    screen.blit(road_image, (0, road_scroll_y - HEIGHT))
    screen.blit(road_image, (0, road_scroll_y))

   
    if current_round == 4:
        # Spawn the boss immediately
        if not boss_spawned:
            spawn_boss(bosses, WIDTH, 200, 200, 500, 20)  # Spawn the boss with example stats
            boss_spawned = True

        # Handle boss logic
        for boss in bosses[:]:
            boss_x, boss_y, boss_health, boss_damage = boss

            # Move the boss (optional: add movement logic here)
            boss_y += 1  # Example downward movement
            boss[1] = boss_y

            # Draw the boss
            pygame.draw.rect(screen, RED, (boss_x, boss_y, 200, 200))  # Replace with boss image if available

            # Check if the boss is defeated
            if boss_health <= 0:
                bosses.remove(boss)
                current_round += 1
                boss_spawned = False
                round_active = True

            # Boss shooting logic
            boss_shoot(boss, boss_bullets, bullet_speed=5)

        # Update and draw boss bullets
        update_boss_bullets(boss_bullets, screen, police_bullet_image)
        continue

    # Spawn police cars
    if len(police_cars) < police_cars_to_spawn and round_active:
        spawn_police_car(police_cars, WIDTH, police_car_width, police_car_height)

    # Update and draw police cars
    police_cars = update_police_cars(police_cars, 5, HEIGHT, police_car_height)
    draw_police_cars(screen, police_cars, police_car_image)

    # Police cars shooting
    police_bullets.extend(police_cars_shoot(police_cars, police_car_width, police_car_height, police_bullet_image))

    # Player shooting
    if pygame.mouse.get_pressed()[2] and rocket_cooldown == 0:
        bullets.append([player.x + player.width // 2 - bullet_image.get_width() // 2, player.y])
        rocket_cooldown = rocket_cooldown_duration

    if rocket_cooldown > 0:
        rocket_cooldown -= 1

    for bullet in bullets[:]:
        bullet[1] -= 10
        screen.blit(bullet_image, (bullet[0], bullet[1]))
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Draw player
    player.draw(screen)

    # Draw health bar
    player_health_ratio = player.health / player.max_health
    pygame.draw.rect(screen, GRAY, (20, 20, 200, 20))
    pygame.draw.rect(screen, RED, (20, 20, 200 * player_health_ratio, 20))

    pygame.display.flip()

pygame.quit()