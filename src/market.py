import math
import pygame


class Market:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        self.speed = 0.5
        self.state = "attack"
        self.current_frame = 0
        self.animation_counter = 0
        self.direction = "right"
        
        self.attack_images = self.load_images("assets\\market\\Attack", 5)
        self.walk_images = self.load_images("assets\\market\\Walk", 7)
        self.idle_images = self.load_images("assets\\market\\Idle", 4)
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def load_images(self, path = None, length = 11):
        images = []
        try:
            for i in range(1, length):
                img = pygame.image.load(f"{path}{i}.png")
                img = pygame.transform.flip(img, True, False)
                img = pygame.transform.scale_by(img, 0.5)
                images.append(img)
            return images
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Tạo một surface màu đỏ làm placeholder
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 0))
            return [placeholder]
    
    def move_to(self, x, y):
        dx, dy = 0, 0
        if self.x < x:
            dx = self.speed
        elif self.x > x:
            dx = -self.speed
        if self.y < y:
            dy = self.speed
        elif self.y > y:
            dy = -self.speed
        
        self.x += dx
        self.y += dy
        
        if dx > 0:
            self.direction = "left"
        elif dx < 0:
            self.direction = "right"
            
    def update(self, player_rect):
        distance = math.sqrt((self.x - player_rect.x) ** 2 + (self.y - player_rect.y) ** 2)
        if distance < 100:
            self.state = "attack"
        else:
            self.state = "walk"
            
        # Cập nhật animation
        self.current_frame += 0.1
        
        if self.state == "attack":
            if self.current_frame >= len(self.attack_images):
                self.current_frame = 0      
            self.image = self.attack_images[int(self.current_frame)]
            
        elif self.state == "walk":
            if self.current_frame >= len(self.walk_images):
                self.current_frame = 0      
            self.image = self.walk_images[int(self.current_frame)]
            
        self.image = pygame.transform.flip(self.image, self.direction == "left", False)
        
        # đuổi theo trader
        self.move_to(player_rect.x, player_rect.y)
        
        # Cập nhật vị trí rect
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Kiểm tra va chạm với player
        if self.rect.colliderect(player_rect):
            # print("Collision!")
            return True  # Trả về True nếu có va chạm
        return False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        
            

