import pygame
import sys
from health_bar import HealthBar
from player import Player
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Fighter")

player1_health_bar = HealthBar(50, 20, 300, 25, max_health=100, color=(0, 255, 0))  # Green for Player 1
player2_health_bar = HealthBar(450, 20, 300, 25, max_health=100, color=(255, 0, 0))  # Red for Player 2

player1 = Player(100, 400, (0, 0, 255), { 
    "left": pygame.K_a,
    "right": pygame.K_d,
    "up": pygame.K_w,
    "down": pygame.K_s
})

player2 = Player(600, 400, (255, 255, 0), {  
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN
})

player1_health = 100
player2_health = 100


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    player1.move(keys)
    player2.move(keys)

    player1 = Player(100, 400, (0, 0 , 255), {
        "left": pygame.K_a,
        "right": pygame.K_d, 
        "up": pygame.K_w, 
        "down": pygame.K_s, 
        "attack": pygame.K_SPACE 
    })

    player2 = Player(600, 400, (255, 255, 0), {
        "left": pygame.K_LEFT, 
        "right": pygame.K_RIGHT,
        "up": pygame.K_UP,
        "down" : pygame.K_DOWN, 
        "attack": pygame.K_RETURN, 
    })

    if keys[player1.controls["attack"]]:
        if player1.attack().colliderect(player2.rect): 
            player2_health -= 1 
            print(f"player 1 hits Player 2! Player 2 Health: {player2_health}")

    if keys[player2.controls["attack"]]: 
        if player2.attack().colliderect(player1.rect): 
            player1_health -= 1
            print(f"Player 2 hits Player 1! Player 1 Health: {player1_health}")

    screen.fill((0, 0, 0))

    player1_health_bar.update(player1_health)
    player2_health_bar.update(player2_health)
    player1_health_bar.draw(screen)
    player2_health_bar.draw(screen)

    player1.draw(screen)
    player2.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()

