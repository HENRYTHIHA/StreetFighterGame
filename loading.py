import pygame
import time

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Segmented Loading Bar with Larger Outline")

# Colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
YELLOW = (220, 180, 50)
GRAY = (180, 180, 180)

# Bar settings
BAR_WIDTH, BAR_HEIGHT = 700, 50
BAR_X = (WIDTH - BAR_WIDTH) // 2

# Font settings
#font = pygame.font.Font("Varsity.ttf", 50)
font = pygame.font.Font(None, 50)
text = font.render("Loading~~~", True, GRAY)
text_rect = text.get_rect()

gap = 10  # Gap between the bar and text
group_height = BAR_HEIGHT + gap + text_rect.height
start_y = (HEIGHT - group_height) // 2
BAR_Y = start_y
TEXT_Y = start_y + BAR_HEIGHT + gap

OUTLINE_MARGIN = 3

NUM_SEGMENTS = 20
SPACING = 6  # Space between segments

SEGMENT_WIDTH = (BAR_WIDTH - (NUM_SEGMENTS - 1) * SPACING) / NUM_SEGMENTS

def draw_loading_bar(filled_segments):
    screen.fill(BLACK)
    
    text = font.render("Loading to Start!", True, GRAY)
    text_rect = text.get_rect(center=(WIDTH // 2, TEXT_Y + text.get_height() // 2))
    screen.blit(text, text_rect)
    
    outline_rect = pygame.Rect(
        BAR_X - OUTLINE_MARGIN,
        BAR_Y - OUTLINE_MARGIN,
        BAR_WIDTH + 2 * OUTLINE_MARGIN,
        BAR_HEIGHT + 2 * OUTLINE_MARGIN
    )
    pygame.draw.rect(screen, WHITE, outline_rect, 3)
    
    for i in range(filled_segments):
        segment_x = BAR_X + i * (SEGMENT_WIDTH + SPACING)
        pygame.draw.rect(screen, YELLOW, (segment_x, BAR_Y, SEGMENT_WIDTH, BAR_HEIGHT))
    
    pygame.display.flip()

def main():
    progress = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if progress <= NUM_SEGMENTS:
            draw_loading_bar(progress)
            progress += 1
            time.sleep(0.3)
        else:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
