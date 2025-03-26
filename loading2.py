import pygame
import time

pygame.init()

# Load sprite sheet (ensure the file is in the project directory or adjust the path)
try:
    sprite_sheet = pygame.image.load("Arcade - Street Fighter 2 Super Street Fighter 2 - Guile.png")
except pygame.error:
    print("Error: Could not load image. Make sure the file exists!")
    exit()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite & Loading Bar Together")
clock = pygame.time.Clock()

# Sprite settings
SPRITE_WIDTH = 380
SPRITE_HEIGHT = 175
frame = sprite_sheet.subsurface((0, 0, SPRITE_WIDTH, SPRITE_HEIGHT))
x_pos = (WIDTH - frame.get_width()) // 2
y_pos = (HEIGHT - frame.get_height()) // 2

# Colors
BACKGROUND_COLOR = (67, 70, 181)  # Hex #4346B5 converted to RGB
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
YELLOW = (220, 180, 50)
GRAY = (180, 180, 180)

# Loading bar settings
BAR_WIDTH, BAR_HEIGHT = 700, 50
BAR_X = (WIDTH - BAR_WIDTH) // 2
# Place the loading bar near the bottom of the screen
BAR_Y = HEIGHT - BAR_HEIGHT - 50  
# Text position above the loading bar
TEXT_Y = BAR_Y - 40  

OUTLINE_MARGIN = 3
NUM_SEGMENTS = 20
SPACING = 6  # Space between segments
SEGMENT_WIDTH = (BAR_WIDTH - (NUM_SEGMENTS - 1) * SPACING) / NUM_SEGMENTS

# Font settings
font = pygame.font.Font(None, 50)

def draw_loading_bar(filled_segments):
    """Draws the loading bar and its accompanying text."""
    # Draw loading text
    text = font.render("Loading to Start!", True, GRAY)
    text_rect = text.get_rect(center=(WIDTH // 2, TEXT_Y))
    screen.blit(text, text_rect)
    
    # Draw outline around the loading bar
    outline_rect = pygame.Rect(
        BAR_X - OUTLINE_MARGIN,
        BAR_Y - OUTLINE_MARGIN,
        BAR_WIDTH + 2 * OUTLINE_MARGIN,
        BAR_HEIGHT + 2 * OUTLINE_MARGIN
    )
    pygame.draw.rect(screen, WHITE, outline_rect, 3)
    
    # Draw each filled segment
    for i in range(filled_segments):
        segment_x = BAR_X + i * (SEGMENT_WIDTH + SPACING)
        pygame.draw.rect(screen, YELLOW, (segment_x, BAR_Y, SEGMENT_WIDTH, BAR_HEIGHT))

def main():
    progress = 0
    # Run the main loop, which updates both the sprite and loading bar concurrently.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Fill background with custom color #4346B5
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the sprite (centered)
        screen.blit(frame, (x_pos, y_pos))
        
        # Draw the loading bar (and text)
        draw_loading_bar(progress)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Update loading progress until complete
        if progress < NUM_SEGMENTS:
            progress += 1
            time.sleep(0.3)  # Delay to simulate loading; adjust as needed

if __name__ == "__main__":
    main()
