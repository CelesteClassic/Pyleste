from PICO8 import PICO8
from Celeste import Celeste

if __name__ == '__main__':
  p8 = PICO8(Celeste)
  p = p8.game.get_player()
  # simulate a jump
  p.spd.y = -2
  for _ in range(60):
    p8.step()
    print(p)