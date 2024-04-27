import math
import pygame
from animations import *

class Main:
    FPS = None
    X = None
    Y = None
    
    def __init__(self, screen):
        self.running = True
        self.screen = screen
        self.animations = Animations((Main.FPS, Main.X, Main.Y), self.screen)
        self.clock = pygame.time.Clock()

        #self.animations.enqueue(GenericAnimation(AnimationInfo().set_health(Main.FPS*5).position(Main.FPS, (800, 300)).position(Main.FPS*2, (0, 200)).position(Main.FPS*5, (600, 800)).image(Main.FPS*0.5, self.animations.LOADING_AAA_TEXTURE)))
        
           
    def begin_main_loop(self):
        self.animations.enqueue(GenericAnimation(AnimationInfo().set_health(Main.FPS).position(0, (Main.X/2-self.animations.LOADING_AAA_TEXTURE.get_rect()[2]/2, Main.Y)).position(Main.FPS, (Main.X/2-self.animations.LOADING_AAA_TEXTURE.get_rect()[2]/2, Main.Y/2-self.animations.LOADING_AAA_TEXTURE.get_rect()[3]/2)).image(0, self.animations.LOADING_AAA_TEXTURE)))
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            # RENDER YOUR GAME HERE
            self.animations.tick()
            
            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(Main.FPS)  # limits FPS
            #print(self.clock.get_fps())
        pygame.quit()

def main():
    # pygame setup
    pygame.init()
    MAIN_SCREEN = pygame.display.set_mode()
    Main.FPS = 60
    Main.X, Main.Y = MAIN_SCREEN.get_size()

    main_instance = Main(MAIN_SCREEN)
    main_instance.begin_main_loop()

if __name__ == "__main__":
    main()
