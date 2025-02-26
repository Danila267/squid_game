import pygame
import random
import time
import sys

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
MIN_BOT_SPEED = PLAYER_SPEED * 0.4  # Bot speed varies from 0.4x to 1.0x of player speed
MAX_BOT_SPEED = PLAYER_SPEED * 1.0  # Ensuring bots do not exceed player speed
REACTION_DELAY = 0.07  # Delay before bots or player are eliminated

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

green_light = True
last_switch_time = time.time()
killing_enabled = False  # Prevents instant death after switching

font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squid Game - Red Light Green Light")

def clamp_speed(speed):
    return max(MIN_BOT_SPEED, min(MAX_BOT_SPEED, speed))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text ("Space Invaders", font, WHITE, WIDTH // 3, HEIGHT // 6)
        draw_text ("1. начать игру ", small_font, WHITE, WIDTH // 3, HEIGHT // 3)
        draw_text ("2. правила", small_font, WHITE, WIDTH // 3, HEIGHT // 3 + 50)
        draw_text ("3. выход", small_font, WHITE, WIDTH // 3, HEIGHT // 3 + 100)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame. QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop()
                elif event.key == pygame.K_2:
                    show_rules()
                elif event.key == pygame.K_3:
                    sys.exit()


def switch_light():
    global green_light, last_switch_time, killing_enabled, bot_states, bot_speeds
    green_light = not green_light
    last_switch_time = time.time()
    killing_enabled = False  # Reset reaction timer
    
    if green_light:
        bot_speeds = [clamp_speed(random.uniform(MIN_BOT_SPEED, MAX_BOT_SPEED)) for _ in range(BOT_COUNT)]
    else:
        bot_states = [random.random() > 0.5 for _ in range(BOT_COUNT)]  # 50% chance for each bot to stop

def game_loop():
    global green_light, killing_enabled, last_switch_time, bot_states  # Ensure bot_states is global

    # Player Setup
    player_size = 50
    player_x, player_y = 100, HEIGHT // 2
    player = pygame.Rect(player_x, player_y, player_size, player_size)
    finish_line = WIDTH - 100

    # Bot Setup
    bots = []
    dead_bots = {}  # Store eliminated bot positions
    bot_states = []  # Track bot movement status (linked to switch_light)
    bot_speeds = []  

    for i in range(BOT_COUNT):
        bot_y = (i + 1) * BOT_SPACING + random.randint(-20, 20)
        bots.append(pygame.Rect(120, bot_y, player_size, player_size))
        bot_states.append(True)  # Bots start moving
        bot_speeds.append(random.uniform(MIN_BOT_SPEED, MAX_BOT_SPEED))

    bot_speeds = [clamp_speed(speed) for speed in bot_speeds]

    running = True

    while running:
        screen.fill(WHITE)
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Light Logic
        if time.time() - last_switch_time > (GREEN_LIGHT_TIME if green_light else RED_LIGHT_TIME):
            switch_light()
        
        if not green_light and time.time() - last_switch_time > REACTION_DELAY:
            killing_enabled = True  # Enable elimination after reaction delay
        
        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
        if not green_light and killing_enabled and keys[pygame.K_RIGHT]:
            print("You moved on RED! Game Over!")
            running = False
        
        # Bot Movement and Red Light Check
        surviving_bots = []
        surviving_states = []
        surviving_speeds = []

        for i, bot in enumerate(bots):
            if green_light or (not killing_enabled and bot_states[i]):  
                bot.x += bot_speeds[i]
            if not green_light and killing_enabled and not bot_states[i]:  # Bot moved when it should have stopped
                if random.random() < BOT_DEATH_CHANCE:
                    print(f"Bot {i} moved on RED! Eliminated!")
                    dead_bots[(bot.x, bot.y)] = bot_dead_img  
                else:
                    surviving_bots.append(bot)
                    surviving_states.append(bot_states[i])
                    surviving_speeds.append(bot_speeds[i])
            else:
                surviving_bots.append(bot)
                surviving_states.append(bot_states[i])
                surviving_speeds.append(bot_speeds[i])
        
        bots = surviving_bots
        bot_states = surviving_states
        bot_speeds = surviving_speeds
        
        # Check Win Condition
        if player.x >= finish_line:
            print("You won!")
            running = False
        
        # Draw Elements
        screen.blit(player_img, (player.x, player.y))
        for i, bot in enumerate(bots):
            if bot_states[i] or green_light:
                screen.blit(bot_img, (bot.x, bot.y))
        for (dead_x, dead_y), dead_img in dead_bots.items():
            screen.blit(dead_img, (dead_x, dead_y))  
        pygame.draw.line(screen, BLACK, (finish_line, 0), (finish_line, HEIGHT), 5)
        screen.blit(light_green_img if green_light else light_red_img, (WIDTH // 2 - 30, 20))
        
        # Update Screen
        pygame.display.flip()
        pygame.time.delay(30)

    pygame.quit()



main_menu()