import pygame

WIDTH, HEIGHT = 1200, 800 # 1536, 1024

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, xSpeed = 10, ySpeed = 10):
        super().__init__()
        self.x = x
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.images = self.load_images("assets/bullet", 14)
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()   
        self.rect.center = (self.x, self.y)
        
    def load_images(self, path, length):
        images = []
        for i in range(1,length):
            image = pygame.image.load(f"{path}/Magic_Attack{i}.png")
            image = pygame.transform.scale(image, (15, 15))
            images.append(image)
        return images
    
    def update(self):
        self.frame += 0.1
        if self.frame < len(self.images):
            self.image = self.images[int(self.frame)]
        else:
            self.frame = 0
            
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.rect.center = (self.x, self.y)
        
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.kill()
