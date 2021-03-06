# coding: utf-8

import pygame, types, threading, traceback


class Game:
    def __init__(self):
        self.size = (500,500)
        self.running = True
        self.scene = list()
        self.flipdelay=16
        self.tickcounter=0
        
    def render(self):
        self.disp.fill((0,0,0))
        for obj in self.scene:
            try:
                obj.render(self.disp)
            except Exception:
                traceback.print_exc()
                self.scene.remove(obj)
                print("Exception during render: Object "+str(obj)+" removed from the scene")
        pygame.display.flip()

    def update(self):
            dt=pygame.time.get_ticks()- self.tickcounter
            for obj in self.scene:
                try:
                    obj.update(dt)
                except Exception:
                    traceback.print_exc()
                    self.scene.remove(obj)
                    print("Exception during update: Object "+str(obj)+" removed from the scene")
            self.tickcounter=pygame.time.get_ticks()
            pygame.time.delay(self.flipdelay)

    def process_events(self):
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_LEFT:
                    self.player.current_anim = "left"
                elif evt.key == pygame.K_RIGHT:
                    self.player.current_anim = "right"
                if evt.key == pygame.K_UP:
                    self.player.current_anim = "up"
                if evt.key == pygame.K_DOWN:
                    self.player.current_anim = "down"
                if evt.key == pygame.K_ESCAPE or  evt.key == pygame.K_q:
                    self.running = False
            if evt.type == pygame.QUIT:
                self.running = False

    def mainloop(self):
        pygame.init()
        self.disp=pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.tickcounter=pygame.time.get_ticks()
        while( self.running ):
            try:
                self.render()
                self.process_events()
                self.update()
            except Exception:
                traceback.print_exc()
                pygame.time.delay(10000)
        pygame.quit()



class Map:
    def __init__(self):
        # We will need to load some images and make a better Tile class later
        # but now I just want to test the speed of the blit operation
        self.tile = pygame.image.load('art/castle/grass.png')
        self.avg_time=0.0
        
    def update(self, dt):
        return
    
    def render(self, disp):
        ta = pygame.time.get_ticks()
        for y in range(0,500,32):
            for x in range(0,500,32):
                disp.blit(self.tile, (x,y))
        self.avg_time = 0.9*self.avg_time + 0.1*float(pygame.time.get_ticks()-ta)
        #print(pygame.time.get_ticks()-ta)
        

class Character:
    def __init__(self, x, y):    
        self.img=pygame.image.load("art/LPC/walk.png")
        # Each animation is stored in the anim dict as a list with the following 
        # format: (tick_per_frame, frame1, frame2, ...)
        
        self.anim = dict()
        self.cycle_index = 0
        self.cycle_tick = 0
        seq = list()
        seq.append(80) # ticks per frame
        for i in range(8):
            seq.append(self.img.subsurface((64+i*64,0,64,64)))
        self.anim["up"] = seq
        
        seq = list()
        seq.append(80) # ticks per frame
        for i in range(8):
            seq.append(self.img.subsurface((64+i*64,128,64,64)))
        self.anim["down"] = seq

        seq = list()
        seq.append(80) # ticks per frame
        for i in range(8):
            seq.append(self.img.subsurface((64+i*64,64,64,64)))
        self.anim["left"] = seq

        seq = list()
        seq.append(80) # ticks per frame
        for i in range(8):
            seq.append(self.img.subsurface((64+i*64,192,64,64)))
        self.anim["right"] = seq

        self.current_anim = "up"
        self.current_frames = self.anim[self.current_anim]
        self.pos = [x,y]

    def update(self, dt):
        dirs = {"up": (0, -0.5), "down": (0, 0.5), "right": (1, 0), "left": (-1, 0)}
        ca = self.anim[self.current_anim]
        dxdy = dirs[self.current_anim]
        self.cycle_tick = (self.cycle_tick + dt) % ((len(ca) - 1) * ca[0])
        self.cycle_index = int(self.cycle_tick / ca[0])
        self.pos[0] += dxdy[0]
        self.pos[1] += dxdy[1]

    def render(self, display):
        ca = self.anim[self.current_anim]
        display.blit(ca[1+self.cycle_index], (self.pos))


game = Game()
game.scene.append(Map())
game.player = Character(100,100)
game.scene.append(game.player)
game.mainloop()

