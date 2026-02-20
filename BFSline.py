from PICO8 import PICO8
from Carts.Celeste import Celeste
import CelesteUtils as utils
import time
from dataclasses import dataclass
try:
  import resource
except:
  resource = None
# import tqdm

@dataclass(slots=True, frozen=True)
class State:
  x: int
  y: int
  x_rem: float
  y_rem: float
  x_spd: float
  y_spd: float
  grace: int = 6
  p_jump: bool = False
  djump: int = 1
  dash_time: int = 0
  freeze: int = 0
  dash_target_x: float = 0
  dash_target_y: float = 0

  def canonicalize(self) -> tuple:
    return (self.x, self.y, round(self.x_rem,1), round(self.y_rem,2), round(self.x_spd,5), round(self.y_spd, 5), self.grace, self.p_jump, self.djump, self.dash_time, self.freeze, self.dash_target_x, self.dash_target_y)

  def __eq__(self, other: "State") -> bool:
    return other and self.canonicalize() == other.canonicalize()

  def __hash__(self):
    return hash(self.canonicalize())


class BFSline:

  def __init__(self, cart=None):
    self.solutions = []
    self.p8 = PICO8(Celeste if cart == None else cart)
    utils.enable_loop_mode(self.p8)

  def find_player(self):
    # player tends to be near the end
    for o in reversed(self.p8.game.objects):
      if isinstance(o, self.p8.game.player):
        return o

  def find_player_spawn(self):
    # player tends to be near the end
    for o in self.p8.game.objects:
      if isinstance(o, self.p8.game.player_spawn):
        return o

  def load_state(self, state: State):
    utils.place_maddy(self.p8, state.x, state.y, state.x_rem, state.y_rem, state.x_spd, state.y_spd, state.grace, state.djump)
    self.p8.game.delay_restart = 0
    self.p8.game.freeze = state.freeze
    p = self.find_player()
    assert p
    p.p_jump = state.p_jump
    p.dash_time = state.dash_time

    if state.dash_time > 0:
      p.dash_target.x=state.dash_target_x
      p.dash_target.y=state.dash_target_y
      p.dash_accel.x = 1.5 if state.dash_target_y == 0 else 1.06066017177
      p.dash_accel.y = 1.5 if state.dash_target_x == 0 else 1.06066017177
    else:
      p.dash_target.x, p.dash_target.y = 0,0

  def get_state(self) -> State | None:
    p = self.find_player()
    if not p:
      return None

    target_x = p.dash_target.x if p.dash_time else 0
    target_y = p.dash_target.y if p.dash_time else 0
    return State(p.x, p.y, p.rem.x, p.rem.y, p.spd.x, p.spd.y, p.grace, p.p_jump, p.djump, p.dash_time, self.p8.game.freeze, target_x, target_y)

  def step_state(self, state: State, inputs: int) -> State | None:
      self.load_state(state)
      self.p8.set_btn_state(inputs)
      self.p8.step()
      return self.get_state()

  def action_restrictions(self, state: State) -> tuple[bool, bool, bool]:
    self.step_state(state,0)
    p = self.find_player()
    if not p:
      return False, False, False

    h_movement = abs(p.spd.x) <= 1 or p.is_solid(-1, 0) or p.is_solid(1, 0)
    can_jump = p.grace > 0 or p.is_solid(3, 0) or p.is_solid(-3, 0)
    can_dash = p.djump > 0

    return h_movement, can_jump, can_dash

  def allowable_actions(self, state: State, h_movement, can_jump, can_dash) -> list[int]:
    actions = [0b000000] if not h_movement else [0b000000, 0b000001, 0b000010]
    if can_jump:
      actions.extend([0b010000] if not h_movement else [0b010000, 0b010001, 0b010010])
    if can_dash:
      actions.extend([0b100000, 0b100001, 0b100010, 0b100100, 0b100101, 0b100110, 0b101000, 0b101001, 0b101010])
    return actions

  def is_win(self):
    return self.find_player_spawn()

  def is_rip(self):
    return not self.find_player()

  # initial state (list of game objects) to search from
  # must override this
  def init_state(self):
    # e.g., swap out a room, load it, place maddy
    # return self.get_state() or a state object
    raise NotImplementedError

  def get_actions(self, state: State):
    if state.dash_time != 0: return [0b000000]
    return self.allowable_actions(state, *self.action_restrictions(state))


  def next_depth(self, curr_depth: list[State], parent: dict[State, tuple[State, int]]):

    next_depth = []
    winning_states = set()
    for s in curr_depth:
      prev_state = None
      inps = self.get_actions(s)
      for input in inps:
        next_state = self.step_state(s, input)
        if self.is_win():
          winning_states.add((s, input))
        elif next_state is None or self.is_rip():
          continue
        if next_state == prev_state or next_state is None:
          continue

        if next_state not in parent:
          parent[next_state] = (s, input)
          prev_state = next_state
          next_depth.append(next_state)


    return next_depth, winning_states


  def construct_inputs_for_state(self, state: State, first_input: int, parent: dict[State, tuple[State, int]]):
    v = state
    full_input = [first_input]
    while v in parent:
      p, inp = parent[v]
      if not p:
        break
      full_input.append(inp)
      v = p

    full_input = full_input[::-1]
    return full_input

  def depth_base_states(self, depth: int):
    if depth==1:
      return [self.init_state()]
    return []

  def search(self, max_depth, complete=False):
    self.solutions = []
    timer = time.time()

    curr_depth = []
    parent = {s: (None,0) for s in curr_depth}
    all_winning_states = set()
    print('searching...')
    for depth in range(1, max_depth + 1):
      print(f"depth {depth}...")
      curr_depth += self.depth_base_states(depth)
      next_depth, winning_states = self.next_depth(curr_depth, parent)
      all_winning_states |= winning_states
      done = winning_states and not complete
      print(f"  elapsed time: {time.time() - timer:.2f} [s],  num_visited={len(parent)}")
      if resource is not None:
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(f"Peak Memory Usage: {usage / 1024:.2f} MB")
      if done:
        print(f"found solutions at depth {depth}")
        break
      curr_depth = next_depth

    self.winning_states = []
    for state, inp in all_winning_states:
      inputs = self.construct_inputs_for_state(state, inp, parent)
      self.solutions.append(inputs)
      self.winning_states.append(state)
      print(f"  inputs: {inputs}\n  frames: {len(inputs) - 1}")
    return self.solutions
