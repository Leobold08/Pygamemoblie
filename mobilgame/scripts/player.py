import pygame

class Player:
    def __init__(self, x, y, width, height, speed, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.max_health = max_health
        self.health = max_health
        self.image = pygame.image.load("pictures/forklift.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.invincible = False
        self.invincibility_timer = 0

    def move(self, mouse_x, mouse_y, screen_width, screen_height):
        self.x = max(0, min(screen_width - self.width, mouse_x - self.width // 2))
        self.y = max(screen_height // 2, min(screen_height - self.height, mouse_y - self.height // 2))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def set_max_health(self, new_max):
        self.max_health = new_max
        self.health = new_max

    def update_invincibility(self, duration):
        if self.invincible:
            self.invincibility_timer += 1
            if self.invincibility_timer > duration:
                self.invincible = False
                self.invincibility_timer = 0