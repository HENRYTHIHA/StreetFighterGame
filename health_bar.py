import pygame 

class HealthBar:
    def __init__(self, x, y, width, height, max_health, color): 
        self.rect = pygame.Rect(x, y, width, height)
        self.max_health = max_health
        self.current_health = max_health 
        self.color = color 

    def update(self, health): 
        """Update the current health."""
        self.current_health = max(0, health)

    def draw(self, screen): 
        """Draw the health bar."""
        pygame.draw.rect(screen, (169, 169, 169), self.rect)

        health_width = (self.current_health / self.max_health) * self.rect.width 
        health_rect = pygame.Rect(self.rect.x, self.rect.y, health_width, self.rect.height)
        pygame.draw.rect(screen, self.color, health_rect)