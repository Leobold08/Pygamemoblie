import pygame 
import random
import math

def spawn_boss(bosses, WIDTH, boss_width, boss_height, boss_heath, boss_damage):
    boss_x = random.randint(0, WIDTH - boss_width)
    bosses.append([boss_x, -boss_height, boss_heath, boss_damage])

def boss_shoot(boss, boss_bullets, bullet_speed):
    """
    Makes the boss shoot 3 bullets: one straight, one at 45° left, and one at 45° right.
    """
    boss_x, boss_y, _, _ = boss  # Extract boss position
    bullet_width = 10  # Example bullet width, adjust as needed
    bullet_height = 20  # Example bullet height, adjust as needed

    # Straight bullet
    boss_bullets.append([boss_x + bullet_width // 2, boss_y + bullet_height, 0, bullet_speed])

    # Left angled bullet (-45 degrees)
    angle_left = math.radians(-45)
    boss_bullets.append([
        boss_x + bullet_width // 2,
        boss_y + bullet_height,
        bullet_speed * math.cos(angle_left),
        bullet_speed * math.sin(angle_left)
    ])

    # Right angled bullet (+45 degrees)
    angle_right = math.radians(45)
    boss_bullets.append([
        boss_x + bullet_width // 2,
        boss_y + bullet_height,
        bullet_speed * math.cos(angle_right),
        bullet_speed * math.sin(angle_right)
    ])

def update_boss_bullets(boss_bullets, screen, bullet_image):

    for bullet in boss_bullets[:]:
        bullet[0] += bullet[2]  
        bullet[1] += bullet[3]  

        # Remove bullets that go off-screen
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

update_boss_bullets(boss_bullets, screen, bullet_image)

