import pygame
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Trader:
    def __init__(self, x, y, api=None):
        self.api = api
        self.x = x
        self.y = y
        self.speed = 5
        
        self.state = "idle"
        self.state_timer = 0
        self.current_frame = 0
        self.direction = "right"  # Thêm biến direction để theo dõi hướng
        
        try:
            self.idle_images = self.load_images("assets/trader/Idle", 4)
            self.flight_images = self.load_images("assets/trader/Flight", 5)
            self.attack_images = self.load_images("assets/trader/Attack", 5)
            self.death_images = self.load_images("assets/trader/Death", 7)
            self.hurt_images = self.load_images("assets/trader/Hurt", 3)
            self.image = self.idle_images[0]
        except Exception as e:
            print(f"Error loading images: {e}")
            # Tạo một surface màu đỏ làm placeholder
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            self.idle_images = [self.image]
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.animation_counter = 0
        

            
        self.health = 100
        self.balance = 0
        self.positions = []
        self.orders = []
        
    def load_images(self, path = None, length = 9):
        images = []
        try:
            for i in range(1, length):
                img = pygame.image.load(f"{path}{i}.png")
                width, height = img.get_width(), img.get_height()
                img = pygame.transform.scale(img, (width*50/height, 50))
                images.append(img)
            return images
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Trả về một surface màu đỏ làm placeholder
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 0))
            return [placeholder]

    def update(self, keys):
        # cập nhật vị trí rect
        self.rect.topleft = (self.x, self.y)
        
        # Handle horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.state = "flight"
            # Update x position and handle boundaries
            if keys[pygame.K_LEFT]:
                self.x = max(0, self.x - self.speed)  # Don't go off left edge
                self.direction = "left"  # Cập nhật hướng khi di chuyển sang trái
            if keys[pygame.K_RIGHT]:
                self.x = min(1200 - self.image.get_width(), self.x + self.speed)  # Don't go off right edge
                self.direction = "right"  # Cập nhật hướng khi di chuyển sang phải
                
        # Handle vertical movement        
        elif keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.state = "flight"
            # Update y position and handle boundaries
            if keys[pygame.K_UP]:
                self.y = max(0, self.y - self.speed)  # Don't go off top edge
                self.direction = "up"
            if keys[pygame.K_DOWN]:
                self.y = min(800 - self.image.get_height(), self.y + self.speed)  # Don't go off bottom edge
                self.direction = "down"
            
        elif keys[pygame.K_SPACE]:
            # print(self.x, self.y)
            self.state = "attack"
            
        # No movement - return to idle state
        else:
            self.state = "idle"

        # Cập nhật animation
        self.current_frame += 0.1
            
        if self.state == "flight":
            if self.current_frame >= len(self.flight_images):
                self.current_frame = 0
            current_image = self.flight_images[int(self.current_frame)]
        elif self.state == "attack":
            if self.current_frame >= len(self.attack_images):
                self.current_frame = 0
            current_image = self.attack_images[int(self.current_frame)]
        elif self.state == "hurt":
            if self.current_frame >= len(self.hurt_images):
                self.current_frame = 0
            current_image = self.hurt_images[int(self.current_frame)]
        elif self.state == "death":
            if self.current_frame >= len(self.death_images):
                self.current_frame = 0
            current_image = self.death_images[int(self.current_frame)]
        elif self.state == "idle":
            if self.current_frame >= len(self.idle_images):
                self.current_frame = 0
            current_image = self.idle_images[int(self.current_frame)]
        
        # Lật hình ảnh nếu đang di chuyển sang trái
        self.image = pygame.transform.flip(current_image, self.direction == "left", False)
        
        # data = self.api.data.get('account', {})
        # self.balance = data.get('balance', 0)
        # self.positions = self.api.data.get('positions', [])
        # self.orders = self.api.data.get('orders', [])
        # # Cập nhật health dựa vào balance (ví dụ)
        # self.health = max(0, min(100, int((self.balance / 10000) * 100)))

    def draw(self, screen):
        # Vẽ nhân vật Trader là một hình tròn
        screen.blit(self.image, (self.x, self.y))
        
        
        # Vẽ thanh máu
        bar_width = 200
        bar_height = 15
        bar_x = screen.get_width()//2 - bar_width//2
        bar_y = 20

        # self.health = bar_width * (self.x / 1200)
  
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * (self.health / 100), bar_height))

        # Vẽ số dư tài khoản
        # font = pygame.font.SysFont(None, 24)
        # balance_text = font.render(f"${self.balance:,.2f}", True, (255, 255, 255))
        # screen.blit(balance_text, (self.position[0] - 40, self.position[1] + self.radius + 10))

        # Debug orders/positions nếu cần
        # print(self.positions, self.orders)
