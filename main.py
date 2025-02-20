import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
GREEN_LIGHT_TIME = 2
RED_LIGHT_TIME = 2

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squid Game - Red Light Green Light")

# Player Setup
player_size = 50
player = pygame.Rect(100, HEIGHT // 2, player_size, player_size)
finish_line = WIDTH - 100

# Game Variables
running = True
green_light = True
last_switch_time = time.time()

# Fonts
font = pygame.font.Font(None, 50)

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
        light_color = GREEN
        if time.time() - last_switch_time > GREEN_LIGHT_TIME:
            switch_light()
    else:
        light_color = RED
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
    
    # Check Win Condition
    if player.x >= finish_line:
        print("You won!")
        running = False
    
    # Draw Elements
    pygame.draw.rect(screen, BLACK, player)
    pygame.draw.line(screen, BLACK, (finish_line, 0), (finish_line, HEIGHT), 5)
    pygame.draw.circle(screen, light_color, (WIDTH // 2, 50), 30)
    
    # Update Screen
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()