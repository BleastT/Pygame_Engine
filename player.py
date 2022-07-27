import Bin.Engine as Engine

def MAIN(body, deltatime):
    xspeed = 1000
    yspeed = 500
    def update():
        if Engine.check_key_pressed(Engine.pygame.K_a):
            body.move_by(-xspeed * deltatime, 0)
        elif Engine.check_key_pressed(Engine.pygame.K_d):
            body.move_by(xspeed * deltatime, 0)

        if Engine.check_key_pressed(Engine.pygame.K_w):
            body.move_by(0, -yspeed * deltatime)
        elif Engine.check_key_pressed(Engine.pygame.K_s):
            body.move_by(0, yspeed * deltatime)



    update()
