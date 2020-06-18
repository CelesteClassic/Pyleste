from PICO8 import PICO8
from Celeste import Celeste

if __name__ == '__main__':
  # load game
  p8 = PICO8(Celeste)

  # build a room and get player
  g = p8.game

  # simulate a jump
  for f in range(100):
    p8.step()
    p = g.get_player()
    print(p)