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

forklift_image = pygame.image.load("pictures/forklift.png")
forklift_width, forklift_height = 90, 150

def draw_health_bar(surface, x, y, width, height, health, max_health):
    health_ratio = health / max_health
    pygame.draw.rect(surface, GRAY, (x, y, width, height))
    pygame.draw.rect(surface, RED, (x, y, width * health_ratio, height))

# Initialize player
player = Player(WIDTH // 2, HEIGHT - 150, forklift_width, forklift_height, 5, 100)

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

# Auto turret variables
auto_turret_enabled = False
auto_turret_cooldown = 0
auto_turret_cooldown_duration = 5  # Fast fire rate
auto_turret_bullets = []

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

def main_menu():
    menu_running = True

    forklift_menu_image = pygame.image.load("pictures/forklift.png")
    forklift_menu_image = pygame.transform.scale(forklift_menu_image, (forklift_width, forklift_height))

    button_width = 200
    button_height = 60
    play_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 100, button_width, button_height)
    quit_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)

    while menu_running:
        screen.fill(GRAY)

        screen.blit(forklift_menu_image, (WIDTH // 2 - forklift_width // 2, HEIGHT // 2 - 250))

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

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.move(mouse_x, mouse_y, WIDTH, HEIGHT)
    forklift_x, forklift_y = player.x, player.y

    # Scroll the road
    road_scroll_y += 5
    if road_scroll_y >= HEIGHT:
        road_scroll_y = 0
    screen.blit(road_image, (0, road_scroll_y - HEIGHT))
    screen.blit(road_image, (0, road_scroll_y))

    # Spawn police cars
    if len(police_cars) < police_cars_to_spawn and round_active:
        police_spawn_timer += 1
        if police_spawn_timer >= police_spawn_delay:
            police_spawn_timer = 0
            police_x = random.randint(0, WIDTH - police_car_width)
            police_cars.append([police_x, -police_car_height, 20])  # 20 HP

    # Move and draw police cars
    for car in police_cars[:]:
        car[1] += 5
        car[1] = min(car[1], HEIGHT // 2 - police_car_height)
        car[0] += random.choice([-1, 1])
        car[0] = max(0, min(WIDTH - police_car_width, car[0]))

        # Police shooting bullets
        if random.randint(0, 100) < 2:
            police_bullet_x = car[0] + police_car_width // 2 - police_bullet_image.get_width() // 2
            police_bullet_y = car[1] + police_car_height
            police_bullets.append([police_bullet_x, police_bullet_y])

        screen.blit(police_car_image, (car[0], car[1]))

        # Check for collision with the forklift
        if (forklift_x < car[0] + police_car_width and
            forklift_x + forklift_width > car[0] and
            forklift_y < car[1] + police_car_height and
            forklift_y + forklift_height > car[1]):
            if not player.invincible:
                player.take_damage(10)
            if player.health <= 0:
                pygame.quit()
                sys.exit()

    # Player shooting
    if pygame.mouse.get_pressed()[2] and rocket_cooldown == 0:
        bullets.append([forklift_x + forklift_width // 2 - bullet_image.get_width() // 2, forklift_y])
        rocket_cooldown = rocket_cooldown_duration

    if rocket_cooldown > 0:
        rocket_cooldown -= 1

    # Update and draw player bullets
    for bullet in bullets[:]:
        bullet[1] -= 10
        screen.blit(bullet_image, (bullet[0], bullet[1]))
        for car in police_cars[:]:
            car_x, car_y, car_hp = car
            if (bullet[0] < car_x + police_car_width and
                bullet[0] + bullet_image.get_width() > car_x and
                bullet[1] < car_y + police_car_height and
                bullet[1] + bullet_image.get_height() > car_y):
                car[2] -= 10  # Rocket does 10 damage
                bullets.remove(bullet)
                if car[2] <= 0:
                    police_cars.remove(car)
                    police_cars_destroyed += 1
                    score += 10
                break

    # --- AUTO TURRET LOGIC ---
    if auto_turret_enabled:
        auto_turret_cooldown -= 1
        if auto_turret_cooldown <= 0:
            turret_bullet_x = forklift_x + forklift_width // 2 - police_bullet_image.get_width() // 2
            turret_bullet_y = forklift_y
            auto_turret_bullets.append([turret_bullet_x, turret_bullet_y])
            auto_turret_cooldown = auto_turret_cooldown_duration

    for bullet in auto_turret_bullets[:]:
        bullet[1] -= 15  # Fast upward
        screen.blit(police_bullet_image, (bullet[0], bullet[1]))
        for car in police_cars[:]:
            car_x, car_y, car_hp = car
            if (bullet[0] < car_x + police_car_width and
                bullet[0] + police_bullet_image.get_width() > car_x and
                bullet[1] < car_y + police_car_height and
                bullet[1] + police_bullet_image.get_height() > car_y):
                car[2] -= 5  # Auto turret does 5 damage
                auto_turret_bullets.remove(bullet)
                if car[2] <= 0:
                    police_cars.remove(car)
                    police_cars_destroyed += 1
                    score += 10
                break
        else:
            if bullet[1] < 0:
                auto_turret_bullets.remove(bullet)

    # Update and draw police bullets
    for bullet in police_bullets[:]:
        bullet[1] += 10
        screen.blit(police_bullet_image, (bullet[0], bullet[1]))
        if (forklift_x < bullet[0] + police_bullet_image.get_width() and
            forklift_x + forklift_width > bullet[0] and
            forklift_y < bullet[1] + police_bullet_image.get_height() and
            forklift_y + forklift_height > bullet[1]):
            player.take_damage(5)
            police_bullets.remove(bullet)

    # Remove off-screen bullets
    bullets = [bullet for bullet in bullets if bullet[1] > 0]
    police_bullets = [bullet for bullet in police_bullets if bullet[1] < HEIGHT]
    auto_turret_bullets = [bullet for bullet in auto_turret_bullets if bullet[1] > 0]

    # Draw player
    player.draw(screen)

    # Draw health bar
    draw_health_bar(screen, 20, 20, 200, 20, player.health, player.max_health)

    # Draw the score, highscore, round number, and timer
    score_text = font.render(f"Score: {score}", True, WHITE)
    highscore_text = font.render(f"Highscore: {highscore}", True, YELLOW)
    round_text = font.render(f"Round: {current_round}", True, WHITE)
    timer_text = font.render(f"Time Left: {round_timer // 60}s", True, RED)
    screen.blit(score_text, (20, 50))
    screen.blit(highscore_text, (20, 100))
    screen.blit(round_text, (20, 150))
    screen.blit(timer_text, (20, 200))

    # Decrease the round timer
    if round_active:
        round_timer -= 1

    # Check if the round is complete
    if (police_cars_destroyed >= police_cars_required or round_timer <= 0) and round_active:
        round_active = False
        police_cars_destroyed = 0
        round_timer = round_time_limit * 60
        # Show the reward menu
        upgrade = reward_menu()
        if upgrade == "firerate":
            rocket_cooldown_duration = max(5, rocket_cooldown_duration - 5)
        elif upgrade == "maxhp":
            player.set_max_health(player.max_health + 20)
        elif upgrade == "speed":
            player.speed += 2
        elif upgrade == "autoturret":
            auto_turret_enabled = True

        # Start the next round
        current_round += 1
        police_cars_to_spawn += 2
        police_cars_required += 20
        round_active = True

    pygame.display.flip()

pygame.quit()