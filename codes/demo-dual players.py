import pygame
import gameUI
import text_button
import player
import playerbigger
from basic_codes import settings as st

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# --- --- 初始参数 --- ---
FPS = 60
window_open = True
motion_count = 0
window_width = st.window_width
window_height = st.window_height
world_width = st.world_width
world_height = st.world_height
window_centerx = st.window_centerx
window_centery = st.window_centery
world_centerx = st.world_centerx
world_centery = st.world_centery
min_zoom = 0.8
max_zoom = 1.0

game_window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("事件发射器")

class Background:
    def __init__(self,path=None,width=world_width,height=world_height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.surface_x = window_centerx - self.width//2
        self.surface_y = window_centery - self.height//2
        if path == None: return
        image = pygame.image.load(path).convert_alpha()
        image_width,image_height = image.get_size()
        image_num = self.width // image_width
        image_x = (self.width - image_width) // 2
        image_y = (self.height - image_height) // 2
        for i in range(-image_num//2,image_num//2+1):
            self.surface.blit(image, (image_x + image_width * i, image_y))

    def draw(self,screen,parallaxFactor):
        # return screen.blit(self.surface,(self.surface_x - camera.x * parallaxFactor,self.surface_y - camera.y))
        return screen.blit(self.surface,(self.surface_x - camera.x * parallaxFactor,self.surface_y - camera.y))

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.deadzone = 50

    def update(self, player1, player2):
        player1Left = player1.getPosition('left')
        player2Left = player2.getPosition('left')
        player1Right = player1.getPosition('right')
        player2Right = player2.getPosition('right')
        player1CenterX = player1.getPosition('centerx')
        player2CenterX = player2.getPosition('centerx')
        player1CenterY = player1.getPosition('centery')
        player2CenterY = player2.getPosition('centery')

        screenLeft = world_centerx - window_centerx + camera.x
        screenRight = world_centerx - window_centerx + camera.x + window_width
        playerLeft = min(player1Left,player2Left)
        playerRight = max(player1Right,player2Right)

        anchor_x = (player1CenterX + player2CenterX) // 2
        anchor_y = (player1CenterY + player2CenterY) // 2

        camera_target_x = anchor_x - world_centerx
        camera_target_y = anchor_y - world_centery

        offset_x = camera_target_x - self.x

        if offset_x > self.deadzone:
            target_x = camera_target_x - self.deadzone
        elif offset_x < - self.deadzone:
            target_x = camera_target_x + self.deadzone
        else:
            target_x = self.x
        
        target_y = camera_target_y
        
        if not playerLeft < screenLeft + offset_x and not playerRight > screenRight + offset_x:

    # 每帧更新，factor 通常 0.05~0.15
            self.x += (target_x - self.x) * 0.1
            self.y += (target_y - self.y) * 0.1
            # self.zoom += (zoom - self.zoom) * 0.05

            max_camera_x = world_centerx - window_centerx
            min_camera_x = window_centerx - world_centerx
            self.x = max(min_camera_x, min(self.x, max_camera_x))

def screenCheck(player, camera):
    screenLeft = world_centerx - window_centerx + camera.x
    screenRight = world_centerx - window_centerx + camera.x + window_width
    playerLeft = player.getPosition('left')
    playerRight = player.getPosition('right')
    if playerLeft < screenLeft:
        player.setPosition('left',screenLeft)
    elif playerRight > screenRight:
        player.setPosition('right',screenRight)

bt_player1_up = text_button.TextButton("↑",250,545,50,50)
bt_player1_down = text_button.TextButton("↓",250,605,50,50)
bt_player1_left = text_button.TextButton("←",190,605,50,50)
bt_player1_right = text_button.TextButton("→",310,605,50,50)
bt_player2_up = text_button.TextButton("↑",950,545,50,50,text_color=(0, 0, 0), 
                 bg_color=(0, 0, 255),
                 hover_color=(100, 100, 255),
                 click_text_color=(200,200,200),
                 click_bg_color=(0,0,100))
bt_player2_down = text_button.TextButton("↓",950,605,50,50,text_color=(0, 0, 0), 
                 bg_color=(0, 0, 255),
                 hover_color=(100, 100, 255),
                 click_text_color=(200,200,200),
                 click_bg_color=(0,0,100))
bt_player2_left = text_button.TextButton("←",890,605,50,50,text_color=(0, 0, 0), 
                 bg_color=(0, 0, 255),
                 hover_color=(100, 100, 255),
                 click_text_color=(200,200,200),
                 click_bg_color=(0,0,100))
bt_player2_right = text_button.TextButton("→",1010,605,50,50,text_color=(0, 0, 0), 
                 bg_color=(0, 0, 255),
                 hover_color=(100, 100, 255),
                 click_text_color=(200,200,200),
                 click_bg_color=(0,0,100))
BG1 = Background('./img/bg/cloud.png')
BG2 = Background('./img/bg/mountain_far.png')
BG3 = Background('./img/bg/mountain_near.png')
BG4 = Background('./img/bg/road.png')
BG5 = Background('./img/bg/tree.png',width=3840)
BG6 = Background('./img/bg/bush.png',width=8000)
UI = gameUI.UI()

player1 = player.Player()
player1.init(world_centerx - window_centerx, world_centery)

player2 = playerbigger.Player()
player2.init(world_centerx + window_centerx, world_centery, False)

camera = Camera()

while window_open:
    delta_time = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False
        # player1.event_handle(event)
        player1_up = bt_player1_up.event_handle(event)
        player1_donw = bt_player1_down.event_handle(event)
        player1_left = bt_player1_left.event_handle(event)
        player1_right = bt_player1_right.event_handle(event)

        if player1_up == 'pressed':
            if not player1.isJumping:
                player1.isJumping = True
                player1.isMoving = True
                bottomLeft = player1.image_rect.bottomleft
                player1.getImages('jumping')
                player1.image_rect.bottomleft = bottomLeft

        if player1_left == 'pressed':
            if not player1.isJumping:
                if player1.facingRight:
                    player1.facingRight = False
                player1.isMoving = True
                if not player1.action == 'running':
                    bottomLeft = player1.image_rect.bottomleft
                    player1.getImages('running')
                    player1.image_rect.bottomleft = bottomLeft

        if player1_right == 'pressed':
            if not player1.isJumping:
                if not player1.facingRight:
                    player1.facingRight = True
                player1.isMoving = True
                if not player1.action == 'running':
                    bottomLeft = player1.image_rect.bottomleft
                    player1.getImages('running')
                    player1.image_rect.bottomleft = bottomLeft
        
        if player1_left == 'released':
            if not player1.isJumping:
                player1.isMoving = False
        
        if player1_right == 'released':
            if not player1.isJumping:
                player1.isMoving = False       

        player2_up = bt_player2_up.event_handle(event)
        player2_donw = bt_player2_down.event_handle(event)
        player2_left = bt_player2_left.event_handle(event)
        player2_right = bt_player2_right.event_handle(event)

        if player2_up == 'pressed':
            if not player2.isJumping:
                player2.isJumping = True
                player2.isMoving = True
                bottomLeft = player2.image_rect.bottomleft
                player2.getImages('jumping')
                player2.image_rect.bottomleft = bottomLeft

        if player2_left == 'pressed':
            if not player2.isJumping:
                if player2.facingRight:
                    player2.facingRight = False
                player2.isMoving = True
                if not player2.action == 'running':
                    bottomLeft = player2.image_rect.bottomleft
                    player2.getImages('running')
                    player2.image_rect.bottomleft = bottomLeft

        if player2_right == 'pressed':
            if not player2.isJumping:
                if not player2.facingRight:
                    player2.facingRight = True
                player2.isMoving = True
                if not player2.action == 'running':
                    bottomLeft = player2.image_rect.bottomleft
                    player2.getImages('running')
                    player2.image_rect.bottomleft = bottomLeft
        
        if player2_left == 'released':
            if not player2.isJumping:
                player2.isMoving = False
        
        if player2_right == 'released':
            if not player2.isJumping:
                player2.isMoving = False  

    if player1.isMoving:
        player1.update(player2)
        screenCheck(player1,camera)

    if player2.isMoving:
        player2.update(player1)
        screenCheck(player2,camera)
    camera.update(player1,player2)

    bt_player1_up.update()
    bt_player1_down.update()
    bt_player1_left.update()
    bt_player1_right.update()
    bt_player2_up.update()
    bt_player2_down.update()
    bt_player2_left.update()
    bt_player2_right.update()

    update_rects = []
    bg_rect1 = BG1.draw(game_window,0.1)
    bg_rect2 = BG2.draw(game_window,0.3)
    bg_rect3 = BG3.draw(game_window,0.4)
    bg_rect4 = BG4.draw(game_window,1)
    player1_rect = player1.draw(game_window,camera.x,camera.y)
    player2_rect = player2.draw(game_window,camera.x,camera.y)
    bg_rect5 = BG5.draw(game_window,2)
    bg_rect6 = BG6.draw(game_window,5)
    ui_rect = UI.draw(game_window)
    
    bt_pl1_u_rect = bt_player1_up.draw(game_window)
    bt_pl1_d_rect = bt_player1_down.draw(game_window)
    bt_pl1_l_rect = bt_player1_left.draw(game_window)
    bt_pl1_r_rect = bt_player1_right.draw(game_window)
    bt_pl2_u_rect = bt_player2_up.draw(game_window)
    bt_pl2_d_rect = bt_player2_down.draw(game_window)
    bt_pl2_l_rect = bt_player2_left.draw(game_window)
    bt_pl2_r_rect = bt_player2_right.draw(game_window)
    
    update_rects.append(bg_rect1)
    update_rects.append(bg_rect2)
    update_rects.append(bg_rect3)
    update_rects.append(bg_rect4)
    update_rects.append(player1_rect)
    update_rects.append(player2_rect)
    update_rects.append(bg_rect5)
    update_rects.append(bg_rect6)
    update_rects.append(ui_rect)

    update_rects.append(bt_pl1_u_rect)
    update_rects.append(bt_pl1_d_rect)
    update_rects.append(bt_pl1_l_rect)
    update_rects.append(bt_pl1_r_rect)
    update_rects.append(bt_pl2_u_rect)
    update_rects.append(bt_pl2_d_rect)
    update_rects.append(bt_pl2_l_rect)
    update_rects.append(bt_pl2_r_rect)

    pygame.display.update(update_rects)
pygame.quit() 