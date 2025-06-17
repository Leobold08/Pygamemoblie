import pygame 
import random
import math

def spawn_boss(bosses, WIDTH, HEIGHT, boss_width, boss_height, boss_health, boss_damage, boss_image, boss_type):
    boss_x = random.randint(0, WIDTH - boss_width)
    boss_y = random.randint(0, HEIGHT // 4)
    bosses.append([boss_x, boss_y, boss_health, boss_damage, boss_image, boss_type])

def draw_bosses(bosses, screen, boss_image):
    for boss in bosses:
        # Unpack only the first six elements, ignoring any extras
        boss_x, boss_y, boss_health, boss_damage, boss_image, boss_type = boss[:6]
        screen.blit(boss_image, (boss_x, boss_y))  # Draw the boss image at its position

def boss_shoot(boss, boss_bullets, bullet_speed, boss_width, boss_height, bullet_image):
    boss_x, boss_y, _, _, _, _ = boss[:6]  # Unpack the boss list correctly
    bullet_width = bullet_image.get_width()
    bullet_height = bullet_image.get_height()

    # Straight bullet
    angle_straight = math.radians(90)  # Straight down
    boss_bullets.append([
        boss_x + boss_width // 2 - bullet_width // 2,
        boss_y + boss_height,
        bullet_speed * math.cos(angle_straight),
        bullet_speed * math.sin(angle_straight),
        bullet_image  # Add bullet image to bullet data
    ])

    # Left angled bullet (-45 degrees)
    angle_left = math.radians(135)  # Adjusted to shoot left
    boss_bullets.append([
        boss_x + boss_width // 2 - bullet_width // 2,
        boss_y + boss_height,
        bullet_speed * math.cos(angle_left),
        bullet_speed * math.sin(angle_left),
        bullet_image  # Add bullet image to bullet data
    ])

    # Right angled bullet (+45 degrees)
    angle_right = math.radians(45)  # Adjusted to shoot right
    boss_bullets.append([
        boss_x + boss_width // 2 - bullet_width // 2,
        boss_y + boss_height,
        bullet_speed * math.cos(angle_right),
        bullet_speed * math.sin(angle_right),
        bullet_image  # Add bullet image to bullet data
    ])

def boss_shoot_tracking(boss, boss_bullets, forklift_x, forklift_y, bullet_speed, bullet_image):
    boss_x, boss_y, _, _, _, _ = boss[:6]
    bullet_width = bullet_image.get_width()
    bullet_height = bullet_image.get_height()

    # Calculate initial bullet position from the bottom-center of the boss
    bullet_x = boss_x + 100 - bullet_width // 2  # Center horizontally (boss width is 200)
    bullet_y = boss_y + 200  # Bottom of the boss (boss height is 200)

    # Calculate direction vector to forklift
    dx = forklift_x - bullet_x
    dy = forklift_y - bullet_y
    
    # Normalize the direction vector
    distance = math.sqrt(dx**2 + dy**2)
    if distance != 0:
        dx = (dx / distance) * bullet_speed
        dy = (dy / distance) * bullet_speed

    # Add the bullet with its velocity and image
    boss_bullets.append([
        bullet_x,          # x position
        bullet_y,          # y position
        dx,               # x velocity (scaled by speed)
        dy,               # y velocity (scaled by speed)
        bullet_image      # bullet image
    ])

def update_boss_bullets(boss_bullets, screen, bullet_image, WIDTH, HEIGHT):
    for bullet in boss_bullets[:]:
        bullet[0] += bullet[2]  # Horizontal movement
        bullet[1] += bullet[3]  # Vertical movement
        if len(bullet) > 4:  # If bullet has a specific image
            screen.blit(bullet[4], (bullet[0], bullet[1]))
        else:
            screen.blit(bullet_image, (bullet[0], bullet[1]))

        # Remove bullets that go off-screen
        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            boss_bullets.remove(bullet)

# Initialize required variables
bullet_image = pygame.Surface((10, 20))  
bullet_image.fill((255, 0, 0)) 
boss = [100, 100, 100, 10, bullet_image, "default"] 
boss_bullets = []  # List to store boss bullets

boss_shoot_timer = 0  # Initialize the shoot timer
# In your game loop or appropriate update function:
boss_shoot_timer += 1
if boss_shoot_timer >= 120:  # Shoot every 2 seconds (at 60 FPS)
    boss_shoot_timer = 0
    boss_shoot(boss, boss_bullets, bullet_speed=5, boss_width=100, boss_height=100, bullet_image=bullet_image)

# Update and draw boss bullets
