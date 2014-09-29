# -*- coding: utf-8 -*-
"""
Telemetry
"""

from sympy.geometry import Polygon,Line,Point,intersection
from sympy import N
import pgturtle as turtle
import random
from math import *
import numpy as np

def new_box(x,y,c):
    V = turtle.Turtle()
    V.hideturtle(); V.penup()
    V.setpos(x-c/2,y-c/2); V.setheading(0) ; V.pendown()
    for i in range(4):
        V.fd(c)
        V.left(90)
    return Polygon(Point(x-c/2,-y-c/2),Point(x-c/2,-y+c/2),Point(x+c/2,-y+c/2),Point(x+c/2,-y-c/2))

def telemetry(T,boxelist):
    a = radians(T.heading())
    P1,P2 = Point(T.xcor(),T.ycor()) , Point(T.xcor()+cos(a),T.ycor()+sin(a))
    P12 = P2 - P1
    intr = [N(P12.dot(p-P1)) for r in boxelist for p in intersection(Line(P1,P2),r) ]
    intr = [d for d in intr if d >= 0]
    #print intr
    return None if intr==[] else (min(intr)+np.random.normal(0,10))

if __name__ == '__main__':

        ######### main ########
        turtle.clearscreen()
        T = turtle.Turtle()
        T.penup()
        
        boxelist = [ new_box(0,0,400) ]
        boxelist += [ new_box(150*cos(1+i*2*pi/15),150*sin(1+i*2*pi/15),random.randint(10,40)) for i in range(12)]
        
        print telemetry(T,boxelist)
        raw_input()

