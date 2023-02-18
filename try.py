import pygame
import random

# Set up the game window
WIDTH = 800
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Everwing")

# Load the images
dragon_image = pygame.image.load("Jade2.png")
bullet_image = pygame.image.load("bullet.png")
enemy_image = pygame.image.load("enemy.png")

# Define the classes for the game objects
class Dragon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = dragon_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 5
        self.bullets = []

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
        elif keys[pygame.K_SPACE]:
            self.fire_bullet()
        self.update_bullets()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)

    def fire_bullet(self):
        bullet = Bullet(self.x + self.width / 2, self.y)
        self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = bullet_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 10

    def update(self):
        self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x - self.width / 2, self.y))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = enemy_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 5

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x - self.width / 2, self.y))

