import pygame
import sys
sys.path.insert(0, '.')
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
            if other_player is not None:
                if abs(self.image_rect.centerx - other_player.image_rect.centerx) + self.size[0] + other_player.size[0] > st.window_width:
                    self.image_rect.centerx -= dx
            self.image_rect.centerx = max(self.size[0] // 2, min(self.image_rect.centerx, st.world_width - self.size[0] // 2)) 
            self.image_rect.centery += dy
            self.motion_count = 0
            if self.isJumping == True and self.image_index == 0:
                self.isMoving = False
                self.isJumping = False
                self.image_rect.bottom = self.rect_bottom

    def draw(self,screen,camera_x = 0,camera_y = 0):
        self.screenX = self.image_rect.centerx - st.world_centerx + st.window_centerx - self.size[0] // 2
        self.screenY = self.image_rect.centery - st.world_centery + st.window_centery - self.size[1] // 2
        return screen.blit(self.image,(self.screenX - camera_x, self.screenY - camera_y))