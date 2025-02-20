import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 1000, 600  # Increased width for longer gameplay
PLAYER_SPEED = 5
BOT_SPEED = 3
GREEN_LIGHT_TIME = 2
RED_LIGHT_TIME = 2
BOT_COUNT = 5
BOT_SPACING = 60
BOT_DEATH_CHANCE = 0.7  # Increased chance of dying on red

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Load Images
player_img = pygame.image.load("player.png")
bot_img = pygame.image.load("bot.png")
bot_dead_img = pygame.image.load("bot_dead.png")  # Image for dead bots
light_green_img = pygame.image.load("light_green.png")
light_red_img = pygame.image.load("light_red.png")

# Resize Images
player_img = pygame.transform.scale(player_img, (50, 50))
bot_img = pygame.transform.scale(bot_img, (50, 50))
bot_dead_img = pygame.transform.scale(bot_dead_img, (50, 50))
light_green_img = pygame.transform.scale(light_green_img, (60, 60))
light_red_img = pygame.transform.scale(light_red_img, (60, 60))

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squid Game - Red Light Green Light")

# Player Setup
player_size = 50
player_x, player_y = 100, HEIGHT // 2
player = pygame.Rect(player_x, player_y, player_size, player_size)
finish_line = WIDTH - 100

# Bot Setup (Spread above and below player, avoiding overlap)
bots = []
bot_states = []
dead_bots = []  # Store positions of dead bots
for i in range(BOT_COUNT):
    bot_y = player_y + (i - BOT_COUNT // 2) * BOT_SPACING
    bot_y = max(0, min(HEIGHT - player_size, bot_y))  # Keep bots within screen
    bots.append(pygame.Rect(100, bot_y, player_size, player_size))
    bot_states.append(random.choice([True, False]))  # Some bots obey red light, some don't

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
    
    # Bot Movement and Red Light Check
    new_bots = []
    new_bot_states = []
    for i, bot in enumerate(bots):
        if green_light:
            bot.x += BOT_SPEED
            new_bots.append(bot)
            new_bot_states.append(bot_states[i])
        else:
            if not bot_states[i] and random.random() < BOT_DEATH_CHANCE:  # Higher chance of dying on red
                print(f"Bot {i} moved on RED! Eliminated!")
                dead_bots.append(bot)  # Store dead bot position
            else:
                new_bots.append(bot)
                new_bot_states.append(bot_states[i])
    
    bots = new_bots
    bot_states = new_bot_states
    
    # Check Win Condition
    if player.x >= finish_line:
        print("You won!")
        running = False
    
    # Draw Elements
    screen.blit(player_img, (player.x, player.y))
    for bot in bots:
        screen.blit(bot_img, (bot.x, bot.y))
    for dead_bot in dead_bots:
        screen.blit(bot_dead_img, (dead_bot.x, dead_bot.y))  # Draw dead bot image
    pygame.draw.line(screen, BLACK, (finish_line, 0), (finish_line, HEIGHT), 5)
    screen.blit(light_img, (WIDTH // 2 - 30, 20))
    
    # Update Screen
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
