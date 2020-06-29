# exiting the level restarts the level
def enable_loop_mode(p8):
  def loop_room(): p8.game.next_rm = True
  p8.game.next_room = loop_room

# set max number of dashes
def set_max_djump(p8, max_djump):
  p8.game.max_djump = max_djump

# load a room by level id
# loading jank simulates extra updates performed by vanilla's foreach
def load_room(p8, level_id, loading_jank=False):
  p8.set_btn_state(0)
  p8.game.load_room(level_id % 8, level_id // 8)
  if loading_jank and level_id > 0:
    object_counts = [2, 1, 4, 14, 3, 2, 12, 9, 6, 5, 7, 3, 6, 5, 11, 8, 4, 7, 3, 6, 8, 2, 2, 1, 8, 3, 3, 7, 6, 7, 2]
    for o in p8.game.objects[object_counts[level_id - 1] - 1:object_counts[level_id]]:
      o.move(o.spd.x, o.spd.y)
      if callable(getattr(o, 'update', None)):
        o.update()

# remove all instances of an object from the current loaded room
def suppress_object(p8, object_type):
  p8.game.objects = [obj for obj in p8.game.objects if type(obj) != object_type]

# skip player spawn animation
def skip_player_spawn(p8):
  while type(p8.game.get_player()) == p8.game.player_spawn: p8.step()

# replace a room with a 128-character room string
# every 16 characters represents a row of the room, rows going from top to bottom
# ignores spaces, line breaks, and letter cases
def replace_room(p8, level_id, room_data):
  room_data = room_data.replace('\n', '').replace(' ', '').lower()
  tiles = {
    'w': 32, # terrain
    '^': 17, # up spike
    'v': 27, # down spike
    '<': 59, # leftspike
    '>': 43, # right spike
    'b': 22, # balloon
    'c': 23, # crumble block
    's': 18, # spring
    'p': 1,  # player spawn
    '.': 0   # empty
  }
  rx, ry = level_id % 8, level_id // 8
  for tx in range(16):
    for ty in range(16):
      tile = room_data[tx + 16 * ty]
      p8.mset(rx * 16 + tx, ry * 16 + ty, tiles[tile] if tile in tiles else 0)

# forces an already spawned maddy to be in a specific state
def place_maddy(p8, x, y, remx=0.0, remy=0.0, spdx=0.0, spdy=0.0, grace=6, djump=1):
  p = p8.game.get_player()
  if p: p8.game.objects.remove(p)
  p = p8.game.init_object(p8.game.player, x, y)
  p.rem.x, p.rem.y = remx, remy
  p.spd.x, p.spd.y = spdx, spdy
  p.grace, p.djump = grace, djump

# render the game from the current game state onward given a list of inputs
def watch_inputs(p8, inputs):
  import time
  print(p8.input_display)
  print(p8.game)
  for a in inputs:
    time.sleep(1 / 30)
    p8.set_btn_state(a)
    p8.step()
    print(p8.input_display)
    print(p8.game)