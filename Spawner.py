import Bin.Engine as Engine
import random

def spawner(body):

    def start():
        body.enemy_timer = 1
        body.enemy_curr_time = 0

        body.score_timer = 2
        body.score_curr_time = 0

    def update():
        x = 70
        y_enemy = random.randint(0, 56)
        y_score = random.randint(0, 56)

        if body.enemy_curr_time > body.enemy_timer:
            body.enemy_curr_time = 0
            body.appRef.createObject(Engine.OBJECT('Bin/assets/images/player.png', name='enemy', category='enemy', type='!static', function='enemy', start_pos=(x,y_enemy)))
        else:
            body.enemy_curr_time += body.appRef.deltatime

        if body.score_curr_time > body.score_timer:
            body.score_curr_time = 0
            body.appRef.createObject(Engine.OBJECT('Bin/assets/images/ground.png', name='score', category='score', type='!static', function='collectible', start_pos=(x,y_score)))
        else:
            body.score_curr_time += body.appRef.deltatime



    
    if body.initialized_script == False:
        start()
        body.initialized_script = True
    else:
        update()