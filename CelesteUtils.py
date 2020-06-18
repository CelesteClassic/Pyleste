from Celeste import Table

def load_room(p8, level_id):
  g = p8.game
  g.load_room(level_id % 8, level_id // 8)

def replace_room(p8, level_id, room_data):
  '''
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . .
  . . . . u . . . . . . . . . . .
  . . . . w > . . . . . . . . . .
  . . . . w > . . . . . . . . . .
  . p . . w > . . . . . . . . . .
  w w w w w w w w w w w w w w w w
  '''
  room_data = room_data.replace('\n', '').replace(' ', '')
  tiles = {
    'w': 32, # terrain
    '^': 17, # up spike
    'v': 27, # down spike
    '<': 59, # leftspike
    '>': 43, # right spike
    'p': 1,  # player spawn
    '.': 0   # empty
  }
  rx, ry = level_id % 8, level_id // 8
  for tx in range(16):
    for ty in range(16):
      tile = room_data[tx + 16 * ty]
      p8.mset(rx * 16 + tx, ry * 16 + ty, tiles[tile] if tile in tiles else 0)

def place_maddy(p8, x, y, remx=0.0, remy=0.0, spdx=0.0, spdy=0.0):
  g = p8.game
  p = g.get_player()
  if p != None:
    g.destroy_object(p)
  p = g.init_object(g.player, x, y)
  p.rem.x, p.rem.y = remx, remy
  p.spd.x, p.spd.y = spdx, spdy