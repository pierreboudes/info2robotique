import turtle
import random
import math
#parametres
N = 20 # nb de boids
dmin = 30 # rayon de la zone de repulsion
alpha = 0.3
beta = 0.5
gamma = 1.
epsilon = 0.05 #0.5
tau = 90
vitesse = 2 
rayon_terrain = 150

boid = [turtle.Turtle() for i in range(N)]
boid[0].tracer(40, 1)


#initialisation des parametres (aleatoirement)
for i in range(N):
    boid[i].penup()
    boid[i].setposition(random.randint(-100, 100), random.randint(-100, 100))
    boid[i].setheading(random.randint(0,359))
    boid[i].color(random.random(),random.random(),random.random())
#   boid[i].pendown()
#moyenne des positions
def position_moyenne(t):
    n = len(t)
    sx, sy = 0, 0
    for b in t:
        x, y = b.position()
        sx += x
        sy += y
    return sx / n, sy / n

#angle moyen en degres
def angle_moyen():
    a = 0
    for i in range(N):
        a += boid[i].heading()
    return a / N

def heading2speed(angle):
    return math.cos(angle/57.17) * vitesse, math.sin(angle/57.17) * vitesse

def speed2heading(vx, vy):
    return math.atan2(vy, vx) * 57.17

def vitesse_moyenne() :
    return heading2speed(angle_moyen())
        
def voisins(i):
    bb = boid[i] 
    return [b for b in boid if b is not bb and bb.distance(b) < dmin]

while (True):
    px, py = position_moyenne(boid)
    r2x, r2y = vitesse_moyenne()
    for i in range(N):
        x, y = boid[i].position()
        r1x, r1y = px - x, py -y
        r3x, r3y = 0, 0
        entourage = voisins(i)
        if (len(entourage) > 0) :
            ex, ey = position_moyenne(entourage)
            d = boid[i].distance(ex, ey)
            if (d > 1.) :
                r3x = (x - ex) / d
                r3y = (y - ey) / d
            else :
                print("pseudocollision")
                r3x = random.randint(-vitesse, vitesse)
                r3y = random.randint(-vitesse, vitesse)

        if (boid[i].distance(0,0) > rayon_terrain) :
            r4x, r4y = -x, -y
        else :
            r4x, r4y = 0, 0
        r5x, r5y = heading2speed(boid[i].heading())
        rx = alpha * r1x + beta * r2x + gamma * r3x + epsilon * r4x + tau * r5x
        ry = alpha * r1y + beta * r2y + gamma * r3y + epsilon * r4y + tau * r5y
        boid[i].setheading(speed2heading(rx, ry))
        boid[i].forward(vitesse)
            

raw_input()
