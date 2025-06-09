import pygame
import sys
import random

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

forklift_width = 150
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
Hears = pygame.transform.scale(Hearts_image, (120, 120))
hearts_delay = 120
hearts_timer = 0

# List to hold active hearts
hearts = []

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

    # Draw the road image fullscreen
    screen.blit(road_image, (0, 0))  # Position the road image at the top-left corner

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
        bullets.append([bullet_x, bullet_y])  # Add bullet to the list
        rocket_cooldown = rocket_cooldown_duration  # Reset cooldown timer

    # Update cooldown timer
    if rocket_cooldown > 0:
        rocket_cooldown -= 1

    police_spawn_timer += 1
    if police_spawn_timer >= police_spawn_delay:
        police_spawn_timer = 0
        police_x = random.randint(0, WIDTH - police_car_width)
        police_cars.append([police_x, -police_car_height])

    # Spawn hearts periodically
    hearts_timer += 1
    if hearts_timer >= hearts_delay:
        hearts_timer = 0
        heart_x = random.randint(0, WIDTH - 120)
        hearts.append([heart_x, -120])  # Add heart to the list

    # Update invincibility timer
    if invincible:
        invincibility_timer += 1
        if invincibility_timer >= invincibility_duration:
            invincible = False
            invincibility_timer = 0

    for car in police_cars:
        car[1] += line_speed
        screen.blit(police_car_image, (car[0], car[1]))

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

    police_cars = [car for car in police_cars if car[1] < HEIGHT]

    # Update and draw hearts
    for heart in hearts:
        heart[1] += line_speed  # Move the heart downward
        screen.blit(Hears, (heart[0], heart[1]))

        # Check for collision with forklift
        if (forklift_x < heart[0] + 120 and
            forklift_x + forklift_width > heart[0] and
            forklift_y < heart[1] + 120 and
            forklift_y + forklift_height > heart[1]):
            forklift_health = min(forklift_health + 10, max_health)  # Increase health
            hearts.remove(heart)  # Remove the heart

    # Remove hearts that go off-screen
    hearts = [heart for heart in hearts if heart[1] < HEIGHT]

    # Update and draw bullets
    for bullet in bullets:
        bullet[1] -= 10  
        screen.blit(bullet_image, (bullet[0], bullet[1]))

        for car in police_cars:
            if (bullet[0] < car[0] + police_car_width and
                bullet[0] + bullet_image.get_width() > car[0] and
                bullet[1] < car[1] + police_car_height and
                bullet[1] + bullet_image.get_height() > car[1]):
                police_cars.remove(car) 
                bullets.remove(bullet) 
                break
    
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    screen.blit(forklift_image, (forklift_x, forklift_y))

    draw_health_bar(screen, 20, 20, 200, 20, forklift_health, max_health)

    pygame.display.flip()

pygame.quit()
sys.exit()