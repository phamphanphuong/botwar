import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = self.load_images("assets\\explosion")
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame = 0
    
    def load_images(self, path = None):
        images = []
        for i in range(1, 6):
            image = pygame.image.load(f"{path}\\exp{i}.png")
            images.append(image)
        return images
        
    def update(self):
        self.frame += 0.2
        if self.frame < len(self.images):
            self.image = self.images[int(self.frame)]
        else:
            self.kill()
        
    # def draw(self, screen):
    #     screen.blit(self.image, self.rect)

