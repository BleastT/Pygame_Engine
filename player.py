import Bin.Engine as Engine


def player(body, deltatime):


    def start():
        body.xspeed = 3
        body.yvelocity = 0
        body.gravity = 1
        body.jumping = False
        body.jumpForce = 8


    def update():
        if Engine.check_key_pressed(Engine.pygame.K_a):
            body.movement[0] = -body.xspeed * deltatime
            body.appRef.xView = 'left'
        elif Engine.check_key_pressed(Engine.pygame.K_d):
            body.movement[0] = body.xspeed * deltatime
            body.appRef.xView = 'right'


        if Engine.check_key_pressed(Engine.pygame.K_SPACE) and body.jumping == False:
            body.yvelocity = -body.jumpForce 
            body.jumping = True
        else:
            body.yvelocity += body.gravity
            

        if body.collision_types['Bottom'] == True:
            body.jumping = False
            body.yvelocity = 0
        elif body.collision_types['Top'] == True:
            body.yvelocity = True

        body.movement[1] = body.yvelocity * deltatime

    
    if body.initialized_script == False:
        start()
        body.initialized_script = True
    else:
        update()



