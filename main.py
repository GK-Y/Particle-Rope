import rope
import pygame as pg


def main():
    HT = 1000
    WT = 1000

    threshold = rope.threshold

    #rope list to hold all particles
    bodies=[]
    length = 25 #length of rope in units
    for i in range(length):
        bodies.append(rope.Particle("green",(500+(i*15),20+(i*rope.Particle().repelDist)),rad=5))

    #anchor the first node to hang the rope
    bodies[0].accel=pg.math.Vector2(0,0)

    #boundary padding display
    boundary = pg.Rect(threshold,threshold,WT-2*threshold,HT-2*threshold)

    pg.init()

    screen = pg.display.set_mode((WT,HT))

    clk = pg.time.Clock()
    fps = 60
    running = True

    while running:
        dt = clk.tick(fps)
        for event in pg.event.get():
            if event.type== pg.QUIT:
                running=False

        screen.fill("black")

        rope.makerope(bodies,dt=dt,drawNode=True)

        pg.draw.rect(screen,"blue",boundary,2)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
