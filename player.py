import Bin.Engine as Engine


def player(body):


    def start():

        body.yspeed = 1
        body.score = 0
        body.lives = 3


    def update():
        if Engine.check_key_pressed(Engine.pygame.K_w):
            body.move_by(0, -body.yspeed)
        else:
            body.move_by(0, 1)

        
        if body.collided_with('enemy', 1) == True:
            if body.lives <= 0:
                body.appRef.play = False
                body.appRef.uiElements['start_text'].x = 3
                body.appRef.uiElements['start_text'].y = 24
                body.appRef.uiElements['start_text'].color = (255, 0, 0)
                body.appRef.uiElements['start_text'].font_size = 13
                body.appRef.uiElements['start_text'].updateText('GameOver')
                body.delete()
            else:
                body.lives -= 1

        if body.collided_with('score', 1) == True:
            body.score += 1
            body.appRef.objects['spawner'].enemy_timer -= .01
            body.appRef.objects['spawner'].score_timer += .01


    
    if body.initialized_script == False:
        start()
        body.initialized_script = True
    else:
        update()



