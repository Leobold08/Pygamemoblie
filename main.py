import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forklift Road Drive")

GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 204, 0)
BLACK = (0, 0, 0)
CYEAN = (0, 255, 255)


forklift_width = 60
forklift_height = 100
forklift_x = WIDTH // 2 - forklift_width // 2
forklift_y = HEIGHT - forklift_height - 20
forklift_speed = 5

line_width = 10
line_height = 40
line_spacing = 40
line_speed = 5
lines = []
for i in range(0, HEIGHT, line_height + line_spacing):
    lines.append(i)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Update forklift position to follow the cursor
    forklift_x = mouse_x - forklift_width // 2


    # Ensure forklift stays within bounds
    forklift_x = max(60, min(WIDTH - forklift_width - 60, forklift_x))
    forklift_y = max(20, min(HEIGHT - forklift_height - 20, forklift_y))

    for i in range(len(lines)):
        lines[i] += line_speed
        if lines[i] > HEIGHT:
            lines[i] = -line_height

    screen.fill(CYEAN)
    pygame.draw.rect(screen, BLACK, (40, 0, WIDTH - 80, HEIGHT))

    if (pygame.mouse.get_pressed()[0]):
        line_speed = 10
    else:
        line_speed = 5

    if (pygame.mouse.get_pressed()[2]):
        pygame.quit()
        sys.exit()


    for y in lines:
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - line_width // 2, y, line_width, line_height))

    pygame.draw.rect(screen, YELLOW, (forklift_x, forklift_y, forklift_width, forklift_height))

    pygame.display.flip()

pygame.quit()
sys.exit()