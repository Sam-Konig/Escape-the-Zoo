import pygame
import sys
sys.path.insert(0, '.')
from basic_codes import settings as st

pygame.font.init()

font = pygame.font.Font('./font/SourceHanSansTC-Bold.otf',24)
player1_text = font.render("player 1", True, (0,0,0))
player1_text_rect = player1_text.get_rect(center=(100, 600))
player2_text = font.render("player 2", True, (0,0,0))
player2_text_rect = player2_text.get_rect(center=(800, 600))

class UI:
    def __init__(self):
        self.surface = pygame.Surface((st.window_width,st.window_height),pygame.SRCALPHA)
        self.surface.blit(player1_text,player1_text_rect)
        self.surface.blit(player2_text,player2_text_rect)

    def draw(self,screen):
        screen.blit(self.surface,(0,0))
