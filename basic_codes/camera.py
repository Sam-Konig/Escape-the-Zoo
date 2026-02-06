import sys
# 如果用sys.path.append('..')，检索目录放最后，用insert则先检索上一级目录
sys.path.insert(0, '..')
from basic_codes import settings as st

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dead_zone = 100 # 单边范围，总静止区宽度为2*dead_zone
        self.target_ideal_x = st.window_centerx
        
    def update(self,player_x,player_y):
        target_screen_x = player_x - (st.world_centerx - st.window_centerx) - self.x
        offset = target_screen_x - self.target_ideal_x

        if offset > self.dead_zone:
            # 目标超出右边界，相机向右移动
            camera_target_x = player_x - (st.world_centerx - st.window_centerx) - (self.target_ideal_x + self.dead_zone)
        elif offset < -self.dead_zone:
            # 目标超出左边界，相机向左移动
            camera_target_x = player_x - (st.world_centerx - st.window_centerx) - (self.target_ideal_x - self.dead_zone)
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