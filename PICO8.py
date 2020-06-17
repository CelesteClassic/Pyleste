class Table():
  def __init__(self, contents):
    self._contents = contents
  def __getattr__(self, key):
    return self._contents[key]

class PICO8():
  def __init__(self, game):
    self._btn_state = 0
    self._game = game(self)
    self._game._init()

  def step(self):
    self._game._update()
    self._game._draw()

  def set_button_state(self, state):
    self._btn_state = state

  def btn(self, i):
    return self._btn_state & 2 ** i == 1

  @property
  def game(self):
    return self._game

if __name__ == '__main__':
  from Celeste import Celeste
  p8 = PICO8(Celeste)
  p = p8.game.get_player()
  p.spd.y = -2
  for _ in range(60):
    p8.step()
    print(p)