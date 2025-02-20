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
MIN_BOT_SPEED = PLAYER_SPEED * 0.4  # Bot speed varies from 0.4x to 1.0x of player speed
MAX_BOT_SPEED = PLAYER_SPEED * 1.0  # Ensuring bots do not exceed player speed
REACTION_DELAY = 0.07  # Delay before bots or player are eliminated

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

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

# Font Setup
font = pygame.font.Font(None, 50)

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, w, h)
    
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, button_rect)
        if click[0]:
            return True
    else:
        pygame.draw.rect(screen, color, button_rect)
    
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)
    return False

def main_menu():
    while True:
        screen.fill(WHITE)
        if draw_button("Start", WIDTH // 2 - 100, HEIGHT // 3, 200, 60, GRAY, (170, 170, 170)):
            return "start"
        if draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 2, 200, 60, GRAY, (170, 170, 170)):
            pygame.quit()
            exit()
        pygame.display.flip()

def end_menu():
    while True:
        screen.fill(WHITE)
        if draw_button("Restart", WIDTH // 2 - 100, HEIGHT // 3, 200, 60, GRAY, (170, 170, 170)):
            return "restart"
        if draw_button("Main Menu", WIDTH // 2 - 100, HEIGHT // 2, 200, 60, GRAY, (170, 170, 170)):
            return "menu"
        if draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 1.5, 200, 60, GRAY, (170, 170, 170)):
            pygame.quit()
            exit()
        pygame.display.flip()

def game_loop():
    # Player Setup
    player_size = 50
    player_x, player_y = 100, HEIGHT // 2
    player = pygame.Rect(player_x, player_y, player_size, player_size)
    finish_line = WIDTH - 100

    # Bot Setup
    bots = []
    bot_states = []
    bot_speeds = []
    dead_bots = {}
    bot_start_x = 120
    for i in range(BOT_COUNT):
        bot_y = (i + 1) * BOT_SPACING + random.randint(-20, 20)
        bots.append(pygame.Rect(bot_start_x, bot_y, player_size, player_size))
        bot_states.append(True)
        bot_speeds.append(random.uniform(MIN_BOT_SPEED, MAX_BOT_SPEED))
    
    def clamp_speed(speed):
        return max(MIN_BOT_SPEED, min(MAX_BOT_SPEED, speed))
    
    bot_speeds = [clamp_speed(speed) for speed in bot_speeds]
    
    running = True
    green_light = True
    last_switch_time = time.time()
    killing_enabled = False
    
    def switch_light():
        nonlocal green_light, last_switch_time, killing_enabled, bot_speeds, bot_states
        green_light = not green_light
        last_switch_time = time.time()
        killing_enabled = False
        if green_light:
            bot_speeds = [clamp_speed(random.uniform(MIN_BOT_SPEED, MAX_BOT_SPEED)) for _ in range(BOT_COUNT)]
        else:
            bot_states = [random.random() > 0.5 for _ in range(BOT_COUNT)]
    
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        if time.time() - last_switch_time > (GREEN_LIGHT_TIME if green_light else RED_LIGHT_TIME):
            switch_light()
        
        if not green_light and time.time() - last_switch_time > REACTION_DELAY:
            killing_enabled = True
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
        if not green_light and killing_enabled and keys[pygame.K_RIGHT]:
            return "lost"
        
        surviving_bots = []
        surviving_states = []
        surviving_speeds = []
        for i, bot in enumerate(bots):
            if green_light or (not killing_enabled and bot_states[i]):
                bot.x += bot_speeds[i]
            if not green_light and killing_enabled and not bot_states[i]:
                if random.random() < BOT_DEATH_CHANCE:
                    dead_bots[(bot.x, bot.y)] = bot_dead_img
                else:
                    surviving_bots.append(bot)
                    surviving_states.append(bot_states[i])
                    surviving_speeds.append(bot_speeds[i])
            else:
                surviving_bots.append(bot)
                surviving_states.append(bot_states[i])
                surviving_speeds.append(bot_speeds[i])
        
        bots, bot_states, bot_speeds = surviving_bots, surviving_states, surviving_speeds
        if player.x >= finish_line:
            return "won"
        pygame.display.flip()
        pygame.time.delay(30)

while True:
    choice = main_menu()
    if choice == "start":
        outcome = game_loop()
        end_menu()
