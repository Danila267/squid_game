import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 1000, 600  # Increased width for longer gameplay
PLAYER_SPEED = 5
GREEN_LIGHT_TIME = 2
RED_LIGHT_TIME = 2
BOT_COUNT = 5
BOT_SPACING = HEIGHT // (BOT_COUNT + 1)  # Distribute bots evenly across the height
BOT_DEATH_CHANCE = 0.5  # Adjusted for more random deaths
MIN_BOT_SPEED = PLAYER_SPEED * 0.4  # Bot speed varies from 0.4x to 1.1x of player speed
MAX_BOT_SPEED = PLAYER_SPEED
REACTION_DELAY = 0.5  # Delay before bots or player are eliminated

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

# Bot Setup (Evenly spread along the starting line with slight variation)
bots = []
bot_states = []
bot_speeds = []  # Different speeds for bots
dead_bots = []  # Store positions of dead bots
bot_start_x = 120  # Ensure bots do not spawn too close to the player
for i in range(BOT_COUNT):
    bot_y = (i + 1) * BOT_SPACING + random.randint(-20, 20)  # Spread evenly with slight random offset
    bots.append(pygame.Rect(bot_start_x, bot_y, player_size, player_size))
    bot_states.append(random.choice([True, False]))  # Some bots obey red light, some don't
    bot_speeds.append(random.uniform(MIN_BOT_SPEED, MAX_BOT_SPEED))  # Random speeds for bots, properly varied

# Game Variables
running = True
green_light = True
last_switch_time = time.time()
killing_enabled = False  # Prevents instant death after switching

def switch_light():
    global green_light, last_switch_time, killing_enabled
    green_light = not green_light
    last_switch_time = time.time()
    killing_enabled = False  # Reset reaction timer

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
        elif time.time() - last_switch_time > REACTION_DELAY:
            killing_enabled = True  # Enable killing only after reaction delay
    
    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if green_light:
            player.x += PLAYER_SPEED
        elif killing_enabled:
            print("You moved on RED! Game Over!")
            running = False
    
    # Bot Movement and Red Light Check
    new_bots = []
    new_bot_states = []
    new_bot_speeds = []
    for i, bot in enumerate(bots):
        if green_light:
            bot.x += bot_speeds[i]
            new_bots.append(bot)
            new_bot_states.append(bot_states[i])
            new_bot_speeds.append(bot_speeds[i])
        else:
            if killing_enabled and not bot_states[i] and random.random() < BOT_DEATH_CHANCE:  # More varied deaths
                print(f"Bot {i} moved on RED! Eliminated!")
                dead_bots.append(bot)  # Store dead bot position
            else:
                new_bots.append(bot)
                new_bot_states.append(bot_states[i])
                new_bot_speeds.append(bot_speeds[i])
    
    bots = new_bots
    bot_states = new_bot_states
    bot_speeds = new_bot_speeds
    
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