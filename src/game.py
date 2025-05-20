import time
import pygame
import random
import os
import warnings

from src.bullet import Bullet
from src.utils import draw_text
from .trader import Trader
from .market import Market
from .explosion import Explosion

# from .ui import UI
# from .utils import *
# from .api_connector import TradingBotAPI

# Bỏ qua cảnh báo libpng
warnings.filterwarnings("ignore", category=UserWarning)

# Thiết lập biến môi trường để bỏ qua cảnh báo
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Khởi tạo Pygame và mixer
pygame.init()
pygame.mixer.init()  # Khởi tạo mixer để phát âm thanh

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 1200, 800 # 1536, 1024


class Game:
    def __init__(self):
        self.score = 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bgImage = pygame.image.load("assets/background/1.png")
        self.bgImage = pygame.transform.scale(self.bgImage, (WIDTH, HEIGHT))
        # Đặt caption cho cửa sổ game nên được đặt ngay sau khi tạo cửa sổ
        pygame.display.set_caption("Trading Bot")
        pygame.display.set_icon(pygame.image.load("assets/background/icon.png"))

        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.running = True
        
        # Load sounds
        try:
            # Load và phát nhạc nền
            pygame.mixer.music.load("assets/sounds/background.mp3")
            pygame.mixer.music.set_volume(0.5)  # Điều chỉnh âm lượng (0.0 đến 1.0)
            pygame.mixer.music.play(-1)  # -1 để phát lặp lại vô hạn
            
            # Load âm thanh nổ
            self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
            self.shoot_sound = pygame.mixer.Sound("assets/sounds/woosh.mp3")
            self.hurt_sound = pygame.mixer.Sound("assets/sounds/hurt.mp3")
            self.hurt_sound.set_volume(0.7)  # Điều chỉnh âm lượng âm thanh nổ
            self.shoot_sound.set_volume(0.7)  # Điều chỉnh âm lượng âm thanh nổ
            self.explosion_sound.set_volume(0.7)  # Điều chỉnh âm lượng âm thanh nổ
        except Exception as e:
            print(f"Error loading sounds: {e}") 
        
        self.trader = Trader(440, 670)
        
        # market
        self.markets = []
        self.spawn_markets(10)
        
        # explosion
        self.explosions = pygame.sprite.Group()
        
        # bullet
        self.bullets = pygame.sprite.Group()
        self.fire_delay = 100
        
        # self.ui = UI()
        # self.api = TradingBotAPI()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def spawn_markets(self, num_markets):
        for i in range(num_markets):
            x = random.randint(WIDTH//2, WIDTH - 100)  # Leave room for market width
            y = random.randint(100, HEIGHT//2 - 100)  # Leave room for market height
            market = Market(x, y)
            self.markets.append(market)
            # time.sleep(0.1)
    
    def update(self):
        # cập nhật trader
        #  a. click chuột điều khiển trader
        mouseClick = pygame.mouse.get_pressed()
        if mouseClick[0]:
            self.trader.x, self.trader.y =  pygame.mouse.get_pos() 
        
        # b.truyền phím điều khiển trader
        keys = pygame.key.get_pressed()
        if keys:
            self.trader.update(keys)
     
        
        # tạo bullet
        if keys[pygame.K_SPACE]:
            if self.fire_delay > 10:
                if self.trader.direction == "right":
                    xSpeed = 10
                    ySpeed = 0
                elif self.trader.direction == "left":
                    xSpeed = -10
                    ySpeed = 0
                elif self.trader.direction == "up":
                    xSpeed = 0
                    ySpeed = -10
                elif self.trader.direction == "down":
                    xSpeed = 0
                    ySpeed = 10
                    
                bullet = Bullet(self.trader.x+35, self.trader.y+28, xSpeed, ySpeed)
                self.bullets.add(bullet)
                self.shoot_sound.play()
                self.fire_delay = 0
            else:
                self.fire_delay += 1
                
                
        # cập nhật bullet
        self.bullets.update()
        
        # Cập nhật market
        markets_to_remove = set()
        bullets_to_remove = set()
        
        for market in self.markets:
            # kiểm tra va chạm với trader
            if market.rect.colliderect(self.trader.rect):
                if self.trader.x > market.x:
                    self.trader.x = 50
                elif self.trader.x < market.x:
                    self.trader.x = WIDTH -50
                if self.trader.y > market.y:
                    self.trader.y = 50
                elif self.trader.y < market.y:
                    self.trader.y = HEIGHT - 50
                    
                self.hurt_sound.play()
                print(self.trader.x, self.trader.y)
                self.trader.state = "hurt"
                self.trader.health -= 1
                if self.trader.health <= 0:
                    self.trader.state = "death"
                return # thoát để tránh va chạm với market khác
                
            # kiểm tra va chạm với bullet
            for bullet in self.bullets:
                if market.rect.colliderect(bullet.rect):
                    self.score += 1
                    bullets_to_remove.add(bullet)
                    markets_to_remove.add(market)
                    # Tạo explosion
                    explosion = Explosion(market.x, market.y)
                    self.explosions.add(explosion)
                    # Phát âm thanh nổ
                    try:
                        self.explosion_sound.play()
                    except:
                        pass
                    break  # Break after first collision to avoid multiple hits
            
            market.update(self.trader.rect)        
                    
        # Remove collected markets and bullets
        for market in markets_to_remove:
            if market in self.markets:
                self.markets.remove(market)
        
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        
        # nếu trader chết hết -> tạo thêm market
        if len(self.markets) <= 10:
            self.spawn_markets(20)
        
        
        # cập nhật explosion
        self.explosions.update()
        
    def run(self):  
        while self.running:
            self.clock.tick(self.FPS)
            # xử lý sự kiện
            self.handle_events()
            # cập nhật trạng thái keys
            self.update()
            # vẽ
            self.draw()

        pygame.quit()

    
    def draw_text(self, text, color, x,  y):
        text_surface, text_rect = draw_text(text, color, x, y)
        self.screen.blit(text_surface, text_rect)   

    
    def draw(self):
        # vẽ background vào screen
        self.screen.blit(self.bgImage, (0, 0))
        
        # vẽ text
        self.draw_text(f"Score: {self.score}   Bullet: {len(self.bullets)}", GREEN, 10, 10)
        self.draw_text(f"{self.trader.health}", BLUE, WIDTH//2 - 150, 15)
        self.draw_text(f"Markets: {len(self.markets)}", RED, WIDTH - 200, 10)
        
        
        # self.draw_text(f"Balance: {self.trader.balance}", GREEN, 10, 40)
        # self.draw_text(f"Positions: {self.trader.positions}", BLUE, 10, 70)
        # self.draw_text(f"Orders: {self.trader.orders}", YELLOW, 10, 100)
        
        # vẽ trader
        self.trader.draw(self.screen)
        
        # vẽ market
        for market in self.markets:
            market.draw(self.screen)
            
        # vẽ bullet
        self.bullets.draw(self.screen)
        
        # vẽ explosion
        self.explosions.draw(self.screen)
        
        # cập nhật screen
        pygame.display.flip()
