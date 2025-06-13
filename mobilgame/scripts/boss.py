import pygame 
import random
import math

def spawn_boss(bosses, WIDTH, HEIGHT, boss_width, boss_height, boss_health, boss_damage, boss_image):
    if WIDTH < boss_width or HEIGHT < boss_height:
        print("Error: Boss dimensions are larger than the screen!")
        return

    boss_x = random.randint(0, WIDTH - boss_width)  # Random x position
    boss_y = random.randint(0, HEIGHT // 4)  # Spawn in the top quarter of the screen
    bosses.append([boss_x, boss_y, boss_health, boss_damage, boss_image])
    print(f"Boss spawned at position: ({boss_x}, {boss_y}) with health: {boss_health}")

def draw_bosses(bosses, screen):
    for boss in bosses:
        boss_x, boss_y, _, _, boss_image = boss  # Unpack the boss list correctly
        screen.blit(boss_image, (boss_x, boss_y))  # Draw the boss image at its position

def boss_shoot(boss, boss_bullets, bullet_speed):
    boss_x, boss_y, _, _, _ = boss  # Extract boss position
    bullet_width = 20
    bullet_height = 20

    # Straight bullet
    boss_bullets.append([boss_x + 100 - bullet_width // 2, boss_y + 200, 0, bullet_speed])

    # Left angled bullet (-45 degrees)
    angle_left = math.radians(-45)
    boss_bullets.append([
        boss_x + 100 - bullet_width // 2,
        boss_y + 200,
        bullet_speed * math.cos(angle_left),
        bullet_speed * math.sin(angle_left)
    ])

    # Right angled bullet (+45 degrees)
    angle_right = math.radians(45)
    boss_bullets.append([
        boss_x + 100 - bullet_width // 2,
        boss_y + 200,
        bullet_speed * math.cos(angle_right),
        bullet_speed * math.sin(angle_right)
    ])

def update_boss_bullets(boss_bullets, screen, bullet_image):

    for bullet in boss_bullets[:]:
        bullet[0] += bullet[2]  
        bullet[1] += bullet[3]  


        if bullet[1] > screen.get_height() or bullet[0] < 0 or bullet[0] > screen.get_width():
            boss_bullets.remove(bullet)
        else:
            screen.blit(bullet_image, (bullet[0], bullet[1]))

# Initialize required variables
boss = [100, 100, 100, 10]  # Example boss: [x, y, health, damage]
boss_bullets = []  # List to store boss bullets
screen = pygame.display.set_mode((800, 600))  # Example screen setup
bullet_image = pygame.Surface((10, 20))  
bullet_image.fill((255, 0, 0)) 

boss_shoot_timer = 0  # Initialize the shoot timer
# In your game loop or appropriate update function:
boss_shoot_timer += 1
if boss_shoot_timer >= 120:  # Shoot every 2 seconds (at 60 FPS)
    boss_shoot_timer = 0
    boss_shoot(boss, boss_bullets, bullet_speed=5)

# Update and draw boss bullets