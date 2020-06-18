class PICO8():
  def __init__(self, cart):
    self._time = 0
    self._btn_state = 0
    self.load_game(cart)

  # game functions

  def btn(self, i):
    return self._btn_state & 2 ** i != 0

  def mget(self, x, y):
    addr = 2 * (x + y * 128)
    return int(self._mem_map[addr:addr + 2], 16)

  def fget(self, n, f=None):
    addr = 2 * n
    flags = int(self._mem_flags[addr:addr + 2], 16)
    return flags if f == None else flags & 2 ** f != 0

  # console commands

  def load_game(self, cart):
    self._cart = cart
    self._game = self._cart(self)
    self._mem_map = self._game.map_data
    self._mem_flags = self._game.flag_data
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
    return self._t