import pygame

class Player:
    def __init__(self, x, y, color, controls):
        self.image = pygame.Surface((50, 100))  
        self.image.fill(color)  
        self.rect = self.image.get_rect(topleft=(x, y))  
        self.speed = 5  
        self.controls = controls  

    def move(self, keys):
        """Move the player based on assigned controls."""
        if keys[self.controls["left"]]:
            self.rect.x -= self.speed
        if keys[self.controls["right"]]:
            self.rect.x += self.speed
        if keys[self.controls["up"]]:
            self.rect.y -= self.speed
        if keys[self.controls["down"]]:
            self.rect.y += self.speed

    def attact(self): 
        """Check if attack hits opponent and reduce health."""
        return self.attack_rect 

    def draw(self, screen):
        """Draw the player on the screen."""
        screen.blit(self.image, self.rect)
