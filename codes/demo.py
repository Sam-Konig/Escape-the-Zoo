import pygame
import random

pygame.init()
clock = pygame.time.Clock()
FPS = 60
window_open = True
facingRight = True
motion_count = 0
game_window = pygame.display.set_mode((1280,720))
background = pygame.image.load('./img/bg/background.png')

try:
    font = pygame.font.SysFont(["KaiTi","SimHei", "Arial"], 36)
except:
    font = pygame.font.Font(None, 36)

data = {
    'running':{
        'PATH' : './img/player_1/running/running_{frame_num}.png',
        'FRAME_NUM' : 12,
        'SPEED' : (18,0),
        'SIZE' : (108,129),
    },
    'jumping':{
        'PATH' : './img/player_1/jumping/jumping_{frame_num}.png',
        'FRAME_NUM' : 14,
        'SPEED' : (0,0),
        'SIZE' : (108,240),
    },
    'punching':{
        'PATH' : './img/player_1/punching/punching_{frame_num}.png',
        'FRAME_NUM' : 21,
        'SPEED' : (0,0),
        'SIZE' : (150,129),
    },
    'kicking' : {
        'PATH' : './img/player_1/kicking/kicking_{frame_num}.png',
        'FRAME_NUM' : 20,
        'SPEED' : (0,0),
        'SIZE' : (150,129),
    },
    'throwing' : {
        'PATH' : './img/player_1/throwing/throwing_{frame_num}.png',
        'FRAME_NUM' : 15,
        'SPEED' : (0,0),
        'SIZE' : (108,180),
    }
}

class ButtonRect:
    def __init__(self, text, x, y, width, height,
                 text_color=(0, 0, 0), 
                 bg_color=(200, 200, 200),
                 hover_color=(150, 150, 150),
                 click_text_color=(200,200,200),
                 click_bg_color=(20,20,20)):

        self.button_rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.default_text_color = text_color
        self.default_bg_color = bg_color
        self.hover_color = hover_color
        self.click_bg_color = click_bg_color
        self.click_text_color = click_text_color

        self.is_hovered = False
        self.is_clicked = False
        self.click_count = 0
        self.click_pause = 6

        self.update_text()

    def update_text(self, color=None):
        text_color = color or self.default_text_color
        self.text_surface = font.render(self.text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)

    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.is_clicked = True
                self.button_rect.x += 4
                self.button_rect.y += 4
                self.update_text(self.click_text_color)  # 更新文字颜色
                return True  # 返回点击状态
        return False
    
    def update(self):
        if self.is_clicked:
            self.click_count += 1
            if self.click_count >= self.click_pause:
                self.is_clicked = False
                self.click_count = 0
                self.button_rect.x -= 4
                self.button_rect.y -= 4
                self.update_text()
        self.is_hovered = self.button_rect.collidepoint(pygame.mouse.get_pos())
    
    def draw(self, surface):
        if self.is_clicked:
            color = self.click_bg_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.default_bg_color
        pygame.draw.rect(surface, color, self.button_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.button_rect, 2) 
        surface.blit(self.text_surface, self.text_rect)

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    
    @property
    def center(self):
        return (self.x, self.y)
    
    def collidepoint(self, point):
        px, py = point
        return (px - self.x)**2 + (py - self.y)**2 <= self.radius**2

class ButtonCircle:
    def __init__(self, text, x, y, radius,
                 text_color=(0, 0, 0), 
                 bg_color=(200, 200, 200),
                 hover_color=(150, 150, 150),
                 click_text_color=(200,200,200),
                 click_bg_color=(20,20,20)):

        self.button_circle = Circle(x,y,radius)
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.default_text_color = text_color
        self.default_bg_color = bg_color
        self.hover_color = hover_color
        self.click_bg_color = click_bg_color
        self.click_text_color = click_text_color

        self.is_hovered = False
        self.is_clicked = False
        self.click_count = 0
        self.click_pause = 6

        self.update_text()

    def update_text(self, color=None):
        text_color = color or self.default_text_color
        self.text_surface = font.render(self.text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.button_circle.center)

    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_circle.collidepoint(event.pos):
                self.is_clicked = True
                self.button_circle.x += 4
                self.button_circle.y += 4
                self.update_text(self.click_text_color)  # 更新文字颜色
                return True  # 返回点击状态
        return False
    
    def update(self):
        if self.is_clicked:
            self.click_count += 1
            if self.click_count >= self.click_pause:
                self.is_clicked = False
                self.click_count = 0
                self.button_circle.x -= 4
                self.button_circle.y -= 4
                self.update_text()
        self.is_hovered = self.button_circle.collidepoint(pygame.mouse.get_pos())
    
    def draw(self, surface):
        if self.is_clicked:
            color = self.click_bg_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.default_bg_color
        pygame.draw.circle(surface, color, self.button_circle.center,self.button_circle.radius)
        pygame.draw.circle(surface, (0, 0, 0), self.button_circle.center,self.button_circle.radius, 3) 
        surface.blit(self.text_surface, self.text_rect)

toThrow = False
button_full_screen = ButtonRect(text="全屏",x=1160, y=30,width=80, height=50)
button_left = ButtonCircle(text="左",x=150, y=570, radius=30)
button_right = ButtonCircle(text="右",x=300, y=570, radius=30)
button_run = ButtonCircle(text="跑",x=225, y=495, radius=30)
button_jump = ButtonCircle(text="跳",x=225, y=645, radius=30)
button_punch = ButtonCircle(text="拳",x=940, y=510, radius=30)
button_kick = ButtonCircle(text="踢",x=920, y=600, radius=30)
button_throw = ButtonCircle(text="元气弹",x=1050, y=570, radius=60, bg_color=(250,125,0),hover_color=(200,100,0),click_bg_color=(100,50,0))

def draw_wave(surface, width, height, center, radius, color=(0, 255, 255), alpha=250):
    temp_surface = pygame.Surface((width, height), pygame.SRCALPHA) 
    pygame.draw.circle(temp_surface, (*color, alpha), center, radius)
    surface.blit(temp_surface, (0, 0))

waves = []
frame_count = 0

path = None
frame_rate = 5
frame_num = None
speed = None
size = None
images = []
images_flipped = []
image_index = None
image = None
image_rect = None
pre_rect_bottom = None

def getImages(action):
    global path, frame_num, speed, size, images, images_flipped, image_index, image, image_rect
    path = data[action]['PATH']
    frame_num = data[action]['FRAME_NUM']
    speed = data[action]['SPEED']
    size = data[action]['SIZE']
    images = []
    for i in range(1, frame_num + 1):
        image_path = path.format(frame_num=i)
        loadingImage = pygame.image.load(image_path)
        loadingImage = pygame.transform.scale(loadingImage, size)
        images.append(loadingImage)
    images_flipped = [pygame.transform.flip(i, True, False) for i in images]
    image_index = 0
    image = images[image_index]
    image_rect = image.get_rect()

getImages('running')
image_rect.bottomleft= (0, 460)
# --- --- koolins@bilibili
while window_open:
    delta_time = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False

        if button_full_screen.event_handle(event):
            pass
        if button_left.event_handle(event):
            facingRight = False
        if button_right.event_handle(event):
            facingRight = True
        if button_run.event_handle(event):
            pre_bottom = image_rect.bottomleft
            getImages('running')
            image_rect.bottomleft = pre_bottom
        if button_jump.event_handle(event):
            pre_bottom = image_rect.bottomleft
            getImages('jumping')
            image_rect.bottomleft = pre_bottom
        if button_kick.event_handle(event):
            pre_bottom = image_rect.bottomleft
            getImages('kicking')
            image_rect.bottomleft = pre_bottom
        if button_punch.event_handle(event):
            pre_bottom = image_rect.bottomleft
            getImages('punching')
            image_rect.bottomleft = pre_bottom
        if button_throw.event_handle(event):
            toThrow = True
            pre_bottom = image_rect.bottomleft
            getImages('throwing')
            image_rect.bottomleft = pre_bottom
            centerx= image_rect.x + 54
            centery= image_rect.y
            waves.append(([centerx,centery], 0, 500))

    if toThrow == True:
        frame_count += 1
        if image_index == 9:
           frame_rate = 210
        elif image_index == 13:
            frame_rate = 360
        else:
            frame_rate = 5
    motion_count += 1
    if motion_count >= frame_rate:
        image_index = (image_index + 1) % len(images)
        if facingRight == True:
            image_rect.x += speed[0]
            image = images[image_index]
        elif facingRight == False:
            image_rect.x -= speed[0]
            image = images_flipped[image_index]
        motion_count = 0 
    game_window.blit(background,background.get_rect())
    button_full_screen.update()   
    button_left.update()
    button_right.update() 
    button_run.update()
    button_jump.update()
    button_kick.update()
    button_punch.update()
    button_throw.update()
    button_full_screen.draw(game_window)
    button_left.draw(game_window)
    button_right.draw(game_window)
    button_run.draw(game_window)
    button_jump.draw(game_window)
    button_kick.draw(game_window)
    button_punch.draw(game_window)
    button_throw.draw(game_window)
    game_window.blit(image,image_rect)
    if frame_count >= 480:
        active_waves = []
        for center, radius, max_radius in waves:
            draw_wave(game_window, 1280, 720, center, radius, 
                    color=(random.randint(50, 255), random.randint(100, 255), 255))
            center += 1  #这里故意写错，让程序崩溃关闭
            active_waves.append((center, radius + 1, max_radius))
        waves = active_waves
    elif frame_count >= 255:
        active_waves = []
        for center, radius, max_radius in waves:
            draw_wave(game_window, 1280, 720, center, radius, 
                    color=(random.randint(50, 255), random.randint(100, 255), 255))
            center[0] += 1
            center[1] += 1
            active_waves.append((center, radius + 1, max_radius))
        waves = active_waves
    elif frame_count >=195 and frame_count < 255:
            draw_wave(game_window, 1280, 720, center, radius, 
                    color=(random.randint(50, 255), random.randint(100, 255), 255))
    elif frame_count < 195 and frame_count >= 75:
        active_waves = []
        for center, radius, max_radius in waves:
            if radius < max_radius:
                draw_wave(game_window, 1280, 720, center, radius, 
                    color=(random.randint(50, 255), random.randint(100, 255), 255))
                center[1] -= 1
                active_waves.append((center, radius + 1, max_radius))
        waves = active_waves
    pygame.display.flip()
pygame.quit() 
