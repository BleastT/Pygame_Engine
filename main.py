import Bin.Engine as Engine
import player


def main():

    Game = Engine.APPLICATION((1000,1000),(64,64),show_fps=True, edit_mode=True)
    Game.createObject(Engine.OBJECT('Bin/assets/images/player.png', 'player', 'fluid',start_pos=(30, 8), function=player.MAIN))

    while Game.running:
        # print(Game.get('player').position(), Game.cam_position())
        Game.Poll_Events()
        # print(Engine.pygame.mouse.get_pos())
        Game.update()


if __name__ == "__main__":
    main()
