from PICO8 import PICO8
from Celeste import Celeste

if __name__ == '__main__':
  # load game
  p8 = PICO8(Celeste)

  # build a room and get player
  g = p8.game
  p = g.init_object(g.Player, 0, 0)

  # simulate a jump
  p.spd.y = -2
  print(p)
  for f in range(60):
    p8.step()
    print(p)