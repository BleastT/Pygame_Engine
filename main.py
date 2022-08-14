import Bin.Engine as Engine
from Spawner import spawner
from player import player
from enemy import enemy
from Collectible import collectible


def main():


    Game = Engine.APPLICATION((700 ,700),(64,64), max_fps=30, show_fps=False, edit_mode=False, window_name='Flappy Bomb')
    Game.load_functions([player, enemy, spawner, collectible])

    GameStarted = False
    icon = Engine.pygame.image.load('Bin/assets/images/enemy.png')

    Game.load_map('Bin/assets/data/map.txt')
    Game.createUIElement(Engine.UI('start_text', pos=(13,13), font_size=19, font_path='Bin/assets/fonts/poppkorn.ttf', color=(0, 255 ,0)))
    Game.createUIElement(Engine.UI('score_text', pos=(1,-1), font_size=13, font_path='Bin/assets/fonts/poppkorn.ttf', color=(0,0,0)))
    Game.createUIElement(Engine.UI('lives_icon', pos=(50,-1), font_size=13, font_path='Bin/assets/fonts/poppkorn.ttf', color=(255,0,0)))
    Game.createUIElement(Engine.UI('lives_nbr', pos=(53,0), font_size=13, font_path='Bin/assets/fonts/poppkorn.ttf', color=(0,0,0)))
    Game.uiElements['lives_icon'].updateText('♡')
    Game.uiElements['score_text'].updateText('0')
    Game.uiElements['start_text'].updateText('Start')
    Game.play = False
    while Game.running:

        Game.Poll_Events()
        Game.update()
        Engine.pygame.display.set_icon(icon)

        if Game.left_clicking == True:
            if GameStarted == False:
                GameStarted = True
                Game.play = True
            elif GameStarted == True and Game.play == False:
                main()
                break

        Game.uiElements['start_text'].enabled = not Game.play



if __name__ == "__main__":
    main()
