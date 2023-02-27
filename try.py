import pygame
import random

# Set up the game window
WIDTH = 576
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Everwing")

# Load the images
dragon_image = pygame.image.load("Jade2.png")
bullet_image = pygame.image.load("bullet2.png")
bullet_image = pygame.transform.scale(bullet_image, (100, 100))
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (100, 100))  # scale to 100x100 pixels
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (576, 1080))


# Define the classes for the game objects
class Dragon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = dragon_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 15
        self.bullets = []
        self.bullet_speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
        elif keys[pygame.K_SPACE]:
            self.fire_bullet()
        self.update_bullets()

    def shoot(self):
        bullet = Bullet(self.x + self.width // 2, self.y)
        return bullet

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)
            else:
                for enemy in enemies:
                    if (bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2 < (bullet.width / 2 + enemy.width / 2) ** 2:
                        enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        return True
        return False

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
        self.speed = 3 
 
    def update(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x - self.width / 2, self.y)) 

class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

# Define the main game loop
dragon = Dragon(WIDTH / 2, HEIGHT - 100)
enemies = []
background = Background("background.jpg")
clock = pygame.time.Clock()
score = 0
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dragon.x -= dragon.speed
            elif event.key == pygame.K_RIGHT:
                dragon.x += dragon.speed
            elif event.key == pygame.K_SPACE:
                bullet = dragon.fire_bullet()
                if bullet is not None:
                    dragon.bullets.append(bullet)

    # Move the game objects
    dragon.update()
    for bullet in dragon.bullets:
        bullet.update()
    for enemy in enemies:
        enemy.update()
    dragon.update_bullets()

    # Generate new enemies
    if random.randint(0, 100) < 3:
        enemy = Enemy(random.randint(0, WIDTH), 0)
        enemies.append(enemy)

    # Draw the game objects
    background.draw(screen) # draw background first
    dragon.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in dragon.bullets:
        bullet.draw(screen)

    # Check for collisions
    for enemy in enemies:
        if (dragon.x - enemy.x) ** 2 + (dragon.y - enemy.y) ** 2 < (dragon.width / 2 + enemy.width / 2) ** 2:
            done = True
            break
        for bullet in dragon.bullets:
            if (bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2 < (bullet.width / 2 + enemy.width / 2) ** 2:
                enemies.remove(enemy)
                dragon.bullets.remove(bullet)
                score += 10

    # Display the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(60)

# Display the final score
screen.fill((0, 0, 0))
font = pygame.font.Font(None, 36)
text = font.render(f"Game over! Final score: {score}", True, (255, 255, 255))
text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
screen.blit(text, text_rect)
pygame.display.flip()
pygame.time.wait(3000)

# Clean up
pygame.quit()