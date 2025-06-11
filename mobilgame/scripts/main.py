import pygame
import sys
import random
import os
import math
from upgrade import reward_menu
from boss import spawn_boss, draw_bosses, boss_shoot, update_boss_bullets

pygame.init()

WIDTH, HEIGHT = 1280, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forklift Road Drive")

GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 204, 0)
BLACK = (0, 0, 0)
CYEAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

forklift_width = 90
forklift_height = 150
forklift_x = WIDTH // 2 - forklift_width // 2
forklift_y = HEIGHT - forklift_height - 20
forklift_speed = 5
forklift_health = 100 
max_health = 100

bullet_image = pygame.image.load("pictures/RPGAMMO.png")
bullet_image = pygame.transform.scale(bullet_image, (60, 60))  

def draw_health_bar(surface, x, y, width, height, health, max_health):
    health_ratio = health / max_health
    pygame.draw.rect(surface, GRAY, (x, y, width, height)) 
    pygame.draw.rect(surface, RED, (x, y, width * health_ratio, height))  

line_width = 10
line_height = 40
line_spacing = 40
line_speed = 5
lines = []
for i in range(0, HEIGHT, line_height + line_spacing):
    lines.append(i)

# Import the forklift image
forklift_image = pygame.image.load("pictures/forklift.png")
forklift_image = pygame.transform.scale(forklift_image, (forklift_width, forklift_height))

# Import the police car image
police_car_image = pygame.image.load("pictures/police_car.png")
police_car_width, police_car_height = 120, 120
police_car_image = pygame.transform.scale(police_car_image, (police_car_width, police_car_height))

red_car_image = pygame.image.load("pictures/red_car.png")
red_car_image = pygame.transform.scale(red_car_image, (120, 120))
blue_car_image = pygame.image.load("pictures/blue_car.png")
blue_car_image = pygame.transform.scale(blue_car_image, (120, 120))
green_car_image = pygame.image.load("pictures/green_car.png")
green_car_image = pygame.transform.scale(green_car_image, (120, 120))

police_cars = []  # List to hold police car positions
police_spawn_timer = 0
police_spawn_delay = 90  

normal_cars = []  # Each car: [x, y, color]
normal_car_types = [
    ("red", red_car_image),
    ("blue", blue_car_image),
    ("green", green_car_image)
]
normal_car_spawn_timer = 0
normal_car_spawn_delay = 60  # Adjust for spawn rate

# Load the road image
road_image = pygame.image.load("pictures/ROAD.png")
road_image = pygame.transform.scale(road_image, (WIDTH, HEIGHT))  # Scale to fullscreen dimensions

try:
    boss_image = pygame.image.load("pictures/TRACTOR.png")
    boss_image = pygame.transform.scale(boss_image, (200, 200))  # Scale the image
except pygame.error as e:
    print(f"Error loading boss image: {e}")
    pygame.quit()
    sys.exit()

bosses = []
boss_bullets = []
boss_shoot_timer = 0 
boss_health = 750
boss_damage = 25

clock = pygame.time.Clock()
running = True


invincible = False
invincibility_timer = 0
invincibility_duration = 60

auto_turret_enabled = False
auto_turret_cooldown = 0
auto_turret_cooldown_duration = 30  # Fast fire rate
auto_turret_bullets = []  #

# List to hold active bullets
bullets = []

# Cooldown timer for rockets
rocket_cooldown = 0
rocket_cooldown_duration = 20  # 2 seconds at 60 FPS

Hearts_image = pygame.image.load("pictures/heart.png")
Hears = pygame.transform.scale(Hearts_image, (50, 50))
hearts_delay = 1
hearts_timer = 0

# List to hold active hearts
hearts = []

# Load highscore from file
highscore_file = "highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
else:
    highscore = 0

score = 0  # Current score
upgrade_given = False  

font = pygame.font.SysFont(None, 48)  # Add this after pygame.init() or after setting up the screen

road_scroll_y = 0

# Load police bullet image
police_bullet_image = pygame.image.load("pictures/bullet.png")
police_bullet_image = pygame.transform.scale(police_bullet_image, (30, 30))

police_bullets = []  # List to hold police bullets

# Add this variable near the other turret variables, before the game loop:
auto_turret_damage = 10  # Initial auto turret damage

# Add this variable near the other boss-related variables
boss_direction = 1  # 1 for right, -1 for left

# Load explosion frames
explosion_frames = []
for i in range(5):  # Assuming the GIF has 5 frames
    frame = pygame.image.load(f"kaput/frame_{i}.png")
    frame = pygame.transform.scale(frame, (120, 120))  # Scale to match the car size
    explosion_frames.append(frame)

explosions = []  # List to hold active explosions

def main_menu():
    menu_running = True

    forklift_menu_image = pygame.image.load("pictures/forklift.png")
    forklift_menu_image = pygame.transform.scale(forklift_menu_image, (forklift_width, forklift_height))

    police_car_menu_image = pygame.image.load("pictures/police_car.png")
    police_car_menu_image = pygame.transform.scale(police_car_menu_image, (police_car_width, police_car_height))


    button_width = 200
    button_height = 60
    play_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 100, button_width, button_height)
    quit_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)

    while menu_running:
        screen.fill(GRAY) 


        screen.blit(forklift_menu_image, (WIDTH // 2 - forklift_width // 2, HEIGHT // 2 - 250))
        screen.blit(police_car_menu_image, (WIDTH // 2 - police_car_width - 150, HEIGHT // 2 - 25))
        screen.blit(police_car_menu_image, (WIDTH // 2 - police_car_width // 2, HEIGHT // 2 - 25))
        screen.blit(police_car_menu_image, (WIDTH // 2 + police_car_width, HEIGHT // 2 - 25))

   
        pygame.draw.rect(screen, WHITE, play_button_rect)
        pygame.draw.rect(screen, WHITE, quit_button_rect)

        # Add text to buttons
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
                    menu_running = False  # Start the game
                elif quit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

main_menu()

current_round = 1
round_active = True
police_cars_to_spawn = 20  # Number of police cars to spawn per round
police_cars_destroyed = 0
police_cars_required = 10
round_time_limit = 180  # 3 minutes (in seconds)
round_timer = round_time_limit * 60  # Convert to frames (assuming 60 FPS)

auto_turret_enabled = False
auto_turret_cooldown = 0
auto_turret_cooldown_duration = 30  # Fast fire rate     
auto_turret_bullets = []

#boss_direction = random.choice([-2, 2])

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    forklift_x = mouse_x - forklift_width // 2
    forklift_x = max(0, min(WIDTH - forklift_width, forklift_x))  

    # Restrict forklift_y to the bottom half of the screen
    forklift_y = max(HEIGHT // 2, min(HEIGHT - forklift_height, mouse_y - forklift_height // 2))

    for i in range(len(lines)):
        lines[i] += line_speed
        if lines[i] > HEIGHT:
            lines[i] = -line_height

    # Scroll the road image
    road_scroll_y += line_speed
    if road_scroll_y >= HEIGHT:
        road_scroll_y = 0


    screen.blit(road_image, (0, road_scroll_y - HEIGHT))  
    screen.blit(road_image, (0, road_scroll_y)) 

    if pygame.mouse.get_pressed()[0]:
        forklift_speed = 10
        line_speed = 10
    else:
        forklift_speed = 5
        line_speed = 5

    # Spawn bullets when right mouse button is clicked, respecting cooldown
    if pygame.mouse.get_pressed()[2] and rocket_cooldown == 0:  # Right mouse button
        bullet_x = forklift_x + forklift_width // 2 - bullet_image.get_width() // 2
        bullet_y = forklift_y
        bullets.append([bullet_x, bullet_y]) 
        rocket_cooldown = rocket_cooldown_duration 

    # Update cooldown timer
    if rocket_cooldown > 0:
        rocket_cooldown -= 1

    # Increase difficulty by reducing spawn delay over time
    # Limit the maximum number of police cars
    if not bosses and len(police_cars) < 7:  # Only spawn police cars if no boss is active
        police_spawn_timer += 1
        if police_spawn_timer >= police_spawn_delay:
            police_spawn_timer = 0
            police_x = random.randint(0, WIDTH - police_car_width)
            # Spawn police cars with a direction
            police_cars.append([police_x, -police_car_height, 100, random.choice([-1, 1])]) 

    for car in police_cars:

        car[1] += line_speed

        car[0] += car[3] * 2  # Adjust speed as needed

        # Reverse direction if the car hits the screen edges
        if car[0] <= 0 or car[0] + police_car_width >= WIDTH:
            car[3] *= -1  # Reverse direction

        # Ensure police cars stay above the bottom half of the screen
        car[1] = min(car[1], HEIGHT // 2 - police_car_height)

        # Draw the police car
        screen.blit(police_car_image, (car[0], car[1]))


        # Collision with forklift
        if (forklift_x < car[0] + police_car_width and
            forklift_x + forklift_width > car[0] and
            forklift_y < car[1] + police_car_height and
            forklift_y + forklift_height > car[1]):
            if not invincible:  
                forklift_health = forklift_health - 10
                invincible = True  

            if forklift_health <= 0:
                pygame.quit()
                sys.exit()


    # Remove police cars that go off-screen or are destroyed
    police_cars = [car for car in police_cars if car[1] < HEIGHT // 2 and car[2] > 0]


    # Spawn hearts randomly (e.g., 0.5% chance per frame, and limit number of hearts)
    if len(hearts) < 2 and random.randint(1, 200) == 1:
        heart_x = random.randint(0, WIDTH - 50)
        heart_y = -50  # Start above the screen
        hearts.append([heart_x, heart_y])

    for heart in hearts:
        heart[1] += line_speed 
        screen.blit(Hears, (heart[0], heart[1]))

        # Check for collision with forklift
        if (forklift_x < heart[0] + 120 and
            forklift_x + forklift_width > heart[0] and
            forklift_y < heart[1] + 120 and
            forklift_y + forklift_height > heart[1]):
            forklift_health = min(forklift_health + 10, max_health)  
            hearts.remove(heart)

    # Remove hearts that go off-screen
    hearts = [heart for heart in hearts if heart[1] < HEIGHT]

    # Update and draw bullets (ROCKETS)
    for bullet in bullets[:]:
        bullet[1] -= 10  
        screen.blit(bullet_image, (bullet[0], bullet[1]))

        for car in police_cars[:]:
            if (bullet[0] < car[0] + police_car_width and
                bullet[0] + bullet_image.get_width() > car[0] and
                bullet[1] < car[1] + police_car_height and
                bullet[1] + bullet_image.get_height() > car[1]):
                car[2] -= 80  # Reduce car health
                if car[2] <= 0:
                    police_cars.remove(car)
                    police_cars_destroyed += 1
                    score += 10
                    # Add explosion at the car's position
                    explosions.append({"x": car[0], "y": car[1], "frame": 0, "timer": 0})
                bullets.remove(bullet)
                break

    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Police cars shoot bullets
    for car in police_cars:
        # 1% chance per frame to shoot a bullet
        if random.randint(1, 100) == 1:
            bullet_x = car[0] + police_car_width // 2 - police_bullet_image.get_width() // 2
            bullet_y = car[1] + police_car_height
            police_bullets.append([bullet_x, bullet_y])

    # Move police bullets and check collision with player
    for bullet in police_bullets[:]:
        bullet[1] += 10  # Bullet speed
        screen.blit(police_bullet_image, (bullet[0], bullet[1]))

        # Collision with forklift
        if (forklift_x < bullet[0] + police_bullet_image.get_width() and
            forklift_x + forklift_width > bullet[0] and
            forklift_y < bullet[1] + police_bullet_image.get_height() and
            forklift_y + forklift_height > bullet[1]):
            forklift_health = max(0, forklift_health - 10)
            police_bullets.remove(bullet)
            if forklift_health <= 0:
                pygame.quit()
                sys.exit()
        # Remove if off screen
        elif bullet[1] > HEIGHT:
            police_bullets.remove(bullet)

    if round_active:
        round_timer -= 1


    # Check if the round is complete
    if (police_cars_destroyed >= police_cars_required or round_timer <= 0) and round_active:

        round_active = False
        police_cars_destroyed = 0
        round_timer = round_time_limit * 60  # Reset timer for the next round

        # Clear police cars and bullets
        police_cars = []
        police_bullets = []

        # Show the reward menu and get the selected upgrade
        upgrade = reward_menu(screen, WIDTH, HEIGHT)  # Pass the required arguments

        # Apply the selected upgrade
        if upgrade == "firerate":
            rocket_cooldown_duration -= 1
        elif upgrade == "maxhp":
            max_health += 20
            forklift_health = max_health
        elif upgrade == "speed":
            line_speed += 2
            forklift_speed += 2
        elif upgrade == "autoturret":
            auto_turret_enabled = True
            auto_turret_damage += 5  # Increase auto turret damage by 5 each time

        # Start the next round
        current_round += 1
        police_cars_to_spawn += 2  # Increase the number of police cars for the next round
        police_cars_required += 1
        round_active = True

        # --- Boss Spawning Logic ---
        if current_round == 4 and not bosses:  # Spawn the boss only once
            print(f"Spawning boss with health: {boss_health}, damage: {boss_damage}, image: {boss_image}")
            print(f"Calling spawn_boss with: bosses={bosses}, WIDTH={WIDTH}, HEIGHT={HEIGHT}, boss_width=200, boss_height=200, boss_health={boss_health}, boss_damage={boss_damage}, boss_image={boss_image}")
            spawn_boss(bosses, WIDTH, HEIGHT, 200, 200, boss_health, boss_damage, boss_image)
            print(f"Boss spawned at: {bosses}")  # Debugging line

    screen.blit(forklift_image, (forklift_x, forklift_y))

    draw_health_bar(screen, 20, 20, 200, 20, forklift_health, max_health)
    score_text = font.render(f"Score: {score}", True, WHITE)
    highscore_text = font.render(f"Highscore: {highscore}", True, YELLOW)
    round_text = font.render(f"Round: {current_round}", True, WHITE)
    timer_text = font.render(f"Time Left: {round_timer // 60}s", True, RED)
    screen.blit(score_text, (20, 50))
    screen.blit(highscore_text, (20, 100))
    screen.blit(round_text, (20, 150))
    screen.blit(timer_text, (20, 200))

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
            if (bullet[0] < car[0] + police_car_width and
                bullet[0] + police_bullet_image.get_width() > car[0] and
                bullet[1] < car[1] + police_car_height and
                bullet[1] + police_bullet_image.get_height() > car[1]):
                car[2] -= auto_turret_damage  # Use variable damage
                auto_turret_bullets.remove(bullet)
                if car[2] <= 0:
                    police_cars.remove(car)
                    police_cars_destroyed += 1
                    score += 10
                break
        else:
            if bullet[1] < 0:
                auto_turret_bullets.remove(bullet)

    # --- UPGRADE MECHANIC ---
    # REMOVE or COMMENT OUT this block:
    # if score >= 100 and not upgrade_given:
    #     chosen_upgrade = reward_menu(screen, WIDTH, HEIGHT)
    #     print("Upgrade chosen:", chosen_upgrade)
    #     upgrade_given = True


    if bosses:
        for boss in bosses[:]:
            boss[0] += boss_direction * 3  # Move left or right
            if boss[0] <= 0 or boss[0] + 200 >= WIDTH:  # Reverse direction at edges
                boss_direction *= -1

            # Keep the boss in the top half of the screen
            boss[1] = min(boss[1], HEIGHT // 2 - 200)

        draw_bosses(bosses, screen)  # Draw the boss

        # Boss shooting logic
        boss_shoot_timer += 1
        if boss_shoot_timer >= 120: 
            boss_shoot_timer = 0
            for boss in bosses:
                boss_shoot(boss, boss_bullets, bullet_speed=5)

        # Update boss bullets
        update_boss_bullets(boss_bullets, screen, police_bullet_image)

        # Check for collisions between boss bullets and the forklift
        for bullet in boss_bullets[:]:
            if (forklift_x < bullet[0] + police_bullet_image.get_width() and
                forklift_x + forklift_width > bullet[0] and
                forklift_y < bullet[1] + police_bullet_image.get_height() and
                forklift_y + forklift_height > bullet[1]):
                forklift_health -= 25  # Boss bullet damage
                boss_bullets.remove(bullet)
                if forklift_health <= 0:
                    pygame.quit()
                    sys.exit()


        # Check for collision with the forklift
        for boss in bosses[:]:
            boss_x, boss_y, boss_health, _, _ = boss
            if (forklift_x < boss_x + 200 and
                forklift_x + forklift_width > boss_x and
                forklift_y < boss_y + 200 and
                forklift_y + forklift_height > boss_y):
                if not invincible:
                    forklift_health -= boss_damage
                    invincible = True
                if forklift_health <= 0:
                    pygame.quit()
                    sys.exit()


            if boss_health <= 0:
                bosses.remove(boss)
                score += 100  

    # Check for collisions between bullets and the boss
    for bullet in bullets[:]:
        for boss in bosses[:]:
            boss_x, boss_y, boss_health, _, boss_image = boss
            if (bullet[0] < boss_x + boss_image.get_width() and
                bullet[0] + bullet_image.get_width() > boss_x and
                bullet[1] < boss_y + boss_image.get_height() and
                bullet[1] + bullet_image.get_height() > boss_y):
                boss[2] -= 20  # Reduce boss health by 80
                bullets.remove(bullet)
                if boss[2] <= 0:  # Remove boss if health is 0
                    bosses.remove(boss)
                    score += 500  # Reward for defeating the boss
                break

    # Check for collisions between auto turret bullets and the boss
    for bullet in auto_turret_bullets[:]:
        for boss in bosses[:]:
            boss_x, boss_y, boss_health, _, boss_image = boss
            if (bullet[0] < boss_x + boss_image.get_width() and
                bullet[0] + police_bullet_image.get_width() > boss_x and
                bullet[1] < boss_y + boss_image.get_height() and
                bullet[1] + police_bullet_image.get_height() > boss_y):
                boss[2] -= auto_turret_damage  # Reduce boss health by turret damage
                auto_turret_bullets.remove(bullet)
                if boss[2] <= 0:  # Remove boss if health is 0
                    bosses.remove(boss)
                    score += 500  # Reward for defeating the boss
                break

    # Draw a health bar above the boss
    for boss in bosses:
        boss_x, boss_y, boss_health, _, boss_image = boss
        health_bar_width = boss_image.get_width()
        health_bar_height = 10
        health_ratio = boss_health / 500  # Assuming 500 is the max health
        pygame.draw.rect(screen, RED, (boss_x, boss_y - 20, health_bar_width, health_bar_height))  # Background
        pygame.draw.rect(screen, GREEN, (boss_x, boss_y - 20, health_bar_width * health_ratio, health_bar_height))  # Health

    # --- Spawn normal cars ---
    normal_car_spawn_timer += 1
    if normal_car_spawn_timer >= normal_car_spawn_delay:
        normal_car_spawn_timer = 0
        car_type, car_img = random.choice(normal_car_types)
        car_x = random.randint(0, WIDTH - 120)
        normal_cars.append([car_x, -120, car_type])

    # --- Move, draw, and handle collisions for normal cars ---
    for car in normal_cars[:]:
        car[1] += line_speed + 5  # Move faster than police cars
        # Draw the correct image, flipped vertically
        if car[2] == "red":
            flipped_img = pygame.transform.flip(red_car_image, False, True)
            screen.blit(flipped_img, (car[0], car[1]))
        elif car[2] == "blue":
            flipped_img = pygame.transform.flip(blue_car_image, False, True)
            screen.blit(flipped_img, (car[0], car[1]))
        elif car[2] == "green":
            flipped_img = pygame.transform.flip(green_car_image, False, True)
            screen.blit(flipped_img, (car[0], car[1]))

        # Remove if off screen
        if car[1] > HEIGHT:
            normal_cars.remove(car)
            continue

        # Collision with forklift
        if (forklift_x < car[0] + 120 and
            forklift_x + forklift_width > car[0] and
            forklift_y < car[1] + 120 and
            forklift_y + forklift_height > car[1]):
            normal_cars.remove(car)
            score += 15  # Award points for hitting with forklift
            continue

        # Collision with bullets
        for bullet in bullets[:]:
            if (bullet[0] < car[0] + 120 and
                bullet[0] + bullet_image.get_width() > car[0] and
                bullet[1] < car[1] + 120 and
                bullet[1] + bullet_image.get_height() > car[1]):
                normal_cars.remove(car)
                bullets.remove(bullet)
                score += 15  # Award points for shooting
                break

    # Manage and draw explosions
    for explosion in explosions[:]:
        explosion["timer"] += 1
        if explosion["timer"] >= 5:  # Adjust frame rate (higher = slower)
            explosion["timer"] = 0
            explosion["frame"] += 1
            if explosion["frame"] >= len(explosion_frames):  # If last frame is reached
                explosions.remove(explosion)  # Remove the explosion
                continue

        # Draw the current frame of the explosion
        frame = explosion_frames[explosion["frame"]]
        screen.blit(frame, (explosion["x"], explosion["y"]))

    pygame.display.flip()

pygame.quit()
sys.exit()