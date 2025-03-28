import pygame
import sys

pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.music.load("02 Crimson Ken ~Burning Blood~ [KEN].mp3")
    pygame.mixer.music.play(-1)  
except pygame.error:
    print("Error: Could not load the music file. Make sure it exists!")

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Combined Loading & Moving Sprite")
clock = pygame.time.Clock()

BACKGROUND_COLOR = (67, 70, 181)  
WHITE = (200, 200, 200)
YELLOW = (220, 180, 50)
GRAY = (180, 180, 180)

# ----------------- LOADING BAR SETUP ---------------------------->
try:
    loading_sprite = pygame.image.load("streetfighter.png").convert_alpha()
except pygame.error:
    print("Error: Could not load 'streetfighter.png'. Make sure the file exists!")
    sys.exit()

SPRITE_WIDTH = 380
SPRITE_HEIGHT = 175
loading_frame = loading_sprite.subsurface((0, 0, SPRITE_WIDTH, SPRITE_HEIGHT))
loading_x = (WIDTH - loading_frame.get_width()) // 2
loading_y = (HEIGHT - loading_frame.get_height()) // 2 - 100

BAR_WIDTH, BAR_HEIGHT = 700, 50
BAR_X = (WIDTH - BAR_WIDTH) // 2
BAR_Y = HEIGHT - BAR_HEIGHT - 50  
TEXT_Y = BAR_Y - 40  

OUTLINE_MARGIN = 3
NUM_SEGMENTS = 30
SPACING = 5 
SEGMENT_WIDTH = (BAR_WIDTH - (NUM_SEGMENTS - 1) * SPACING) / NUM_SEGMENTS

font = pygame.font.Font(None, 50)

def draw_loading_bar(filled_segments, loaded):
    if not loaded:
        text = font.render("Loading to Start!", True, GRAY)
    else:
        text = font.render("<<Click to Start!>>", True, GRAY)
    text_rect = text.get_rect(center=(WIDTH // 2, TEXT_Y))
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

# ----------------- MOVING SPRITE SETUP -------------------------->
class Spritesheet:
    def __init__(self, image_path, rows, columns, scale=1.0):
        try:
            self.sheet = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            print(f"Error: Could not load '{image_path}'. Make sure the file exists!")
            pygame.quit()
            sys.exit()
        self.img_width = self.sheet.get_width()
        self.img_height = self.sheet.get_height()
        self.rows = rows      
        self.columns = columns 
        self.frame_width = self.img_width // self.columns
        self.frame_height = self.img_height // self.rows
        self.frame_index = (0, 0)  
        self.scale = scale

    def draw(self, surface, x, y):
        row, col = self.frame_index
        frame_x = col * self.frame_width
        frame_y = row * self.frame_height
        frame_image = self.sheet.subsurface((frame_x, frame_y, self.frame_width, self.frame_height))
        if self.scale != 1.0:
            scaled_width = int(self.frame_width * self.scale)
            scaled_height = int(self.frame_height * self.scale)
            frame_image = pygame.transform.scale(frame_image, (scaled_width, scaled_height))
        surface.blit(frame_image, (x, y))

    def next_frame(self):
        row, col = self.frame_index
        col += 1
        if col >= self.columns:
            col = 0
        self.frame_index = (row, col)

class FrameClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def transition(self, frame_duration):
        return self.time >= frame_duration

scale_factor = 0.5
spritesheet = Spritesheet("movingforward.png", rows=1, columns=5, scale=scale_factor)
frame_duration = 10  
frame_clock = FrameClock()

scaled_frame_width = int(spritesheet.frame_width * scale_factor)
scaled_frame_height = int(spritesheet.frame_height * scale_factor)

sprite_x = (WIDTH - scaled_frame_width) // 2
sprite_y = (HEIGHT - scaled_frame_height) // 2 + 60

# ----------------- FADE OUT FUNCTION -------------------------->
def fade_out():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    # Loop through alpha values from 0 to 255
    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

# ----------------- LOADING PROGRESS TIMER ------------------------->
progress = 0
loading_delay = 300  
last_loading_update = pygame.time.get_ticks()

def get_sprite_x(progress):
    return BAR_X + (progress / NUM_SEGMENTS) * (BAR_WIDTH - scaled_frame_width)

# MAIN LOOP ---------------------------->>>
waiting_for_click = False  

running = True
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if waiting_for_click and event.type == pygame.MOUSEBUTTONDOWN:
            fade_out()  # Call fade out after clicking
            running = False  
    
    if not waiting_for_click and progress < NUM_SEGMENTS and (current_time - last_loading_update >= loading_delay):
        progress += 1
        last_loading_update = current_time
    
    if progress >= NUM_SEGMENTS:
        waiting_for_click = True

    screen.fill(BACKGROUND_COLOR)
    
    screen.blit(loading_frame, (loading_x, loading_y))
    draw_loading_bar(progress, waiting_for_click)
    
    frame_clock.tick()
    if frame_clock.transition(frame_duration):
        spritesheet.next_frame()
        frame_clock.time = 0

    sprite_x = get_sprite_x(progress)
    spritesheet.draw(screen, sprite_x, sprite_y)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
