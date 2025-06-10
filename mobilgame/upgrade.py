import pygame
import sys
import random
import os

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

police_cars = []  # List to hold police car positions
police_spawn_timer = 0
police_spawn_delay = 90  

# Load the road image
road_image = pygame.image.load("pictures/ROAD.png")
road_image = pygame.transform.scale(road_image, (WIDTH, HEIGHT))  # Scale to fullscreen dimensions

clock = pygame.time.Clock()
running = True


invincible = False
invincibility_timer = 0
invincibility_duration = 60  

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
highscore_file = "mobilgame/highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
else:
    highscore = 0

score = 0  # Current score

font = pygame.font.SysFont(None, 48)

road_scroll_y = 0

# Load police bullet image
police_bullet_image = pygame.image.load("pictures/bullet.png")
police_bullet_image = pygame.transform.scale(police_bullet_image, (30, 30))

police_bullets = []  # List to hold police bullets

def reward_menu():
    # Load images
    rpgammo_img = pygame.image.load("pictures/RPGAMMO.png")
    rpgammo_img = pygame.transform.scale(rpgammo_img, (100, 100))
    heart_img = pygame.image.load("pictures/heart.png")
    heart_img = pygame.transform.scale(heart_img, (100, 100))
    forklift_img = pygame.image.load("pictures/forklift.png")
    forklift_img = pygame.transform.scale(forklift_img, (100, 100))

    # List of upgrades and their actions
    upgrades = [
        ("firerate", rpgammo_img, "Faster Fire Rate"),
        ("maxhp", heart_img, "Increase Max HP"),
        ("speed", forklift_img, "Faster Movement")
    ]
    random.shuffle(upgrades)

    # Position upgrades horizontally centered
    spacing = 100
    total_width = 3 * 100 + 2 * spacing
    start_x = WIDTH // 2 - total_width // 2
    y = HEIGHT // 2 - 50

    menu_running = True
    font_small = pygame.font.SysFont(None, 32)  # Font for labels

    while menu_running:
        screen.fill(GRAY)
        font_big = pygame.font.SysFont(None, 60)
        text = font_big.render("Choose Your Upgrade!", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

        rects = []
        for i, (name, img, label) in enumerate(upgrades):
            x = start_x + i * (100 + spacing)
            rect = pygame.Rect(x, y, 100, 100)
            rects.append((rect, name))
            screen.blit(img, (x, y))
            # Draw label under the image
            label_surface = font_small.render(label, True, WHITE)
            label_x = x + 50 - label_surface.get_width() // 2
            label_y = y + 110  # 10px below the image
            screen.blit(label_surface, (label_x, label_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for rect, name in rects:
                    if rect.collidepoint(mx, my):
                        menu_running = False
                        return name  # Return the chosen upgrade

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


# Initialize round variables
current_round = 1
round_active = True
police_cars_to_spawn = 99999  # Number of police cars to spawn per round
police_cars_destroyed = 0
police_cars_required = 15  # Number of police cars to destroy to complete the round
round_time_limit = 180  # 3 minutes (in seconds)
round_timer = round_time_limit * 60  # Convert to frames (assuming 60 FPS)

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

    # Scroll the road image
    road_scroll_y += line_speed
    if road_scroll_y >= HEIGHT:
        road_scroll_y = 0

    screen.blit(road_image, (0, road_scroll_y - HEIGHT))  
    screen.blit(road_image, (0, road_scroll_y)) 

    # Spawn police cars for the current round
    if len(police_cars) < police_cars_to_spawn and round_active:
        police_spawn_timer += 1
        if police_spawn_timer >= police_spawn_delay:
            police_spawn_timer = 0
            police_x = random.randint(0, WIDTH - police_car_width)
            police_cars.append([police_x, -police_car_height])  # Spawn new police car

    for car in police_cars:
        # Move the police car downward
        car[1] += line_speed

        # Restrict police cars to the upper half of the screen
        car[1] = min(car[1], HEIGHT // 2 - police_car_height)

        # Add slight horizontal movement
        car[0] += random.choice([-1, 1])  # Slight horizontal movement
        car[0] = max(0, min(WIDTH - police_car_width, car[0]))  # Keep within bounds

        # Police shooting bullets
        if random.randint(0, 100) < 2:  # 2% chance to shoot per frame
            police_bullet_x = car[0] + police_car_width // 2 - police_bullet_image.get_width() // 2
            police_bullet_y = car[1] + police_car_height
            police_bullets.append([police_bullet_x, police_bullet_y])

        # Draw the police car
        screen.blit(police_car_image, (car[0], car[1]))

        # Check for collision with the forklift
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

    # Spawn bullets when right mouse button is clicked, respecting cooldown
    if pygame.mouse.get_pressed()[2] and rocket_cooldown == 0:  # Right mouse button
        bullet_x = forklift_x + forklift_width // 2 - bullet_image.get_width() // 2
        bullet_y = forklift_y
        bullets.append([bullet_x, bullet_y])  # Add bullet to the list
        rocket_cooldown = rocket_cooldown_duration  # Reset cooldown timer

    # Update cooldown timer
    if rocket_cooldown > 0:
        rocket_cooldown -= 1

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet[1] -= 10  # Move the bullet upward
        screen.blit(bullet_image, (bullet[0], bullet[1]))

        # Check for collision with police cars
        for car in police_cars[:]:
            if (bullet[0] < car[0] + police_car_width and
                bullet[0] + bullet_image.get_width() > car[0] and
                bullet[1] < car[1] + police_car_height and
                bullet[1] + bullet_image.get_height() > car[1]):
                police_cars.remove(car) 
                bullets.remove(bullet) 
                police_cars_destroyed += 1 
                score += 10  
                break

    # Update and draw police bullets
    for bullet in police_bullets[:]:
        bullet[1] += 10  # Move the bullet downward
        screen.blit(police_bullet_image, (bullet[0], bullet[1]))

        # Check for collision with the forklift
        if (forklift_x < bullet[0] + police_bullet_image.get_width() and
            forklift_x + forklift_width > bullet[0] and
            forklift_y < bullet[1] + police_bullet_image.get_height() and
            forklift_y + forklift_height > bullet[1]):
            forklift_health -= 5  # Reduce health on hit
            police_bullets.remove(bullet)

    # Spawn hearts periodically
    hearts_timer += 1
    if hearts_timer >= 180:  # Spawn a heart every 3 seconds (at 60 FPS)
        hearts_timer = 0
        heart_x = random.randint(0, WIDTH - Hears.get_width())
        hearts.append([heart_x, -Hears.get_height()])  # Spawn heart at the top

    # Update and draw hearts
    for heart in hearts[:]:
        heart[1] += line_speed  # Move the heart downward
        screen.blit(Hears, (heart[0], heart[1]))

        # Check for collision with the forklift
        if (forklift_x < heart[0] + Hears.get_width() and
            forklift_x + forklift_width > heart[0] and
            forklift_y < heart[1] + Hears.get_height() and
            forklift_y + forklift_height > heart[1]):
            forklift_health = min(forklift_health + 20, max_health)  # Increase health
            hearts.remove(heart)

    # Remove hearts that go off-screen
    hearts = [heart for heart in hearts if heart[1] < HEIGHT]

    # Remove bullets that go off-screen
    bullets = [bullet for bullet in bullets if bullet[1] > 0]
    police_bullets = [bullet for bullet in police_bullets if bullet[1] < HEIGHT]

    # Decrease the round timer
    if round_active:
        round_timer -= 1

    # Check if the round is complete
    if (police_cars_destroyed >= police_cars_required or round_timer <= 0) and round_active:
        round_active = False
        police_cars_destroyed = 0
        round_timer = round_time_limit * 60  # Reset timer for the next round
        # Show the reward menu
        upgrade = reward_menu()
        if upgrade == "firerate":
            rocket_cooldown_duration = max(5, rocket_cooldown_duration - 5)
        elif upgrade == "maxhp":
            max_health += 20
            forklift_health = max_health
        elif upgrade == "speed":
            forklift_speed += 2

        # Start the next round
        current_round += 1
        police_cars_to_spawn += 2  # Increase the number of police cars for the next round
        police_cars_required += 20
        round_active = True

    # Draw the forklift
    screen.blit(forklift_image, (forklift_x, forklift_y))

    draw_health_bar(screen, 20, 20, 200, 20, forklift_health, max_health)

    # Draw the score, highscore, round number, and timer
    score_text = font.render(f"Score: {score}", True, WHITE)
    highscore_text = font.render(f"Highscore: {highscore}", True, YELLOW)
    round_text = font.render(f"Round: {current_round}", True, WHITE)
    timer_text = font.render(f"Time Left: {round_timer // 60}s", True, RED)
    screen.blit(score_text, (20, 50))
    screen.blit(highscore_text, (20, 100))
    screen.blit(round_text, (20, 150))
    screen.blit(timer_text, (20, 200))

    pygame.display.flip()