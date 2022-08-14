import Bin.Engine as Engine


def player(body):


    def start():

        body.yspeed = 1
        body.score = 0
        body.lives = 5

        body.appRef.uiElements['score_text'].updateText(str(body.score))
        body.appRef.uiElements['lives_nbr'].updateText(str(body.lives))


    def update():


        if Engine.check_key_pressed(Engine.pygame.K_w):
            body.move_by(0, -body.yspeed)
        else:
            body.move_by(0, 1)

        
        if body.collided_with('enemy', 1, True) == True:
            if body.lives < 1:
                body.appRef.play = False
                body.appRef.uiElements['start_text'].x = 3
                body.appRef.uiElements['start_text'].y = 24
                body.appRef.uiElements['start_text'].color = (255, 0, 0)
                body.appRef.uiElements['start_text'].font_size = 13
                body.appRef.uiElements['start_text'].updateText('GameOver')
                body.delete()
            else:
                body.lives -= 1
                body.appRef.uiElements['lives_nbr'].updateText(str(body.lives))

        if body.collided_with('score', 1, True) == True:
            body.score += 1
            body.appRef.objects['spawner'].enemy_timer -= .03
            body.appRef.objects['spawner'].score_timer += .03
            body.appRef.uiElements['score_text'].updateText(str(body.score))


        if body.rect.y <= 0:
            body.move_to(body.rect.x, 0)
        elif body.rect.y + body.height >= 64:
            body.move_to(body.rect.x, 64 - body.height)



    
    if body.initialized_script == False:
        start()
        body.initialized_script = True
    else:
        update()



