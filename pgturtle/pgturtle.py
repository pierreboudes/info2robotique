# myturtle.py - based on Tomasz Kwiatkowski's myturtle.py
 
import pygame
import time
import math
from weakref import WeakSet

class Turtle: 
    """
    This class, based on the code of Tomasz Kwiatkowski, is a pygame implementation of the standard turtle python package.
    It is meant to be compatible with the turtle package, but not all functions are implemented already.
    Added function not available in initial turtle package: exit,quit, and autoupdate_off,autoupdate_on
    Yann Chevaleyre
    """
    _surf   = None
    _center = None
    _screen = None
    _autoupdate = True

    _all_turtles = WeakSet()

    ###### INIT ######
    def __init__(self,xsize=800,ysize=600):
        Turtle._all_turtles.add(self)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self._pos = (0, 0)
        self._ang = 0
        self._pen = True
        self._changed = True
        self._color = (0, 0, 0)
        self._turtle_visible = True
        self._tsize = 10 # size of the turtle
        self._boundingbox = None  #will then be of type pygame.Rect((0,0,0,0)) 

        if Turtle._surf == None:
             pygame.init() 
             Turtle._surf = pygame.Surface((xsize, ysize), depth=24)
             Turtle._screen = pygame.display.set_mode((xsize, ysize))
             Turtle._center = (Turtle._surf.get_width() // 2, Turtle._surf.get_height() // 2)
             Turtle.clearscreen()

    ###### PEN #######
    def pendown(self):
        self._pen = True
    
    def penup(self):
        self._pen = False

    def hideturtle(self):
	self._turtle_visible = False 

    def showturtle(self):
	self._turtle_visible = True 

    ######## MOVE #######
    def setposition(self,x,y=None):
        old_pos, self._pos = self._pos , (x if y == None else (x,y))

        if self._pen:
            _a,_b = Turtle._convert_pos(old_pos) , Turtle._convert_pos(self._pos)
            pygame.draw.aaline(Turtle._surf, self._color, _a,_b)
            pygame.draw.aaline(Turtle._screen, self._color, _a,_b)
            self._changed = True

        self.update()


    def _fwdbackutil(self,v):
        vr = Turtle._rot(v, Turtle._convert_angle(self._ang))
        self.setposition(Turtle._vsum(self._pos, vr) )
 
    def forward(self,n):
         self._fwdbackutil((n, 0))
 
    def backward(self,n):
        self._fwdbackutil((-n, 0))
     
    def right(self,a):
        self._ang += a
        while self._ang > 360.0:
            self._ang -= 360.0
        self.update()

    def left(self,a):
        self._ang -= a
        while self._ang < 0.0:
            self._ang += 360.0
        self.update()
     
    def setx(self,x):
        self.setposition(x,self._pos[1])
        
    def sety(self,y):
        self.setposition(self._pos[0],y)
        
    def jump_to_pos(self,x,y=None):
        self._pen , oldpen = False , self._pen
        self.setposition(x,y)
        self._pen = old_pen
     
    def setheading(self,a):
        self._ang = a
     
     
    ###### STATE #######
    def position(self):
        return self._pos
     
    def xcor(self):
        return self._pos[0]

    def ycor(self):
        return self._pos[1]

    def heading(self):
        return self._ang
    
    @staticmethod
    def clearscreen():
        Turtle._surf.fill((255, 255, 255))
        Turtle._screen.fill((255, 255, 255))

    def autoupdate(self,on_or_off=True):
        Turtle._autoupdate = on_or_off
        self.update()

    def update(self,forceupdate=False):
        if Turtle._autoupdate or forceupdate:
	    if self._boundingbox == None:
		self._boudingbox = Turtle._surf.get_rect()
            Turtle._screen.blit(Turtle._surf,(0,0))
            #Turtle._screen.blit(Turtle._surf,self._boundingbox,self._boundingbox)
            for t in Turtle._all_turtles:
                if t._turtle_visible:
                    t._drawturtle()
            pygame.display.flip()
            self._boundingbox = pygame.Rect((0,0,0,0))
        Turtle._handle_exceptions()

    @staticmethod
    def exit():
        pygame.quit()

    ###### INTERNALS ######

    def _update_boundingbox(self,x,y):
        b = pygame.Rect((x,y,1,1))
        if self._boundingbox == None:
            self._boundingbox = b
        else:
            self._boundingbox.union_ip( b )
        self._boundingbox = self._boundingbox.clip( Turtle._surf.get_rect() )

    def _drawturtle(self):
        (x,y) = self._pos
        sa = math.sin(Turtle._convert_angle(self._ang))
        ca = math.cos(Turtle._convert_angle(self._ang))
 
         #ci dessous, rajouter convert pos!!!
        x2,y2 = x - self._tsize * ca , y - self._tsize * sa
        dx,dy = (self._tsize/2)*(-sa) , (self._tsize/2)*ca
        pygame.draw.polygon(Turtle._screen, (0,0,255), (Turtle._convert_pos((x,y)) , Turtle._convert_pos((x2-dx,y2-dy)) , Turtle._convert_pos((x2+dx,y2+dy)) , Turtle._convert_pos((x,y)) ))
 
    @staticmethod
    def _handle_exceptions():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: raise KeyboardInterrupt

    @staticmethod
    def _convert_angle(deg):
        return (- deg) / 360.0 * 2 * math.pi
    
    @staticmethod 
    def _convert_pos(pos):
        print "---",pos,"  ,  ",Turtle._center
        return (pos[0] + Turtle._center[0], Turtle._center[1] - pos[1])
    
    @staticmethod 
    def _rot(v, a):
        sa = math.sin(a)
        ca = math.cos(a)
        return (v[0] * ca - v[1] * sa, v[0] * sa + v[1] * ca)
    
    @staticmethod
    def _vsum(x, y):
        return (x[0] + y[0], x[1] + y[1])

    fd=forward
    bk=backward
    back=backward
    rt=right
    lt=left
    pd=pendown
    down=pendown
    pu=penup
    up=penup
    pos=position
    setpos=setposition
    goto=setposition
    seth=setheading
    quit=exit

 
if __name__ == "__main__":
    print("usage: import myturtle")
 
 
# turtledemo.py
 
import pygame
import os
import time
import math
import random

#from  myturtle import *

def tree(t,r):
    if r < 5:
        t.fd(r)
        t.bk(r)
    else:
        t.fd(r / 3)
        t.lt(30)
        tree(t,r * 2 / 3)
        t.rt(30)
        t.bk(r / 3)
 
        t.fd(r / 2)
        t.rt(25)
        tree(t,r / 2)
        t.lt(25)
        t.bk(r / 2)
         
        t.fd(r * 5 / 6)
        t.rt(25)
        tree(t,r / 2)
        t.lt(25)
        t.bk(r * 5 / 6)
 
if __name__== '__main__':
    try:
    	slip=lambda: time.sleep(0.1)
    
    	t1 = Turtle()
    	t2 = Turtle()
    	#tree(t,400)
    	while True:    
            slip()
            t2.setposition(random.randint(-100,100),random.randint(-100,100))
            t1.fd(10)
       	    t1.left(3)

    finally:
        Turtle.quit()
