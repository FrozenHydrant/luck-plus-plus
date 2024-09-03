import pygame
from animations import *
import collections

class Main:
    FPS = None
    X = None
    Y = None
    
    def __init__(self, screen):
        self.running = True
        self.screen = screen
        self.animations = Animations((Main.FPS, Main.X, Main.Y), self.screen)
        self.events = collections.deque()
        self.event_time = 0
        self.clock = pygame.time.Clock()
        self.bound = min(Main.X, Main.Y)
        self.background = (0, 0, 0)

        #self.animations.enqueue(GenericAnimation(AnimationInfo().set_health(Main.FPS*5).position(Main.FPS, (800, 300)).position(Main.FPS*2, (0, 200)).position(Main.FPS*5, (600, 800)).image(Main.FPS*0.5, self.animations.LOADING_AAA_TEXTURE)))
        
    def execute_function(self, **kwargs):
        for k, v in kwargs.items():
            if k == "function":
                v(**kwargs)
                return

    def change_background(self, **kwargs):
        self.background = kwargs['c']

    def begin_main_loop(self):
        self.animations.enqueue(GenericAnimation(AnimationInfo().set_health(Main.FPS*2.5).position(0, (Main.X/2-self.animations.LOADING_AAA_TEXTURE.get_rect()[2]/2, Main.Y)).position(Main.FPS*2/3, (Main.X/2-self.animations.LOADING_AAA_TEXTURE.get_rect()[2]/2, Main.Y/2-self.animations.LOADING_AAA_TEXTURE.get_rect()[3]/2)).position(Main.FPS*2.2, (Main.X/2-self.animations.LOADING_AAA_TEXTURE.get_rect()[2]/2, Main.Y/2-self.animations.LOADING_AAA_TEXTURE.get_rect()[3]/2)).position(Main.FPS*2.5, (Main.X/2, Main.Y/2)).scale(Main.FPS*2, (1, 1)).scale(Main.FPS*2.2, (1.1, 1.1)).scale(Main.FPS*2.5, (0, 0)).image(0, self.animations.LOADING_AAA_TEXTURE)))
        self.animations.enqueue(GenericAnimation(AnimationInfo().set_health(Main.FPS*2.5).position(0, (Main.X/2-self.animations.DOT_TEXTURE.get_rect()[2]/2, Main.Y)).position(Main.FPS*2/3, (Main.X/2-self.animations.DOT_TEXTURE.get_rect()[2]/2, 7*Main.Y/10-self.animations.DOT_TEXTURE.get_rect()[3]/2)).position(Main.FPS, (Main.X/2-self.animations.DOT_TEXTURE.get_rect()[2]/2, 7*Main.Y/10-self.animations.DOT_TEXTURE.get_rect()[3]/2)).position(Main.FPS*2, (Main.X/2-self.animations.DOT_TEXTURE.get_rect()[2]*10, 7*Main.Y/10-self.animations.DOT_TEXTURE.get_rect()[3]/2)).position(Main.FPS*2.2, (Main.X/2-self.animations.DOT_TEXTURE.get_rect()[2]*10, 7*Main.Y/10-self.animations.DOT_TEXTURE.get_rect()[3]/2)).scale(Main.FPS, (1, 1)).position(Main.FPS*2.5, (Main.X/2, Main.Y/2)).scale(Main.FPS*2, (20,1)).scale(Main.FPS*2.2, (20.1, 1.1)).scale(Main.FPS*2.5, (0, 0)).image(0, self.animations.DOT_TEXTURE)))
        self.animations.enqueue(GenericAnimation(AnimationInfo().set_health(Main.FPS*3.75).position(0, (-999, -999)).position(Main.FPS*2.75-1, (-999, -999)).position(Main.FPS*2.75, (Main.X/2-self.animations.DOT_LARGE_TEXTURE.get_rect()[2]/2*0.1, Main.Y/2-self.animations.DOT_LARGE_TEXTURE.get_rect()[3]/2*0.1)).position(Main.FPS*3.75, (Main.X/2-self.animations.DOT_LARGE_TEXTURE.get_rect()[2]/2*3, Main.Y/2-self.animations.DOT_LARGE_TEXTURE.get_rect()[3]/2*3)).scale(0, (0.1, 0.1)).scale(Main.FPS*2.75-1, (0.1, 0.1)).scale(Main.FPS*3.75, (3, 3)).image(0, self.animations.DOT_LARGE_TEXTURE)))
        self.events.append({'time': Main.FPS*3.75, 'function': self.change_background, 'c': (255, 255, 255)})
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.event_time += 1
            if len(self.events) > 0 and self.event_time > self.events[0]['time']:
                event = self.events.popleft()
                self.execute_function(**event)
                self.event_time = 0

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(self.background)

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
