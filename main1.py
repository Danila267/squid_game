import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
BOT_SPEED = 3
GREEN_LIGHT_TIME = 2
RED_LIGHT_TIME = 2
BOT_COUNT = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Load Images
player_img = pygame.image.load("player.png")
bot_img = pygame.image.load("bot.png")
light_green_img = pygame.image.load("light_green.png")
light_red_img = pygame.image.load("light_red.png")

# Resize Images
player_img = pygame.transform.scale(player_img, (50, 50))
bot_img = pygame.transform.scale(bot_img, (50, 50))
light_green_img = pygame.transform.scale(light_green_img, (60, 60))
light_red_img = pygame.transform.scale(light_red_img, (60, 60))

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squid Game - Red Light Green Light")

# Player Setup
player_size = 50
player = pygame.Rect(100, HEIGHT // 2, player_size, player_size)
finish_line = WIDTH - 100

# Bot Setup
bots = [pygame.Rect(random.randint(150, WIDTH - 200), random.randint(100, HEIGHT - 100), player_size, player_size) for _ in range(BOT_COUNT)]

# Game Variables
running = True
green_light = True
last_switch_time = time.time()

def switch_light():
    global green_light, last_switch_time
    green_light = not green_light
    last_switch_time = time.time()

# Game Loop
while running:
    screen.fill(WHITE)
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Light Logic
    if green_light:
        light_img = light_green_img
        if time.time() - last_switch_time > GREEN_LIGHT_TIME:
            switch_light()
    else:
        light_img = light_red_img
        if time.time() - last_switch_time > RED_LIGHT_TIME:
            switch_light()
    
    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if green_light:
            player.x += PLAYER_SPEED
        else:
            print("You moved on RED! Game Over!")
            running = False
    
    # Bot Movement
    for bot in bots:
        if green_light:
            bot.x += BOT_SPEED
    
    # Check Win Condition
    if player.x >= finish_line:
        print("You won!")
        running = False
    
    # Draw Elements
    screen.blit(player_img, (player.x, player.y))
    for bot in bots:
        screen.blit(bot_img, (bot.x, bot.y))
    pygame.draw.line(screen, BLACK, (finish_line, 0), (finish_line, HEIGHT), 5)
    screen.blit(light_img, (WIDTH // 2 - 30, 20))
    
    # Update Screen
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()