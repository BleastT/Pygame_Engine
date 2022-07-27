import Bin.Engine as Engine
import player


def main():

    Game = Engine.APPLICATION((1700,758),(1366,758),show_fps=True, max_fps=144)
    Game.createObject(Engine.OBJECT('Bin/assets/images/player_prototype.png', 'player', 'fluid', function=player.MAIN))
    Game.createObject(Engine.OBJECT('Bin/assets/images/player_prototype.png', 'collisionTest', 'static', start_pos=(80, 0)))


    Game.activateCameraFollow('player')
    while Game.running:
        # print(Game.get('player').position(), Game.cam_position())
        Game.Poll_Events()
        # print(Engine.pygame.mouse.get_pos())
        Game.update()
        Game.flip()

if __name__ == "__main__":
    main()
