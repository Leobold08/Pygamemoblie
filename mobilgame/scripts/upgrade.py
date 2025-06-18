import pygame
import sys
import random

autoturret_enabled = False  

def reward_menu(screen, WIDTH, HEIGHT, num_upgrades=3, boss_upgrade=None):  # Default to 3 upgrades
    # Load images
    rpgammo_img = pygame.image.load("pictures/RPGAMMO.png")
    rpgammo_img = pygame.transform.scale(rpgammo_img, (100, 100))
    heart_img = pygame.image.load("pictures/heart.png")
    heart_img = pygame.transform.scale(heart_img, (100, 100))
    forklift_img = pygame.image.load("pictures/forklift.png")
    forklift_img = pygame.transform.scale(forklift_img, (100, 100))
    turret_img = pygame.image.load("pictures/bullet.png")
    turret_img = pygame.transform.scale(turret_img, (100, 100))
    bullet_img = pygame.image.load("pictures/bullet.png")  # Add bullet image for double shot
    bullet_img = pygame.transform.scale(bullet_img, (100, 100))

    # Define available upgrades
    if num_upgrades == 1:
        
        if autoturret_enabled:  # Boss upgrades
            upgrades = [
                ("triple_shot", bullet_img, "Triple shot"),
                ("damage_boost", rpgammo_img, "1.5x Damage")
            ]
        else:
            upgrades = [
                ("damage_boost", rpgammo_img, "1.5x Damage")
            ]
    else:
        # Regular upgrades remain the same
        upgrades = [
            ("firerate", rpgammo_img, "Faster Fire Rate"),
            ("maxhp", heart_img, "Increase Max HP"),
            ("speed", forklift_img, "Faster Movement"),
            ("autoturret", turret_img, "Auto Turret"),
        ]

    random.shuffle(upgrades)
    upgrades = upgrades[:num_upgrades]  # Pick the specified number of upgrades

    spacing = 100
    total_width = num_upgrades * 100 + (num_upgrades - 1) * spacing
    start_x = WIDTH // 2 - total_width // 2
    y = HEIGHT // 2 - 50

    menu_running = True
    font_small = pygame.font.SysFont(None, 32)
    font_big = pygame.font.SysFont(None, 60)

    while menu_running:
        screen.fill((50, 50, 50))
        text = font_big.render("Choose Your Upgrade!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

        rects = []
        for i, (name, img, label) in enumerate(upgrades):
            x = start_x + i * (100 + spacing)
            rect = pygame.Rect(x, y, 100, 100)
            rects.append((rect, name))
            screen.blit(img, (x, y))
            label_surface = font_small.render(label, True, (255, 255, 255))
            label_x = x + 50 - label_surface.get_width() // 2
            label_y = y + 110
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
                        return name

def military_boss_reward_menu(screen, WIDTH, HEIGHT):
    # Load images
    bullet_img = pygame.image.load("pictures/bullet.png")
    bullet_img = pygame.transform.scale(bullet_img, (100, 100))

    # Define military boss specific upgrades
    upgrades = [
        ("double_shot", bullet_img, "Double Shot")
    ]
    num_upgrades = 1

    # Menu setup
    spacing = 100
    total_width = num_upgrades * 100
    start_x = WIDTH // 2 - total_width // 2
    y = HEIGHT // 2 - 50

    menu_running = True
    font_small = pygame.font.SysFont(None, 32)
    font_big = pygame.font.SysFont(None, 60)

    while menu_running:
        screen.fill((50, 50, 50))
        text = font_big.render("Military Boss Defeated!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

        rects = []
        for i, (name, img, label) in enumerate(upgrades):
            x = start_x + i * (100 + spacing)
            rect = pygame.Rect(x, y, 100, 100)
            rects.append((rect, name))
            screen.blit(img, (x, y))
            label_surface = font_small.render(label, True, (255, 255, 255))
            label_x = x + 50 - label_surface.get_width() // 2
            label_y = y + 110
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
                        return name
