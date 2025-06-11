import pygame
import sys
import random

def reward_menu(screen, WIDTH, HEIGHT):
    # Load images
    rpgammo_img = pygame.image.load("pictures/RPGAMMO.png")
    rpgammo_img = pygame.transform.scale(rpgammo_img, (100, 100))
    heart_img = pygame.image.load("pictures/heart.png")
    heart_img = pygame.transform.scale(heart_img, (100, 100))
    forklift_img = pygame.image.load("pictures/forklift.png")
    forklift_img = pygame.transform.scale(forklift_img, (100, 100))
    turret_img = pygame.image.load("pictures/bullet.png")
    turret_img = pygame.transform.scale(turret_img, (100, 100))

    upgrades = [
        ("firerate", rpgammo_img, "Faster Fire Rate"),
        ("maxhp", heart_img, "Increase Max HP"),
        ("speed", forklift_img, "Faster Movement"),
        ("autoturret", turret_img, "Auto Turret"),
    ]
    random.shuffle(upgrades)
    upgrades = upgrades[:3]  # Only pick 3 random upgrades

    spacing = 100
    total_width = 3 * 100 + 2 * spacing
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
