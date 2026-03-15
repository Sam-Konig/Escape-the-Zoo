import pygame
from basic_codes import settings as st

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
        self.frame_num = frame_num
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
        self.facingRight = True
        self.bodyMargin_x = 0
        self.bodyMargin_y = 0
        self.action = None

        self.data = {
            'running':{
                'PATH' : './img/player_1/running/running_{frame_num}.png',
                'FRAME_NUM' : 12,
                'SPEED' : [(40,0),(40,0),(40,0),(40,0),(40,0),(40,0),(40,0),(40,0),(40,0),(40,0),(40,0),(40,0)],
                'SIZE' : (180,215),
            },
            'jumping':{
                'PATH' : './img/player_1/jumping2/jumping_{frame_num}.png',
                'FRAME_NUM' : 12,
                'SPEED' : [(0,0),(0,0),(0,0),(0,-133),(0,-83),(0,-50),(0,0),(0,50),(0,83),(0,133),(0,0),(0,0)],
                'SIZE' : (180,215),
            },
            'leaping':{
                'PATH' : './img/player_1/leaping/leaping_{frame_num}.png',
                'FRAME_NUM' : 16,
                'SPEED' : [(40,0),(40,0),(50,0),(50,-133),(50,-83),(50,-50),(50,0),(50,0),(50,0),(50,0),(50,50),(50,83),(50,133),(50,0),(40,0),(40,0)],
                'SIZE' : (180,215),
            }
        }
    
    def init(self,x,y,facingRight = True):
        self.facingRight = facingRight
        self.getImages('running')
        if x < st.world_centerx - st.window_centerx + self.size[0] // 2:
            self.image_rect.center = (st.world_centerx - st.window_centerx + self.size[0] // 2, y)
        elif x > st.world_centerx + st.window_centerx - self.size[0] // 2:
            self.image_rect.center = (st.world_centerx + st.window_centerx - self.size[0] // 2, y)
        else: 
            self.image_rect.center = (x,y)
        self.rect_bottom = self.image_rect.bottom
        self.bodyMargin_x = (self.size[0] - st.playerStandardSize_x) // 2
        self.bodyMargin_y = (self.size[1] - st.playerStandardSize_y) // 2

    def getImages(self,action):
        self.action = action
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
        if self.facingRight:
            self.image = self.images[self.image_index]
        else:
            self.image = self.images_flipped[self.image_index]
        self.image_rect = self.image.get_rect()
    
    def event_handle(self,event):
        if self.isJumping == True:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.facingRight = False
                self.isMoving = True
                bottomLeft = self.image_rect.bottomleft
                self.getImages('running')
                self.image_rect.bottomleft = bottomLeft
            if event.key == pygame.K_RIGHT:
                self.facingRight = True
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
    
    def update(self, other_player = None):
        self.motion_count += 1
        if self.motion_count >= self.frame_rate:
            dx = 0
            dy = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            if self.facingRight == True:
                dx += self.speed[self.image_index][0]
                self.image = self.images[self.image_index]
            elif self.facingRight == False:
                dx -= self.speed[self.image_index][0]
                self.image = self.images_flipped[self.image_index]
            dy = self.speed[self.image_index][1]
            self.image_rect.centerx += dx
            # if other_player is not None:
            #     if abs(self.image_rect.centerx - other_player.image_rect.centerx) + self.size[0] + other_player.size[0] > st.window_width:
            #         self.image_rect.centerx -= dx
            self.image_rect.centerx = max(self.size[0] // 2, min(self.image_rect.centerx, st.world_width - self.size[0] // 2)) 
            self.image_rect.centery += dy
            self.motion_count = 0
            if self.isJumping == True and self.image_index == 0:
                self.isMoving = False
                self.isJumping = False
                self.image_rect.bottom = self.rect_bottom

    def getPosition(self,pos):
        if pos == 'left':
            return self.image_rect.left
        elif pos == 'right':
            return self.image_rect.right
        elif pos == 'top':
            return self.image_rect.top
        elif pos == 'bottom':
            return self.image_rect.bottom
        elif pos == 'centerx':
            return self.image_rect.centerx
        elif pos == 'centery':
            return self.image_rect.centery
        
    def setPosition(self,pos,value):
        if pos == 'left':
            self.image_rect.left = value
        elif pos == 'right':
            self.image_rect.right = value
        elif pos == 'top':
            self.image_rect.top = value
        elif pos == 'bottom':
            self.image_rect.bottom = value
        elif pos == 'centerx':
            self.image_rect.centerx = value
        elif pos == 'centery':
            self.image_rect.centery = value

    def draw(self,screen,camera_x = 0,camera_y = 0):
        screenX = self.image_rect.centerx - st.world_centerx + st.window_centerx - self.size[0] // 2
        screenY = self.image_rect.centery - st.world_centery + st.window_centery - self.size[1] // 2
        return screen.blit(self.image,(screenX - camera_x, screenY - camera_y))