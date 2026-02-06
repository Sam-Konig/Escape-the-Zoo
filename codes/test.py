import pygame
import sys

# 初始化Pygame
pygame.init()

# 你的核心配置（屏幕1000，背景2000）
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600  # 屏幕尺寸（可视区域）
BG_WIDTH, BG_HEIGHT = 2000, 1200         # 背景尺寸
CAM_SMOOTH = 0.15                        # 镜头缓动系数（0.1~0.2丝滑，1=硬跟随）

# 创建屏幕窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("双角色镜头跟随")
clock = pygame.time.Clock()
FPS = 60

# 定义角色类（简化，包含位置、移动、绘制）
class Player:
    def __init__(self, x, y, color):
        self.x = x  # 实际世界坐标（不是屏幕坐标）
        self.y = y
        self.size = 30
        self.color = color
        self.speed = 5

    def move(self, keys, is_player1):
        # 角色1：WASD移动，角色2：方向键移动
        if is_player1:
            if keys[pygame.K_w]: self.y -= self.speed
            if keys[pygame.K_s]: self.y += self.speed
            if keys[pygame.K_a]: self.x -= self.speed
            if keys[pygame.K_d]: self.x += self.speed
        else:
            if keys[pygame.K_UP]: self.y -= self.speed
            if keys[pygame.K_DOWN]: self.y += self.speed
            if keys[pygame.K_LEFT]: self.x -= self.speed
            if keys[pygame.K_RIGHT]: self.x += self.speed

        # 角色限制在背景内（可选，避免角色走出背景）
        self.x = max(self.size//2, min(self.x, BG_WIDTH - self.size//2))
        self.y = max(self.size//2, min(self.y, BG_HEIGHT - self.size//2))

    def draw(self, cam_x, cam_y):
        # 绘制坐标 = 实际坐标 - 镜头左上角坐标（核心偏移）
        draw_x = self.x - cam_x
        draw_y = self.y - cam_y
        pygame.draw.circle(screen, self.color, (draw_x, draw_y), self.size)

# 创建两个角色（初始位置分开，方便测试跟随）
player1 = Player(300, 300, (255, 0, 0))  # 红色：WASD
player2 = Player(700, 700, (0, 255, 0))  # 绿色：方向键

# 镜头初始坐标（居中）
cam_x, cam_y = (BG_WIDTH - SCREEN_WIDTH) // 2, (BG_HEIGHT - SCREEN_HEIGHT) // 2

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 1. 获取按键，移动两个角色
    keys = pygame.key.get_pressed()
    player1.move(keys, is_player1=True)
    player2.move(keys, is_player1=False)

    # 2. 计算双角色锚点（镜头中心）
    anchor_x = (player1.x + player2.x) / 2
    anchor_y = (player1.y + player2.y) / 2

    # 3. 计算镜头原始坐标（无边界、无缓动）
    cam_x_raw = anchor_x - SCREEN_WIDTH / 2
    cam_y_raw = anchor_y - SCREEN_HEIGHT / 2

    # 4. 镜头缓动（可选，注释则为硬跟随）
    cam_x += (cam_x_raw - cam_x) * CAM_SMOOTH
    cam_y += (cam_y_raw - cam_y) * CAM_SMOOTH

    # 5. 镜头边界限制（核心！避免滑出背景，转整数避免模糊）
    cam_x = max(0, min(int(cam_x), BG_WIDTH - SCREEN_WIDTH))
    cam_y = max(0, min(int(cam_y), BG_HEIGHT - SCREEN_HEIGHT))

    # 6. 绘制内容（先绘背景，再绘角色，都要做镜头偏移）
    screen.fill((0, 0, 0))  # 黑底（背景外的区域）
    # 绘制背景（大矩形，模拟2000×1200的背景，浅蓝色）
    bg_draw_x = 0 - cam_x
    bg_draw_y = 0 - cam_y
    pygame.draw.rect(screen, (135, 206, 235), (bg_draw_x, bg_draw_y, BG_WIDTH, BG_HEIGHT))
    # 绘制两个角色（传入镜头坐标做偏移）
    player1.draw(cam_x, cam_y)
    player2.draw(cam_x, cam_y)

    # 7. 更新屏幕
    pygame.display.flip()
    clock.tick(FPS)