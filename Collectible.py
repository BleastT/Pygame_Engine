import Bin.Engine as Engine

def collectible(body):

    def start():
        body.xspeed = 1

    def update():
        body.move_by(-body.xspeed, 0)

        if body.rect.x + body.width < 0:
            body.delete()


    
    if body.initialized_script == False:
        start()
        body.initialized_script = True
    else:
        update()