import math
import pygame as pg


threshold = 10

class Particle:
    def __init__(self,clr:str="red",pos:tuple=(400,200),rad:int = 10):
        """
        Makes individual particles or nodes in case of rope.        
        """
        self.rad = rad
        self.clr = clr
        self.pos =pg.math.Vector2(pos[0],pos[1])
        self.accel = pg.math.Vector2(0,0)
        self.vel = pg.math.Vector2(0,0)
        limit = 10
        self.velLt = pg.math.Vector2(limit,limit)
        self.repelDist = 30
        
    
    def update(self,dt:float):
        self.boundaryCollsion()
        self.movement(dt)

    #to add forces, velocity and accelration
    def movement(self,dt:float):
        slowmo = 0.01
        dt*=slowmo
        self.vel.x+=(self.accel.x*dt)
        #velocity limiters
        if(abs(self.vel.x)>self.velLt.x):
            self.vel.x = math.copysign(self.velLt.x,self.vel.x) #returns vel limit with sign of vel.x

        self.pos.x += (self.vel.x*(dt)+ self.accel.x*dt**2)
        
        self.vel.y+=(self.accel.y*dt)
        #velocity limiters
        if(abs(self.vel.y)>self.velLt.y):
            self.vel.y = math.copysign(self.velLt.y,self.vel.y)
        self.pos.y += ((self.vel.y*dt + self.accel.y*dt**2))

    def force(self,other): #how to pass a claass hint in its own function god knows
        #normal vector along centres is simply subraction of positional vectors i.e. centres
        N = pg.math.Vector2(self.pos.x-other.pos.x,self.pos.y-other.pos.y)

        #normalise it i.e. make it unit
        n = pg.math.Vector2.normalize(N)

        #distance between centres is mod of normal
        dist = N.length() #mehod gives math.sqrt(x**2 + y**2)
        
        #find mod of the force vector
        modF = 1/dist

        attract = True
        if(dist<=self.repelDist):
            #REPEL
            F = n * modF #spring force proportional to distance
            self.accel += F
            attract = False

        #ATRACTION
        if(attract):
            #force vector / acceleration vector since mass is 1
            #!!!IMPORTANT for some reason 1/3 artifical non physics dampen smooths out the thread
            F = (dist*1/2.5)* n #attraction hence negative

            #adding the acceleration since we need sum of all forces
            self.accel += -F


    #Teleports them upon reaching edge of screen
    def boundaryCollsion(self):
        screen = pg.display.get_surface()

        if((self.pos.y+self.rad) >= screen.get_height()-threshold):
            self.pos.y = threshold + self.rad
            #self.vel.y=-self.vel.y
        
        if((self.pos.y-self.rad) <= threshold):
            self.pos.y = screen.get_height()-threshold - self.rad 
            #self.vel.y=-self.vel.y

        if((self.pos.x-self.rad) <= threshold):
            self.pos.x = screen.get_width()-threshold - self.rad
            #self.vel.x=-self.vel.x
        
        if((self.pos.x+self.rad) >= screen.get_width()-threshold):
            self.pos.x = threshold + self.rad
            #self.vel.x=-self.vel.x

    def draw(self):
        pg.draw.circle(pg.display.get_surface(),self.clr,self.pos,self.rad)


def makerope(bodies:Particle,dt:float,drawNode:bool=True,Fd:float=-0.2):
    """
    Function to create a rope with constraints with individual particles
    """
    #force
    bodies[-1].force(bodies[-2])
    for i in range(1,len(bodies)-1):
        bodies[i].force(bodies[i+1])
        bodies[i].force(bodies[i-1])
    
    #movement and draw
    for body in bodies:
        if(body != bodies[0]):
            body.accel+=pg.math.Vector2(0,0.5) #adding a const gravity
            if(body.vel.x > body.velLt.x-5):
                #dampen constant for force will calculate vectorially later
                body.accel+=pg.math.Vector2(Fd,0)
            if(body.vel.y > body.velLt.y-5):
                body.accel+=pg.math.Vector2(0,Fd)
        body.update(dt)
        if(drawNode):
            body.draw()
        #drawing the line of nodes
        #reset all accel to 0 since we dont want this frame's accel to add up to next frame
        body.accel = pg.math.Vector2(0,0)
    
    #draw thread
    for i in range(len(bodies)-1):
        pg.draw.line(pg.display.get_surface(),"white",bodies[i].pos,bodies[i+1].pos,2)
