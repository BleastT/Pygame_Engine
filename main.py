import Bin.Engine as Engine
from player import player


def main():

    Game = Engine.APPLICATION((700 ,700),(64,64), max_fps=60, show_fps=True, edit_mode=False)
    Game.load_functions([player])

    Game.load_map('Bin/assets/data/map.txt')
    while Game.running:

        Game.Poll_Events()

        Game.update()



if __name__ == "__main__":
    main()
