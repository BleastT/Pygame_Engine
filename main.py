from tkinter import font
import Bin.Engine as Engine
from Spawner import spawner
from player import player
from enemy import enemy
from Collectible import collectible


def main():

    Game = Engine.APPLICATION((700 ,700),(64,64), max_fps=30, show_fps=False, edit_mode=True)
    Game.load_functions([player, enemy, spawner, collectible])

    GameStarted = False

    Game.load_map('Bin/assets/data/map.txt')
    Game.createUIElement(Engine.UI('start_text', pos=(13,13), font_size=19, font_path='Bin/assets/fonts/poppkorn.ttf', color=(0, 255 ,0)))
    Game.createUIElement(Engine.UI('score_text', pos=(1,-1), font_size=13, font_path='Bin/assets/fonts/poppkorn.ttf'))
    Game.createUIElement(Engine.UI('score_text', pos=(1,-1), font_size=13, font_path='Bin/assets/fonts/poppkorn.ttf'))
    Game.uiElements['start_text'].updateText('♡')
    Game.play = False
    while Game.running:

        Game.Poll_Events()
        Game.update()

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
