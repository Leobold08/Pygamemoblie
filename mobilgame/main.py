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
hearts_delay = 300
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

font = pygame.font.SysFont(None, 48)  # Add this after pygame.init() or after setting up the screen

road_scroll_y = 0

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
    if len(police_cars) < 7:
        police_spawn_timer += 1
        if police_spawn_timer >= police_spawn_delay:
            police_spawn_timer = 0
            police_x = random.randint(0, WIDTH - police_car_width)
            police_cars.append([police_x, -police_car_height])  # Spawn new police car

    for car in police_cars:
        # Move the police car downward
        car[1] += line_speed

        # Optional: Add slight horizontal movement for dynamic effect
        car[0] += random.choice([-1, 1])  # Move left or right randomly

        # Ensure police cars stay above the bottom half of the screen
        car[1] = min(car[1], HEIGHT // 2 - police_car_height)

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


    # Remove police cars that go off-screen or are destroyed
    police_cars = [car for car in police_cars if car[1] < HEIGHT // 2]


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

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet[1] -= 10  
        screen.blit(bullet_image, (bullet[0], bullet[1]))

        for car in police_cars[:]:
            if (bullet[0] < car[0] + police_car_width and
                bullet[0] + bullet_image.get_width() > car[0] and
                bullet[1] < car[1] + police_car_height and
                bullet[1] + bullet_image.get_height() > car[1]):
                police_cars.remove(car) 
                bullets.remove(bullet)
                score += 10 
                if score > highscore:
                    highscore = score
                    with open(highscore_file, "w") as f:
                        f.write(str(highscore))
                break
    
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    screen.blit(forklift_image, (forklift_x, forklift_y))

    draw_health_bar(screen, 20, 20, 200, 20, forklift_health, max_health)

    # Draw the score and highscore at the top left
    score_text = font.render(f"Score: {score}", True, WHITE)
    highscore_text = font.render(f"Highscore: {highscore}", True, YELLOW)
    screen.blit(score_text, (20, 50))
    screen.blit(highscore_text, (20, 100))

    pygame.display.flip()

pygame.quit()
sys.exit()