from PICO8 import PICO8
from Carts.Celeste import Celeste
import CelesteUtils as utils

import time
import copy
import math

'''
To define and run a search problem:

1. Create a class which inherits from Searcheline

2. Override the following methods as needed:

  > init_state(self) [REQUIRED]
    - initial state (list of game objects) to search from
    - e.g., load the room and place maddy in Searcheline's game instance (self.p8.game), return self.p8.game.objects
  
  > allowable_actions(self, objs, player, h_movement, can_jump, can_dash)
    - get list of available inputs for a state
    - default: all actions
    - override this to restrict inputs (e.g., only up-dashes, no directional movement when player's y < 50, etc.)
  
  > h_cost(self, objs)
    - estimated number of steps to satisfy the goal condition
    - default: infinity if is_rip, exit_heuristic otherwise
    - override to change or include additional heuristics
    
    > is_rip(self, objs)
      - rip conditions (situations not worth considering further)
      - default: player dies
      - override to change or include other rip conditions (e.g., don't consider cases where player's x > 64, etc.)
    
    > exit_heuristic(self, player)
      - underestimated number of steps to exit off the top
      - default: assumes player zips upward at a speed of 6 px/step
      - override to specify a less conservative estimate (e.g., if exit will be off a jump, can use 3 px/step)
  
  > is_goal(self, objs)
    - define goal conditions
    - default: exited the level
    - override to change goal conditions (e.g., reach certain coordinates with a dash available)

3. Instantiate the class, and call instance.search(max_depth)

  > use optional argument complete=True to search up to max_depth, even if a solution has already been found
'''

class Searcheline():
  def __init__(self, cart=None):
    self.solutions = []
    self.p8 = PICO8(Celeste if cart == None else cart)
    utils.enable_loop_mode(self.p8)
    

  # initial state (list of game objects) to search from
  # must override this
  def init_state(self):
    # e.g., swap out a room, load it, place maddy
    # return self.p8.game.objects
    raise NotImplementedError

  # define list of available inputs for a state
  # default: all actions
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    ''' button states
      0b000000 -  0 - no input
      0b000001 -  1 - l
      0b000010 -  2 - r
      0b010000 - 16 - z
      0b010001 - 17 - l + z
      0b010010 - 18 - r + z
      0b100000 - 32 - x
      0b100001 - 33 - l + x
      0b100010 - 34 - r + x
      0b100100 - 36 - u + x
      0b100101 - 37 - u + l + x
      0b100110 - 38 - u + r + x
      0b101000 - 40 - d + x
      0b101001 - 41 - d + l + x
      0b101010 - 42 - d + r + x
    '''
    actions = [0b000000] if not h_movement else [0b000000, 0b000001, 0b000010]
    if can_jump:
      actions.extend([0b010000] if not h_movement else [0b010000, 0b010001, 0b010010])
    if can_dash:
      actions.extend([0b100000, 0b100001, 0b100010, 0b100100, 0b100101, 0b100110, 0b101000, 0b101001, 0b101010])
    return actions

  # estimated number of steps to satisfy the goal condition
  # default: infinity if is_rip, exit_heuristic otherwise
  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      return self.exit_heuristic(self.find_player(objs))

  # rip conditions (situations not worth considering further)
  # default: player dies
  def is_rip(self, objs):
    return not self.find_player(objs)

  # underestimated number of steps to exit off the top
  # default: assumes player zips upward at a speed of 6 px/step
  def exit_heuristic(self, player, exit_spd_y=6):
    return math.ceil((player.y + 4) / exit_spd_y)

  # define goal conditions
  # default: exited the level
  def is_goal(self, objs):
    return self.find_player_spawn(objs)

  # get list of available inputs for a state
  def get_actions(self, objs):
    p = self.find_player(objs)
    if p.dash_time != 0: return [0b000000]
    return self.allowable_actions(objs, p, *self.action_restrictions(objs, p))

  # apply inputs to a state, disable freeze and respawn globals as one game instance is shared
  def transition(self, objs, a):
    self.p8.game.objects = copy.deepcopy(objs)
    self.p8.set_btn_state(a)
    self.p8.step()
    freeze = self.p8.game.freeze
    self.p8.game.freeze = 0
    self.p8.game.delay_restart = 0
    return self.p8.game.objects, freeze

  # IDDFS
  def iddfs(self, state, depth, inputs):
    if depth == 0 and self.is_goal(state):
      self.solutions.append(inputs)
      print(f"  inputs: {inputs}\n  frames: {len(inputs) - 1}")
      return True
    else:
      optimal_depth = False
      if depth > 0 and self.h_cost(state) <= depth:
        for a in self.get_actions(state):
          new_state, freeze = self.transition(state, a)
          done = self.iddfs(new_state, depth - 1 - freeze, inputs + [a] + [0] * freeze)
          if done:
            optimal_depth = True
      return optimal_depth

  # run IDDFS routine
  def search(self, max_depth, complete=False):
    self.solutions = []
    timer = time.time()
    state = self.init_state()
    print('searching...')
    for depth in range(1, max_depth + 1):
      print(f"depth {depth}...")
      done = self.iddfs(state, depth, []) and not complete
      print(f"  elapsed time: {time.time() - timer:.2f} [s]")
      if done:
        break
    return self.solutions

  # find player in list of objects (override if player will be at a known position in the object list)
  def find_player(self, objs):
    for o in objs:
      if type(o) == self.p8.game.player:
        return o

  # find player_spawn in list of objects (override if player_spawn will be at a known position in the object list)
  def find_player_spawn(self, objs):
    for o in objs:
      if type(o) == self.p8.game.player_spawn:
        return o

  # compute the player's next displacement to check if a jump/dash will be available next frame
  def compute_displacement(self, player):
    sign = lambda x: 1 if x > 0 else -1 if x < 0 else 0
    dx, dy = round(player.rem.x + player.spd.x), round(player.rem.y + player.spd.y)
    dx, dy = dx + sign(dx), dy + sign(dy)
    while player.is_solid(dx, 0): dx -= sign(player.spd.x)
    while player.is_solid(dx, dy): dy -= sign(player.spd.y)
    return dx, dy

  # compute basic action restrictions (can move horizontally, can jump, can dash)
  def action_restrictions(self, objs, player):
    dx, dy = self.compute_displacement(player)
    h_movement = abs(player.spd.x) <= 1
    can_jump = not player.p_jump and (player.grace - 1 > 0 or player.is_solid(-3 + dx, dy) or player.is_solid(3 + dx, dy) or player.is_solid(dx, 1 + dy))
    can_dash = player.djump > 0 or player.is_solid(dx, 1 + dy) or player.check(self.p8.game.balloon, 0, 0) or player.check(self.p8.game.fruit, 0, 0) or player.check(self.p8.game.fly_fruit, 0, 0)
    return h_movement, can_jump, can_dash

  # translate a list of inputs into english
  def inputs_to_english(self, inputs):
    action_dict = {
      0: 'no input',
      1: 'left',
      2: 'right',
      16: 'neutral jump',
      17: 'jump left',
      18: 'jump right',
      32: 'empty dash',
      33: 'left dash',
      34: 'right dash',
      36: 'up dash',
      37: 'up-left dash',
      38: 'up-right dash',
      40: 'down dash',
      41: 'down-left dash',
      42: 'down-right dash'
    }
    return ', '.join([action_dict[a] for a in inputs])