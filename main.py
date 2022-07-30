import Bin.Engine as Engine
from player import player


def main():

    Game = Engine.APPLICATION((700,700),(64,64), max_fps=60, show_fps=True, edit_mode=True)

    # print(Engine.encrypt_decrypt(Engine.read_from_file('Bin/assets/data/text.txt'), 1))
    # Engine.write_to_file('Bin/assets/data/text.txt',Engine.encrypt_decrypt(Engine.convert_to_text(Game.objects)))
    Game.load_map('Bin/assets/data/text.txt', [player])
    # Game.save_map('Bin/assets/data/text.txt')
    while Game.running:
        # print(Game.get('player').position(), Game.cam_position())
        Game.Poll_Events()
        # print(Engine.pygame.mouse.get_pos())
        Game.update()


if __name__ == "__main__":
    main()
