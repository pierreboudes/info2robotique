# -*- coding: utf-8 -*-
from TurtleTelemeter import *

######### main ########


def fst(x):
    return x[0]

def tourhorizon(T, boxlist, angle, etapes):    
    T.pendown()
    res = []
    for i in range(etapes):        
        d = telemetry(T,boxlist)
        
        res.append((T.heading() % 360, d))
        T.fd(d)
        T.bk(d)
        T.left(angle)
    T.penup()
    return sorted(res, key = fst)

def main():
    T = turtle.Turtle()
    T.clearscreen()
    T.penup()
    T.autoupdate(False)
    boxlist = [ new_box(0,0,590) ]
    boxlist += [ new_box(150*cos(1+i*2*pi/15),150*sin(1+i*2*pi/15),random.randint(10,40)) for i in range(12)]
#    boxlist = [ new_box(0,0,590) ]
    boxlist += [ new_box(random.randint(-500,500), random.randint(30,500),random.randint(10,40)) for i in range(12)]
    boxlist += [ new_box(random.randint(-500,-30), random.randint(-500,500),random.randint(10,40)) for i in range(12)]
    res = tourhorizon(T, boxlist, 7, 200)
    print res
    raw_input()
        
main()

