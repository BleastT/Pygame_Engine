import Bin.Engine as Engine
import random

def spawner(body):

    def start():
        body.enemy_timer = 1
        body.enemy_curr_time = 0

        body.score_timer = 2
        body.score_curr_time = 0

    def update():
        x_enemy = random.randint(70, 90)
        x_score = random.randint(70, 90)
        y_enemy = random.randint(0, 56)
        y_score = random.randint(0, 56)
        spawned = False

        if body.enemy_curr_time > body.enemy_timer:
            spawned = True
            body.enemy_curr_time = 0
            body.appRef.createObject(Engine.OBJECT('Bin/assets/images/enemy.png', name='enemy', category='enemy', type='!static', function='enemy', start_pos=(x_enemy,y_enemy)))
        else:
            body.enemy_curr_time += body.appRef.deltatime

        if spawned == False:
            if body.score_curr_time > body.score_timer:
                body.score_curr_time = 0
                body.appRef.createObject(Engine.OBJECT('Bin/assets/images/coin.png', name='score', category='score', type='!static', function='collectible', start_pos=(x_score,y_score)))
            else:
                body.score_curr_time += body.appRef.deltatime




    
    if body.initialized_script == False:
        start()
        body.initialized_script = True
    else:
        update()