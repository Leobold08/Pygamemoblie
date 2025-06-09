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
police_spawn_delay = 90  # Frames between spawns

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    forklift_x = mouse_x - forklift_width // 2
    forklift_x = max(60, min(WIDTH - forklift_width - 60, forklift_x))
    forklift_y = max(20, min(HEIGHT - forklift_height - 20, forklift_y))

    for i in range(len(lines)):
        lines[i] += line_speed
        if lines[i] > HEIGHT:
            lines[i] = -line_height

    screen.fill(CYEAN)
    pygame.draw.rect(screen, BLACK, (40, 0, WIDTH - 80, HEIGHT))

    if pygame.mouse.get_pressed()[0]:
        forklift_speed = 10 
        line_speed = 10
    else:
        forklift_speed = 5
        line_speed = 5

    if pygame.mouse.get_pressed()[2]: 
        forklift_health =  forklift_health - 1
        if (forklift_health < 0):
            pygame.quit()
            sys.exit()

    # Spawn police car at random x at the top
    police_spawn_timer += 1
    if police_spawn_timer >= police_spawn_delay:
        police_spawn_timer = 0
        police_x = random.randint(60, WIDTH - police_car_width - 60)
        police_cars.append([police_x, -police_car_height])

    # Move police cars down and draw them
    for car in police_cars:
        car[1] += line_speed  # Move down at same speed as lines
        screen.blit(police_car_image, (car[0], car[1]))

    # Remove police cars that move off the screen
    police_cars = [car for car in police_cars if car[1] < HEIGHT]

    for y in lines:
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - line_width // 2, y, line_width, line_height * 2) )


    screen.blit(forklift_image, (forklift_x, forklift_y))

    draw_health_bar(screen, 20, 20, 200, 20, forklift_health, max_health)

    pygame.display.flip()

pygame.quit()
sys.exit()