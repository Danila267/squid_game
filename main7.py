import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 1000, 600  
PLAYER_SPEED = 5
GREEN_LIGHT_TIME = 2
RED_LIGHT_TIME = 2
BOT_COUNT = 5
BOT_SPACING = HEIGHT // (BOT_COUNT + 1)  
BOT_DEATH_CHANCE = 0.5
MIN_BOT_SPEED = PLAYER_SPEED * 0.4  
MAX_BOT_SPEED = PLAYER_SPEED * 1.0
REACTION_DELAY = 0.07

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Load Images
player_img = pygame.image.load("player.png")
bot_img = pygame.image.load("bot.png")
bot_dead_img = pygame.image.load("bot_dead.png")
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

# Button Class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, self.hover_color if self.rect.collidepoint(mouse_pos) else self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Main Menu

def main_menu():
    while True:
        screen.fill(WHITE)
        start_button = Button("Start", WIDTH // 2 - 75, HEIGHT // 2 - 50, 150, 50, GRAY, BLACK, game_loop)
        quit_button = Button("Quit", WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50, GRAY, BLACK, pygame.quit)
        
        start_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if start_button.is_clicked(event):
                return game_loop()
            if quit_button.is_clicked(event):
                pygame.quit()
                return

# End Menu

def end_menu():
    while True:
        screen.fill(WHITE)
        restart_button = Button("Restart", WIDTH // 2 - 75, HEIGHT // 2 - 50, 150, 50, GRAY, BLACK, game_loop)
        main_menu_button = Button("Main Menu", WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50, GRAY, BLACK, main_menu)
        quit_button = Button("Quit", WIDTH // 2 - 75, HEIGHT // 2 + 90, 150, 50, GRAY, BLACK, pygame.quit)

        restart_button.draw(screen)
        main_menu_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if restart_button.is_clicked(event):
                return game_loop()
            if main_menu_button.is_clicked(event):
                return main_menu()
            if quit_button.is_clicked(event):
                pygame.quit()
                return

# Game Loop

def game_loop():
    # Reset game variables
    player = pygame.Rect(100, HEIGHT // 2, 50, 50)
    bots = [pygame.Rect(120, (i + 1) * BOT_SPACING + random.randint(-20, 20), 50, 50) for i in range(BOT_COUNT)]
    bot_states = [True] * BOT_COUNT
    bot_speeds = [random.uniform(MIN_BOT_SPEED, MAX_BOT_SPEED) for _ in range(BOT_COUNT)]
    dead_bots = {}
    green_light = True
    last_switch_time = time.time()
    killing_enabled = False
    running = True
    
    while running:
        screen.fill(WHITE)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Light switch logic
        if time.time() - last_switch_time > (GREEN_LIGHT_TIME if green_light else RED_LIGHT_TIME):
            green_light = not green_light
            last_switch_time = time.time()
            killing_enabled = False
            if green_light:
                bot_speeds = [random.uniform(MIN_BOT_SPEED, MAX_BOT_SPEED) for _ in range(BOT_COUNT)]
            else:
                bot_states = [random.random() > 0.5 for _ in range(BOT_COUNT)]
        
        if not green_light and time.time() - last_switch_time > REACTION_DELAY:
            killing_enabled = True
        
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
        if not green_light and killing_enabled and keys[pygame.K_RIGHT]:
            return end_menu()
        
        # Bot movement and elimination
        new_bots = []
        new_states = []
        new_speeds = []
        for i, bot in enumerate(bots):
            if green_light or (not killing_enabled and bot_states[i]):
                bot.x += bot_speeds[i]
            if not green_light and killing_enabled and not bot_states[i]:
                if random.random() < BOT_DEATH_CHANCE:
                    dead_bots[(bot.x, bot.y)] = bot_dead_img
                else:
                    new_bots.append(bot)
                    new_states.append(bot_states[i])
                    new_speeds.append(bot_speeds[i])
            else:
                new_bots.append(bot)
                new_states.append(bot_states[i])
                new_speeds.append(bot_speeds[i])
        bots, bot_states, bot_speeds = new_bots, new_states, new_speeds
        
        if player.x >= WIDTH - 100:
            return end_menu()
        
        pygame.display.flip()
        pygame.time.delay(30)

main_menu()
