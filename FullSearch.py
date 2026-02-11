from PICO8 import PICO8
from Carts.Celeste import Celeste
import CelesteUtils as utils
import time
from dataclasses import dataclass
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



def find_player(p8):
  # player tends to be near the end
  for o in reversed(p8.game.objects):
    if isinstance(o, p8.game.player):
      return o

def find_player_spawn(p8):
  # player tends to be near the end
  for o in p8.game.objects:
    if isinstance(o, p8.game.player_spawn):
      return o

def load_state(p8: PICO8, state: State):
  utils.place_maddy(p8, state.x, state.y, state.x_rem, state.y_rem, state.x_spd, state.y_spd, state.grace, state.djump)
  p8.game.delay_restart = 0
  p8.game.freeze = state.freeze
  p = find_player(p8)
  assert p
  p.dash_time = state.dash_time

  if state.dash_time > 0:
    p.dash_target.x=state.dash_target_x
    p.dash_target.y=state.dash_target_y
    p.dash_accel.x = 1.5 if state.dash_target_y == 0 else 1.06066017177
    p.dash_accel.y = 1.5 if state.dash_target_x == 0 else 1.06066017177
  else:
    p.dash_target.x, p.dash_target.y = 0,0

def get_state(p8: PICO8) -> State | None:
  p = find_player(p8)
  if not p:
    return None

  target_x = p.dash_target.x if p.dash_time else 0
  target_y = p.dash_target.y if p.dash_time else 0
  # return (p.x, p.y, round(p.rem.x, 1), round(p.rem.y, 1), round(p.spd.x, 5), round(p.spd.y, 5), p.grace, p.djump, p.dash_time, p8.game.freeze)
  return State(p.x, p.y, p.rem.x, p.rem.y, p.spd.x, p.spd.y, p.grace, p.djump, p.dash_time, p8.game.freeze, target_x, target_y)

def step_state(p8: PICO8, state: State, inputs: int) -> State | None:
    load_state(p8, state)
    # print(inputs, find_player(p8))
    p8.set_btn_state(inputs)
    p8.step()
    # print(find_player(p8), get_state(p8))
    return get_state(p8)

def action_restrictions(p8: PICO8, state: State) -> tuple[bool, bool, bool]:
  step_state(p8,state,0)
  p = find_player(p8)
  if not p:
    return False, False, False

  h_movement = abs(p.spd.x) <= 1 or p.is_solid(-1, 0) or p.is_solid(1, 0)
  can_jump = p.grace > 0 or p.is_solid(3, 0) or p.is_solid(-3, 0)
  can_dash = p.djump > 0

  return h_movement, can_jump, can_dash

def get_allowed_inputs(p8, state: State) -> list[int]:
  if state.dash_time:
    return [0]
  h_movement, can_jump, can_dash = action_restrictions(p8, state)

  actions = [0b000000] if not h_movement else [0b000000, 0b000001, 0b000010]
  if can_jump:
    actions.extend([0b010000] if not h_movement else [0b010000, 0b010001, 0b010010])
  if can_dash:
    actions.extend([0b100000, 0b100001, 0b100010, 0b100100, 0b100101, 0b100110, 0b101000, 0b101001, 0b101010])
  return actions

def bfs(level: int, initial_state: State | None = None):
  p8 = PICO8(Celeste)
  utils.load_room(p8, level)

  done = False
  def mark_done():
    nonlocal done
    done = True

  p8.game.next_room = mark_done

  if initial_state is not None:
    load_state(p8, initial_state)
  else:
    utils.skip_player_spawn(p8)
    initial_state = get_state(p8)
    assert initial_state is not None
  utils.suppress_object(p8, p8.game.chest)
  utils.suppress_object(p8, p8.game.key)
  utils.suppress_object(p8, p8.game.key)

  print(p8.game)
  print(initial_state)

  assert len(p8.game.objects) == 1

  visited = set([initial_state])
  curr_depth = [initial_state]
  allowed_inputs = [0, 1, 2, 16, 17, 18, 32, 33, 34, 36, 37, 38, 40, 41, 42]

  depth = 1
  start_time = time.time()

  parent = {}
  final_state = None
  while True:
    next_depth = []
    print(f"depth {depth}, num_visited={len(visited)} elapsed time: {time.time()-start_time}")
    for s in curr_depth:
      prev_state = None
      inps = get_allowed_inputs(p8, s)
      for input in inps:
        next_state = step_state(p8, s, input)
        # print(s, input, next_state)
        if done:
          print(next_state)
          print(f"found solution at depth {depth}!")
          parent[next_state] = (s, input)
          final_state = next_state
          break
        if next_state == prev_state or next_state is None:
          continue

        if next_state not in parent:
          parent[next_state] = (s, input)
          prev_state = next_state
          next_depth.append(next_state)
      if done:
        break


    if done:
      break
    next_depth = set(next_depth) - visited
    visited |= next_depth

    curr_depth = next_depth
    depth += 1

  v = final_state
  full_input = []
  while v != initial_state:
    p, inp = parent[v]
    full_input.append(inp)
    print(full_input, p)
    v = p

  full_input = full_input[::-1]
  print(full_input)






if __name__ == "__main__":
# [player] x: 45, y: 16, rem: {-0.2, 0.00959236}, spd: {-1, -0.45}
  # bfs(4, (45, 16, -0.2, 0.00959, -1, -0.45, 6, True, 0, 0, 0,0))
# [player] x: 42, y: 48, rem: {-0.0395924, -0.450408}, spd: {1.1, -0.45}
  # bfs(4, State(42, 48, -0.0395924, -0.450408, 1.1, -0.45, 6, True, 0, 0, 0, 0))
  bfs(4)
  # p8 = PICO8(Celeste)
  # utils.load_room(p8, 4)
  # state = State(x=14, y=72, x_rem=-0.050000000000000266, y_rem=0.40999999999999925, x_spd=2, y_spd=-1.5, grace=0, djump=0, dash_time=0, freeze=0, dash_target_x=0, dash_target_y=0)
  # print(state)
  # print(step_state(p8, state, 0))











