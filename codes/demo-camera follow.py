import pygame

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# --- --- 初始参数 --- ---
FPS = 60
window_open = True
facingRight = True
motion_count = 0
window_width = 1280
window_height = 720
world_width = 2560
world_height = 1080
window_centerx = window_width//2
world_centerx = world_width//2
window_centery = window_height//2
world_centery = world_height//2

game_window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("镜头跟随与视差效果")

# try:
#     font = pygame.font.SysFont(["KaiTi","SimHei", "Arial"], 36)
# except:
#     font = pygame.font.Font(None, 36)
font = pygame.font.Font('./font/SourceHanSansTC-Bold.otf',36)
text1up = font.render("文案", True, (0,0,0))
text1up_rect = text1up.get_rect(center=(world_centerx+1280, world_centery))
text1down = font.render("koolins", True, (0,0,0))
text1down_rect = text1down.get_rect(center=(world_centerx+1280, world_centery+55))

class Background:
    def __init__(self,path,width=world_width,height=world_height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        image = pygame.image.load(path).convert_alpha()
        image_width,image_height = image.get_size()
        image_num = self.width // image_width
        image_x = (self.width - image_width) // 2
        image_y = (self.height - image_height) // 2
        for i in range(-image_num//2,image_num//2+1):
            self.surface.blit(image, (image_x + image_width * i, image_y))
        self.surface_x = window_centerx - self.width//2
        self.surface_y = window_centery - self.height//2

    def draw(self,screen,parallaxFactor):
        return screen.blit(self.surface,(self.surface_x - camera.x * parallaxFactor,self.surface_y - camera.y))

class Player:
    def __init__(self,
                path = None,
                frame_rate = 5,
                frame_num = None,
                speed = None,
                size = None,
                images = None,
                images_flipped = None,
                image_index = None,
                image = None,
                image_rect = None,
                rect_bottom = None):
        self.path = path
        self.frame_rate = frame_rate
        self.frame_nu = frame_num
        self.speed = speed
        self.size = size
        self.images = images if images is not None else []
        self.images_flipped = images_flipped if images_flipped is not None else []
        self.image_index = image_index
        self.image = image
        self.image_rect = image_rect
        self.rect_bottom = rect_bottom
        self.motion_count = 0
        self.isMoving = False
        self.isJumping = False
        self.screenX = 0
        self.screenY = 0

        self.data = {
            'running':{
                'PATH' : './img/player_1/running/running_{frame_num}.png',
                'FRAME_NUM' : 12,
                'SPEED' : [(24,0),(24,0),(24,0),(24,0),(24,0),(24,0),(24,0),(24,0),(24,0),(24,0),(24,0),(24,0)],
                'SIZE' : (108,129),
            },
            'jumping':{
                'PATH' : './img/player_1/jumping2/jumping_{frame_num}.png',
                'FRAME_NUM' : 12,
                'SPEED' : [(0,0),(0,0),(0,0),(0,-80),(0,-50),(0,-30),(0,0),(0,30),(0,50),(0,80),(0,0),(0,0)],
                'SIZE' : (108,144),
            },
            'leaping':{
                'PATH' : './img/player_1/leaping/leaping_{frame_num}.png',
                'FRAME_NUM' : 16,
                'SPEED' : [(24,0),(24,0),(30,0),(30,-80),(30,-50),(30,-30),(30,0),(30,0),(30,0),(30,0),(30,30),(30,50),(30,80),(30,0),(24,0),(24,0)],
                'SIZE' : (108,129),
            }
        }

    def getImages(self,action):
        self.path = self.data[action]['PATH']
        self.frame_num = self.data[action]['FRAME_NUM']
        self.speed = self.data[action]['SPEED']
        self.size = self.data[action]['SIZE']
        self.images = []
        for i in range(1, self.frame_num + 1):
            image_path = self.path.format(frame_num=i)
            loadingImage = pygame.image.load(image_path)
            loadingImage = pygame.transform.scale(loadingImage, self.size)
            self.images.append(loadingImage)
        self.images_flipped = [pygame.transform.flip(i, True, False) for i in self.images]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.image_rect = self.image.get_rect()
    
    def event_handle(self,event):
        if self.isJumping == True:
            return
        global facingRight
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                facingRight = False
                self.isMoving = True
                bottomLeft = self.image_rect.bottomleft
                self.getImages('running')
                self.image_rect.bottomleft = bottomLeft
            if event.key == pygame.K_RIGHT:
                facingRight = True
                self.isMoving = True
                bottomLeft = self.image_rect.bottomleft
                self.getImages('running')
                self.image_rect.bottomleft = bottomLeft
            if event.key == pygame.K_UP:
                self.isJumping = True
                self.isMoving = True
                bottomLeft = self.image_rect.bottomleft
                self.getImages('jumping')
                self.image_rect.bottomleft = bottomLeft
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.isMoving = False
            if event.key == pygame.K_RIGHT:
                self.isMoving = False
    
    def update(self):
        self.motion_count += 1
        if self.motion_count >= self.frame_rate:
            dx = 0
            dy = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            if facingRight == True:
                dx += self.speed[self.image_index][0]  # 恢复为局部变量
                self.image = self.images[self.image_index]
            elif facingRight == False:
                dx -= self.speed[self.image_index][0]  # 恢复为局部变量
                self.image = self.images_flipped[self.image_index]
            dy = self.speed[self.image_index][1]
            self.image_rect.centerx += dx  # 恢复角色x坐标增量
            self.image_rect.centerx = max(self.size[0] // 2, min(self.image_rect.centerx, world_width - self.size[0] // 2))
            self.image_rect.centery += dy
            self.screenX = self.image_rect.centerx - world_centerx + window_centerx - self.size[0] // 2
            self.screenY = self.image_rect.centery - world_centery + window_centery - self.size[1] // 2
            self.motion_count = 0
            if self.isJumping == True and self.image_index == 0:
                self.isMoving = False
                self.isJumping = False
                self.image_rect.bottom = self.rect_bottom

    def draw(self,screen):
        return screen.blit(self.image,(self.screenX - camera.x, self.screenY - camera.y))
        
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dead_zone = 100 # 单边范围，总静止区宽度为2*dead_zone
        self.target_ideal_x = window_centerx
        
    def update(self,player_x,player_y):
        target_screen_x = player_x - (world_centerx-window_centerx) - self.x
        offset = target_screen_x - self.target_ideal_x

        if offset > self.dead_zone:
            # 目标超出右边界，相机向右移动
            camera_target_x = player_x - (world_centerx-window_centerx) - (self.target_ideal_x + self.dead_zone)
        elif offset < -self.dead_zone:
            # 目标超出左边界，相机向左移动
            camera_target_x = player_x - (world_centerx-window_centerx) - (self.target_ideal_x - self.dead_zone)
        else:
            # 在静止区内，相机不移动
            camera_target_x = self.x

        if player.isMoving == True:
            self.x += (camera_target_x - self.x) * 0.05 
        elif player.isMoving == False:
            self.x += (camera_target_x - self.x) * 0.1

        max_camera_x = world_centerx - window_centerx
        min_camera_x = window_centerx - world_centerx
        self.x = max(min_camera_x, min(self.x, max_camera_x))

        camera_target_y = player_y - world_centery
        self.y += camera_target_y - self.y 

BG1 = Background('./img/bg/cloud.png')
BG2 = Background('./img/bg/mountain_far.png')
BG3 = Background('./img/bg/mountain_near.png')
BG4 = Background('./img/bg/road.png')
BG4.surface.blit(text1up,text1up_rect)
BG4.surface.blit(text1down,text1down_rect)
BG5 = Background('./img/bg/tree.png',width=3840)
BG6 = Background('./img/bg/bush.png',width=8000)
player = Player()
player.getImages('running')
player.image_rect.center = (world_width//2, world_height//2)
player.rect_bottom = player.image_rect.bottom
player.screenX = player.image_rect.centerx - world_centerx + window_centerx - player.size[0] // 2
player.screenY = player.image_rect.centery - world_centery + window_centery - player.size[1] // 2
camera = Camera()

while window_open:
    delta_time = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False
        if player.event_handle(event):
            pass


    camera.update(player.image_rect.centerx,player.image_rect.centery)
    if player.isMoving:
        player.update()
    
    update_rects = []
    bg_rect1 = BG1.draw(game_window,0.1)
    bg_rect2 = BG2.draw(game_window,0.3)
    bg_rect3 = BG3.draw(game_window,0.4)
    bg_rect4 = BG4.draw(game_window,1)
    player_rect = player.draw(game_window)
    bg_rect5 = BG5.draw(game_window,2)
    bg_rect6 = BG6.draw(game_window,5)
    
    update_rects.append(bg_rect1)
    update_rects.append(bg_rect2)
    update_rects.append(bg_rect3)
    update_rects.append(bg_rect4)
    update_rects.append(player_rect)
    update_rects.append(bg_rect5)
    update_rects.append(bg_rect6)
    pygame.display.update(update_rects)
pygame.quit() 