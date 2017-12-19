import sys
import pygame
from time import sleep

class Frame:

    BLACK = 0,0,0
    WHITE = 255, 255, 255
    BLUE = 0,0,255
    RED = 255,0,0
    GREEN = 0,255,0

    def __init__(self):
        pygame.init()
        self.size = width, height = 540, 480
        self.screen = pygame.display.set_mode(self.size)
        self.toggle = True
        self.rectangles = [[None for i in range(8)] for n in range(9)]


    def button(self, x,y,w,h,ic,ac):
        mouse = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y and mouseDown[0] == 1 and self.toggle == True:
            self.toggle = False
            sleep(0.1)

        elif x+w > mouse[0] > x and y+h > mouse[1] > y and mouseDown[0] == 1 and self.toggle == False:
            self.toggle = True
            sleep(0.1)

        if self.toggle == True:
            return pygame.draw.rect(self.screen, ic,(x,y,w,h))
            

        elif self.toggle == False:
            return pygame.draw.rect(self.screen, ac,(x,y,w,h))
            

    def mainLoop(self):
        
        buttons = [[True for i in range(8)] for n in range(9)]
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            self.screen.fill(Frame.WHITE)
            for i in range(9):
                for n in range(8):
                    buttons[i][n] = [i * 60, n * 60]
                    if i == 8:
                        color = Frame.BLUE
                        
                    else:
                        color = Frame.BLACK

                   
                    pygame.draw.rect(self.screen, color, (i * 60, n * 60, 58, 58))
                    self.rectangles[i][n] = self.button(i*60,n*60, 58, 58, Frame.BLACK, Frame.GREEN)
                    
            mouse = pygame.mouse.get_pressed()
            pygame.display.flip()

frame = Frame()
frame.mainLoop()