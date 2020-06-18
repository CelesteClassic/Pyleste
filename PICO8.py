class PICO8():
  def __init__(self, cart):
    self._time = 0
    self._btn_state = 0
    self.load_game(cart)

  # game functions

  def btn(self, i):
    return self._btn_state & (2 ** i) != 0

  def mset(self, x, y, tile):
    self._memory['map'][x + y * 128] = tile

  def mget(self, x, y):
    return self._memory['map'][x + y * 128]

  def fget(self, n, f=None):
    flags = self._memory['flags'][n]
    return flags if f == None else flags & 2 ** f != 0

  # console commands

  def load_game(self, cart):
    self._cart = cart
    self._game = self._cart(self)
    self._memory = {
      'map': [int(self._game.map_data[i:i + 2], 16) if i < 4096 else int(self._game.map_data[i:i + 2][::-1], 16) for i in range(0, len(self._game.map_data), 2)],
      'flags': [int(self._game.flag_data[i:i + 2], 16) for i in range(0, len(self._game.flag_data), 2)]
    }
    print(len(self._memory['map']))
    self._game._init()

  def reset(self):
    self.load_game(self._cart)

  def step(self):
    self._game._update()
    self._game._draw()
    self._time += 1

  def set_button_state(self, state):
    self._btn_state = state

  @property
  def game(self):
    return self._game

  @property
  def time(self):
    return self._time