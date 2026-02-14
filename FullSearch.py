from PICO8 import PICO8
from Carts.Celeste import Celeste
import CelesteUtils as utils
import time
from dataclasses import dataclass
import resource
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
  djump: int = 1
  dash_time: int = 0
  freeze: int = 0
  dash_target_x: float = 0
  dash_target_y: float = 0

  def canonicalize(self) -> tuple:
    return (self.x, self.y, round(self.x_rem,1), round(self.y_rem,1), round(self.x_spd,5), round(self.y_spd, 5), self.grace, self.djump, self.dash_time, self.freeze, self.dash_target_x, self.dash_target_y)

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
    # return (p.x, p.y, round(p.rem.x, 1), round(p.rem.y, 1), round(p.spd.x, 5), round(p.spd.y, 5), p.grace, p.djump, p.dash_time, p8.game.freeze)
    return State(p.x, p.y, p.rem.x, p.rem.y, p.spd.x, p.spd.y, p.grace, p.djump, p.dash_time, self.p8.game.freeze, target_x, target_y)

  def step_state(self, state: State, inputs: int) -> State | None:
      self.load_state(state)
      # print(inputs, find_player(p8))
      self.p8.set_btn_state(inputs)
      self.p8.step()
      # print(find_player(p8), get_state(p8))
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

  def allowable_actions(self, state: State) -> list[int]:
    if state.dash_time:
      return [0]
    h_movement, can_jump, can_dash = self.action_restrictions(state)

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


  def next_depth(self, curr_depth: list[State], visited: set[State], parent: dict[State, tuple[State, int]]):

    next_depth = []
    winning_states = set()
    for s in curr_depth:
      prev_state = None
      inps = self.allowable_actions(s)
      for input in inps:
        next_state = self.step_state(s, input)
        # print(s, input, next_state)
        if next_state is None:
          if self.is_win():
            winning_states.add((s, input))
          elif self.is_rip():
            continue
        if next_state == prev_state or next_state is None:
          continue

        if next_state not in parent:
          parent[next_state] = (s, input)
          prev_state = next_state
          next_depth.append(next_state)

    next_depth = set(next_depth) - visited
    visited |= next_depth

    return list(next_depth), winning_states


  def construct_inputs_for_state(self, state: State, first_input: int, parent: dict[State, tuple[State, int]]):
    v = state
    full_input = [first_input]
    while v in parent:
      p, inp = parent[v]
      full_input.append(inp)
      v = p

    full_input = full_input[::-1]
    return full_input

  def search(self, max_depth, complete=False):
    self.solutions = []
    timer = time.time()
    initial_state = self.init_state()

    curr_depth = [initial_state]
    visited = set(curr_depth)
    parent = {}
    winning_states = {}
    print('searching...')
    for depth in range(1, max_depth + 1):
      print(f"depth {depth}...")
      next_depth, winning_states = self.next_depth(curr_depth, visited, parent)
      done = winning_states and not complete
      print(f"  elapsed time: {time.time() - timer:.2f} [s],  num_visited={len(visited)}")
      usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
      print(f"Peak Memory Usage: {usage / 1024:.2f} MB")
      if done:
        print(f"found solutions at depth {depth}")
        break
      curr_depth = next_depth

    for state, inp in winning_states:
      inputs = self.construct_inputs_for_state(state, inp, parent)
      self.solutions.append(inputs)
      print(f"  inputs: {inputs}\n  frames: {len(inputs) - 1}")
    return self.solutions



class TestBfsline(BFSline):
  def init_state(self):
    utils.load_room(self.p8, 4)
    utils.skip_player_spawn(self.p8)
    utils.place_maddy(self.p8, 45, 16, -0.2, 0.00959, -1, -0.45, 6, 1)
    utils.suppress_object(self.p8, self.p8.game.chest)
    utils.suppress_object(self.p8, self.p8.game.key)

    print(self.p8.game)
    print(self.get_state())
    return self.get_state()

if __name__ == "__main__":
# [player] x: 42, y: 48, rem: {-0.0395924, -0.450408}, spd: {1.1, -0.45}
  # bfs(4, State(42, 48, -0.0395924, -0.450408, 1.1, -0.45, 6, True, 0, 0, 0, 0))
  bfsline = TestBfsline()
  bfsline.search(100)
  # p8 = PICO8(Celeste)
  # utils.load_room(p8, 4)
  # state = State(x=14, y=72, x_rem=-0.050000000000000266, y_rem=0.40999999999999925, x_spd=2, y_spd=-1.5, grace=0, djump=0, dash_time=0, freeze=0, dash_target_x=0, dash_target_y=0)
  # print(state)
  # print(step_state(p8, state, 0))











