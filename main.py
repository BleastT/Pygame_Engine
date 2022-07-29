import Bin.Engine as Engine
import player


def main():

    Game = Engine.APPLICATION((1366,758),show_fps=True)
    Game.createObject(Engine.OBJECT('Bin/assets/images/player_prototype.png', 'player', 'fluid', function=player.MAIN))
    Game.createObject(Engine.OBJECT('Bin/assets/images/player_prototype.png', '', 'static',start_pos=(0, 80) ,function=player.MAIN))
    Game.createObject(Engine.OBJECT('Bin/assets/images/player_prototype.png', '', 'static',start_pos=(64, 80) ,function=player.MAIN))
    Game.createObject(Engine.OBJECT('Bin/assets/images/player_prototype.png', '', 'static',start_pos=(128, 80) ,function=player.MAIN))
    Game.createObject(Engine.OBJECT('Bin/assets/images/player_prototype.png', '', 'static',start_pos=(182, 80) ,function=player.MAIN))

    Game.activateCameraFollow('player')
    while Game.running:
        # print(Game.get('player').position(), Game.cam_position())
        Game.Poll_Events()
        # print(Engine.pygame.mouse.get_pos())
        Game.update()
        Game.flip()


if __name__ == "__main__":
    main()
