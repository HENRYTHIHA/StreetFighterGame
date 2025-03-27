import pygame
import sys
import os
from health_bar import HealthBar
from player import Player
print(os.path.join(os.getcwd(), "assets/sprites/player_spritesheet.png"))

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_RED = (200, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Daniel vs Lucy")

# Create background
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((30, 30, 50))  # Dark blue background
# Draw ground
pygame.draw.rect(background, (80, 60, 40), (0, 450, SCREEN_WIDTH, SCREEN_HEIGHT-450))  # Brown ground
# Add title
font = pygame.font.Font(None, 60)
title = font.render("Daniel vs Lucy", True, (200, 200, 200))
background.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

# Create game objects
player1_health_bar = HealthBar(50, 20, 300, 25, 100, BLUE)
player2_health_bar = HealthBar(450, 20, 300, 25, 100, RED)

player1 = Player(100, 350, "player1", {
    "left": pygame.K_a, 
    "right": pygame.K_d, 
    "punch": pygame.K_j, 
    "kick": pygame.K_k
})
player2 = Player(600, 350, "player2", {})  # AI controlled

# Virtual controls
joystick_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 160, 80)  # Wider joystick area
punch_button = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 90, 60, 60)
kick_button = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90, 60, 60)

# Game state
clock = pygame.time.Clock()
running = True
player1_moving_left = False
player1_moving_right = False
vibration_intensity = 0
vibration_duration = 0
game_over = False
winner = None

def handle_ai(player, opponent, dt):
    """Simple AI for player 2"""
    if game_over:
        return
        
    # Move toward opponent
    if player.rect.x > opponent.rect.x + 50:
        player.rect.x -= player.speed * dt / 16
        player.facing_right = False
    elif player.rect.x < opponent.rect.x - 50:
        player.rect.x += player.speed * dt / 16
        player.facing_right = True
    
    # Random attacks when close
    distance = abs(player.rect.x - opponent.rect.x)
    if distance < 150 and pygame.time.get_ticks() % 120 == 0:
        if pygame.time.get_ticks() % 240 < 120:
            player.attack()
        else:
            player.kick()

def draw_virtual_controls():
    """Draw the on-screen controls"""
    if game_over:
        return
        
    pygame.draw.rect(screen, GRAY, joystick_rect, border_radius=40)
    pygame.draw.rect(screen, WHITE, punch_button, border_radius=30)
    pygame.draw.rect(screen, WHITE, kick_button, border_radius=30)
    
    # Button labels
    font = pygame.font.Font(None, 30)
    screen.blit(font.render("👊", True, BLACK), (punch_button.x + 15, punch_button.y + 15))
    screen.blit(font.render("🦵", True, BLACK), (kick_button.x + 15, kick_button.y + 15))

# Main game loop
while running:
    dt = clock.tick(FPS)  # Delta time for smooth movement
    
    # Handle vibration effect
    if vibration_duration > 0:
        vibration_duration -= dt
        offset_x = (pygame.time.get_ticks() % 100) - 50
        offset_y = (pygame.time.get_ticks() % 100) - 50
        screen_offset = (offset_x * vibration_intensity / 100, 
                        offset_y * vibration_intensity / 100)
    else:
        screen_offset = (0, 0)
        vibration_intensity = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse/touch controls
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            if joystick_rect.collidepoint(x, y):
                if x < joystick_rect.x + joystick_rect.width/2:
                    player1_moving_left = True
                else:
                    player1_moving_right = True
            elif punch_button.collidepoint(x, y):
                player1.attack()
                vibration_intensity = 30
                vibration_duration = 100
            elif kick_button.collidepoint(x, y):
                player1.kick()
                vibration_intensity = 50
                vibration_duration = 150
        
        elif event.type == pygame.MOUSEBUTTONUP:
            player1_moving_left = False
            player1_moving_right = False
        
        # Keyboard controls
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == player1.controls["left"]:
                    player1_moving_left = True
                elif event.key == player1.controls["right"]:
                    player1_moving_right = True
                elif event.key == player1.controls["punch"]:
                    player1.attack()
                    vibration_intensity = 30
                    vibration_duration = 100
                elif event.key == player1.controls["kick"]:
                    player1.kick()
                    vibration_intensity = 50
                    vibration_duration = 150
            
            # Restart game
            if game_over and event.key == pygame.K_r:
                # Reset game state
                player1_health_bar.current_health = 100
                player2_health_bar.current_health = 100
                player1.rect.x, player1.rect.y = 100, 350
                player2.rect.x, player2.rect.y = 600, 350
                game_over = False
                winner = None
        
        elif event.type == pygame.KEYUP:
            if event.key == player1.controls["left"]:
                player1_moving_left = False
            elif event.key == player1.controls["right"]:
                player1_moving_right = False

    if not game_over:
        # Movement handling
        if player1_moving_left:
            player1.rect.x -= player1.speed
            player1.facing_right = False
        if player1_moving_right:
            player1.rect.x += player1.speed
            player1.facing_right = True

        # AI for player 2
        handle_ai(player2, player1, dt)

        # Update players
        player1.update(dt)
        player2.update(dt)

        # Boundary checking
        player1.rect.x = max(0, min(SCREEN_WIDTH - player1.rect.width, player1.rect.x))
        player2.rect.x = max(0, min(SCREEN_WIDTH - player2.rect.width, player2.rect.x))

        # Check for attacks hitting
        for attacker, defender, health_bar in [(player1, player2, player2_health_bar), 
                                            (player2, player1, player1_health_bar)]:
            if attacker.attacking or attacker.kicking:
                attack_rect = attacker.attack_rect if attacker.attacking else attacker.kick_rect
                if attack_rect and attack_rect.colliderect(defender.rect):
                    # Gradually reduce health
                    health_bar.update(health_bar.current_health - 0.5)
                    
                    # Check for game over
                    if health_bar.current_health <= 0:
                        game_over = True
                        winner = "player1" if health_bar == player2_health_bar else "player2"
                        
                    # Knockback effect
                    knockback_dir = 1 if attacker.rect.x < defender.rect.x else -1
                    defender.rect.x += knockback_dir * 20
                    vibration_intensity = 70
                    vibration_duration = 200

    # Drawing
    screen.blit(background, screen_offset)
    
    # Health bars
    player1_health_bar.draw(screen)
    player2_health_bar.draw(screen)

    # Players
    player1.draw(screen)
    player2.draw(screen)

    # Virtual controls
    draw_virtual_controls()

    # Game over display
    if game_over:
        # Create oval background
        oval_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 400, 200)
        pygame.draw.ellipse(screen, YELLOW if winner == "player2" else GREEN, oval_rect)
        pygame.draw.ellipse(screen, BLACK, oval_rect, 3)  # Border
        
        # Game over text
        font_large = pygame.font.Font(None, 72)
        if winner == "player1":
            text = font_large.render("MISSION ACCOMPLISHED", True, (0, 100, 0))
        else:
            text = font_large.render("GAME OVER", True, DARK_RED)
        
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 
                          SCREEN_HEIGHT//2 - text.get_height()//2))
        
        # Add restart prompt
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to restart", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                                   SCREEN_HEIGHT//2 + 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
