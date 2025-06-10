import pygame
import sys
import random
import os


def spawn_police_car(police_cars, WIDTH, police_car_width, police_car_height):
    police_x = random.randint(0, WIDTH - police_car_width)
    police_cars.append([police_x, -police_car_height])

def update_police_cars(police_cars, line_speed, HEIGHT, police_car_height):
    for car in police_cars:
        car[1] += line_speed
        car[1] = min(car[1], HEIGHT // 2 - police_car_height)
        car[0] += random.choice([-1, 1])
    return police_cars

def draw_police_cars(screen, police_cars, police_car_image):
    for car in police_cars:
        screen.blit(police_car_image, (car[0], car[1]))

def police_cars_shoot(police_cars, police_car_width, police_car_height, police_bullet_image):
    bullets = []
    for car in police_cars:
        if random.randint(0, 100) < 2:
            bullet_x = car[0] + police_car_width // 2 - police_bullet_image.get_width() // 2
            bullet_y = car[1] + police_car_height
            bullets.append([bullet_x, bullet_y])
    return bullets

def check_police_car_collision(police_cars, forklift_x, forklift_y, forklift_width, forklift_height, police_car_width, police_car_height, invincible):
    for car in police_cars:
        if (forklift_x < car[0] + police_car_width and
            forklift_x + forklift_width > car[0] and
            forklift_y < car[1] + police_car_height and
            forklift_y + forklift_height > car[1]):
            if not invincible:
                return car
    return None

