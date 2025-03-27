import pygame
import os 
print(os.path.join(os.getcwd(), "assets/sprites/player_spritesheet.png"))

def extract_sprite(sheet, x, y, width, height): 
    """Extract a sprite from a sprite sheet at given x, y coordinates."""
    sprite = sheet.subsurface(pygame.Rect(x, x, width, height))
    return sprite

class Player:
    def __init__(self, x, y, name, controls):
        # Store player's name (optional)
        self.name = name
        # Initialize player rectangle and attributes
        self.rect = pygame.Rect(x, y, 50, 100)  # Player's main rectangle
        self.speed = 5
        self.controls = controls
        self.attacking = False
        self.kicking = False
        self.attack_cooldown = 0
        self.attack_rect = pygame.Rect(0, 0, 0, 0)  # Initialize attack rectangle
        self.kick_rect = pygame.Rect(0, 0, 0, 0)  # Initialize kick rectangle

        # Load sprite sheets
        self.sprite_sheet = pygame.image.load("assets/sprites/player_spritesheet.png")
        
        # Define sprite dimensions (adjust based on your sprite sheet)
        self.frame_width = 64
        self.frame_height = 64

        # Extract sprites for different animations (example: walking and punching)
        self.walking_frames = [extract_sprite(self.sprite_sheet, i * self.frame_width, 0, self.frame_width, self.frame_height) for i in range(4)]
        self.punch_frames = [extract_sprite(self.sprite_sheet, i * self.frame_width, self.frame_height, self.frame_width, self.frame_height) for i in range(3)]
        self.kick_frames = [extract_sprite(self.sprite_sheet, i * self.frame_width, 2 * self.frame_height, self.frame_width, self.frame_height) for i in range(3)]

        # Current animation frame index
        self.frame_index = 0
        self.frame_speed = 10  # Speed of the animation
        self.frame_counter = 0  # Counter to control the speed of animation
