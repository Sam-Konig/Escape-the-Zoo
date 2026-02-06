import pygame

class TextButton:
    def __init__(self, text, x, y, width, height,
                 text_color=(0, 0, 0), 
                 bg_color=(255, 0, 0),
                 hover_color=(255, 100, 100),
                 click_text_color=(200,200,200),
                 click_bg_color=(100,0,0)):
               
        try:
            self.font = pygame.font.SysFont(["KaiTi","SimHei", "Arial"], 36)
        except:
            self.font = pygame.font.Font(None, 36)

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
        self.button_held = False
        self.click_count = 0
        self.click_pause = 3

        self.update_text()

    def update_text(self, color=None):
        text_color = color or self.default_text_color
        self.text_surface = self.font.render(self.text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)

    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.is_clicked = True
                self.button_held = True
                self.button_rect.x += 4
                self.button_rect.y += 4
                self.update_text(self.click_text_color)  # 更新文字颜色
                return 'pressed'  # 返回按下状态
        if event.type == pygame.MOUSEBUTTONUP:
            if self.is_clicked:
                self.button_held = False
                return 'released'  # 返回释放状态
            self.button_held = False
        return 'none'
    
    def update(self):
        if self.is_clicked and not self.button_held:
            self.click_count += 1
            if self.click_count >= self.click_pause:
                self.is_clicked = False
                self.click_count = 0
                self.button_rect.x -= 4
                self.button_rect.y -= 4
                self.update_text()

        self.is_hovered = self.button_rect.collidepoint(pygame.mouse.get_pos())

    # def is_hovered(self, mouse_pos):
    #     return self.button_rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        # color = self.hover_color if (mouse_pos and self.is_hovered(mouse_pos)) else self.bg_color
        if self.is_clicked:
            color = self.click_bg_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.default_bg_color

        pygame.draw.rect(surface, color, self.button_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.button_rect, 2) 
        
        surface.blit(self.text_surface, self.text_rect)