import math

class Table():
  def __init__(self, contents):
    self._contents = contents
  def __getattr__(self, key):
    return self._contents[key]

class Celeste():
  def __init__(self, pico8):
    global p8, g
    p8, g = pico8, self

    # game globals
    self.objects = []
    self.freeze = 0

    self.max_djump = 1

    self.k_left = 0
    self.k_right = 1
    self.k_up = 2
    self.k_down = 3
    self.k_jump = 4
    self.k_dash = 5

  # entry point
  def _init(self):
    self.frames = 0

  # game update loop
  def _update(self):
    self.frames = (self.frames + 1) % 30

    if self.freeze > 0:
      self.freeze -= 1
      return

    for o in self.objects:
      o.move(o.spd.x, o.spd.y)
      if callable(getattr(o, 'update', None)):
        o.update()

  # game draw loop
  def _draw(self):
    if self.freeze > 0:
      return

    for o in self.objects:
      if callable(getattr(o, 'draw', None)):
        o.draw()

  # object base class
  class Obj():
    def __init__(self, x, y, tile):
      self.collideable = True,
      self.solids = False
      self.spr = tile
      self.flip = Table({'x': False, 'y': False})
      self.x = x
      self.y = y
      self.hitbox = Table({'x': 0, 'y': 0, 'w': 8, 'h': 8})
      self.spd = Table({'x': 0.0, 'y': 0.0})
      self.rem = Table({'x': 0.0, 'y': 0.0})

    def is_solid(self, ox, oy):
      # [not implemented]
      return False

    def is_ice(self, ox, oy):
      # [not implemented]
      return False

    def check(type, ox, oy):
      # [not implemented]
      return False

    def move(self, ox, oy):
      self.rem.x += ox
      amt = math.floor(self.rem.x + 0.5)
      self.rem.x -= amt
      self.move_x(amt, 0)
      self.rem.y += oy
      amt = math.floor(self.rem.y + 0.5)
      self.rem.y -= amt
      self.move_y(amt)

    def move_x(self, amt, start):
      if self.solids:
        step = g.sign(amt)
        for i in range(start, abs(amt) + 1):
          if not self.is_solid(step, 0):
            self.x += step
          else:
            self.spd.x = 0
            self.rem.x = 0
            break
      else:
        self.x += amt

    def move_y(self, amt):
      if self.solids:
        step = g.sign(amt)
        for i in range(abs(amt) + 1):
          if not self.is_solid(step, 0):
            self.y += step
          else:
            self.spd.y = 0
            self.rem.y = 0
            break
      else:
        self.y += amt

  # player object

  class Player(Obj):
    def __init__(self, x, y, tile):
      g.Obj.__init__(self, x, y, tile)

    def init(self):
      self.p_jump = False
      self.p_dash = False
      self.grace = 0
      self.jbuffer = 0
      self.djump = 1
      self.dash_time = 0
      self.dash_effect_time = 0
      self.dash_target = Table({'x': 0.0, 'y': 0.0})
      self.dash_accel = Table({'x': 0.0, 'y': 0.0})
      self.hitbox = Table({'x': 1, 'y': 3, 'w': 6, 'h': 5})
      self.solids = True
    
    def update(self):
      # horizontal input
      h_input = 1 if p8.btn(g.k_right) else -1 if p8.btn(g.k_left) else 0

      # spike collision
      if g.spikes_at(self.x + self.hitbox.x, self.y + self.hitbox.y, self.hitbox.w, self.hitbox.h, self.spd.x, self.spd.y):
        g.kill_player(self)

      # bottom death
      if self.y > 128:
        g.kill_player(self)

      # on ground check
      on_ground = self.is_solid(0, 1)

      # jump and dash inmput
      jump = p8.btn(g.k_jump) and not self.p_jump
      dash = p8.btn(g.k_dash) and not self.p_dash
      self.p_jump = p8.btn(g.k_jump)
      self.p_dash = p8.btn(g.k_dash)

      # jump buffer
      if jump:
        self.jbuffer = 4
      elif self.jbuffer > 0:
        self.jbuffer -= 1

      # grace frames and dash restoration
      if on_ground:
        self.grace = 6
        self.djump = g.max_djump
      elif self.grace > 0:
        self.grace -= 1

      # dash effect timer (for dash-triggered events, e.g., berry blocks)
      self.dash_effect_time -= 1

      if self.dash_time > 0:
        self.dash_time -= 1
        self.spd.x = g.appr(self.spd.x, self.dash_target.x, self.dash_accel.x)
        self.spd.y = g.appr(self.spd.y, self.dash_target.y, self.dash_accel.y)
      else:
        maxrun = 1
        accel = (0.6 if not self.is_ice(0, 1) else 0.05) if on_ground else 0.4
        deccel = 0.15

        # set x speed
        self.spd.x = g.appr(self.spd.x, h_input * maxrun, accel) if abs(self.spd.x) <= 1 else g.appr(self.spd.x, sign(self.spd.x) * maxrun, deccel)

        # facing direction
        if self.spd.x != 0:
          self.flip.x = self.spd.x < 0

        # terminal vel + wall sliding
        maxfall = 2 if not (h_input != 0 and self.is_solid(h_input, 0) and not self.is_ice(h_input, 0)) else 0.4

        # apply gravity
        self.spd.y = g.appr(self.spd.y, maxfall, 0.21 if abs(self.spd.y) > 0.15 else 0.105)

        # jump
        if self.jbuffer > 0:
          if self.grace > 0:
            self.jbuffer = 0
            self.grace = 0
            self.spd.y = -2
          else:
            wall_dir = -1 if self.is_solid(-3, 0) else 1 if self.is_solid(3, 0) else 0
            if wall_dir != 0:
              self.jbuffer = 0
              self.spd.y = -2
              self.spd.x = -wall_dir * (maxrun + 1)

        # dash
        d_full = 5
        d_half = 3.5355339059

        if self.djump > 0 and dash:
          self.djump -= 1
          self.dash_time = 4
          self.dash_effect_time = 10
          # vertical input
          v_input = -1 if p8.btn(g.k_up) else 1 if p8.btn(g.k_down) else 0
          # calculate dash speeds
          self.spd.x = h_input * (d_full if v_input == 0 else d_half) if h_input != 0 else (0 if v_input != 0 else -1 if self.flip.x else 1)
          self.spd.y = v_input * (d_full if h_input == 0 else d_half) if v_input != 0 else 0
          # effects
          freeze = 2
          # dash target speeds and accels
          self.dash_target.x = 2 * sign(self.spd.x)
          self.dash_target.y = (2 if self.spd.y >= 0 else 1.5) * sign(self.spd.y)
          self.dash_accel.x = 1.5 if self.spd.y == 0 else 1.06066017177
          self.dash_accel.y = 1.5 if self.spd.x == 0 else 1.06066017177

      # exit level off the top
      if self.y < -4:
        # [not implemented]
        pass

    def draw(self):
      if self.x < -1 or self.x > 121:
        self.x = g.clamp(self.x, -1, 121)
        self.spd.x = 0

    def __str__(self):
      return 'x: {}, y: {}\nrem.x: {:.4f}, rem.y: {:.4f}\nspd.x: {:.4f}, spd.y: {:.4f}'.format(self.x, self.y, self.rem.x, self.rem.y, self.spd.x, self.spd.y)

  # object handling stuff

  def init_object(self, obj, x, y, tile=None):
    o = obj(x, y, tile)
    self.objects.append(o)
    if callable(getattr(o, 'init', None)):
      o.init()
    return o

  def destroy_object(self, obj):
    self.objects.remove(obj)

  def kill_player(self, obj):
    self.destroy_object(obj)

  # helper functions

  def get_player(self):
    for o in self.objects:
      if type(o) == self.Player:
        return o

  def clamp(self, val, a, b):
    return max(a, min(b, val))

  def appr(self, val, target, amount):
    return max(val - amount, target) if val > target else min(val + amount, target)

  def sign(self, x):
    return 1 if x > 0 else -1 if x < 0 else 0

  def spikes_at(self, x, y, w, h, spdx, spdy):
    # [not implemented]
    return False