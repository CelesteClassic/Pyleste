# Pyleste
Python Celeste Classic physics simulator.

# Usage
```python
  # import PICO-8 emulator and Celeste
  from PICO8 import PICO8
  from Celeste import Celeste

  # useful Celeste utils
  import CelesteUtils as utils

  # create a PICO-8 instance with Celeste loaded
  p8 = PICO8(Celeste)

  # hold up + right + x
  p8.set_inputs(u=True, r=True, x=True)

  # swap 100m with this level and reload it
  room_data= '''
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
  . . . . ^ . . . . . . . . . . .
  . . . . w > . . . . . . . . . .
  . . . . w > . . . . . . . . . .
  . . . . w > . . p . . . . . . .
  w w w w w w w w w w w w w w w w
  '''
  utils.replace_room(p8, 0, room_data)
  utils.load_room(p8, 0)

  # force (an already spawned) maddy to be at 0, 112
  utils.place_maddy(p8, 0, 112)

  # run for 20f while outputting player info
  print(p8.game.get_player())
  for f in range(20):
    p8.step()
    print(p8.game.get_player())
```

```
0 [player]
x: 0, y: 112, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
1 [player]
x: 0, y: 112, rem: {0.0000, 0.0000}, spd: {3.5355, -3.5355}
2 [player]
x: 5, y: 107, rem: {-0.4645, 0.4645}, spd: {2.4749, -2.4749}
3 [player]
x: 8, y: 104, rem: {0.0104, -0.0104}, spd: {2.0000, -1.5000}
4 [player]
x: 11, y: 101, rem: {0.0104, 0.4896}, spd: {2.0000, -1.5000}
5 [player]
x: 14, y: 99, rem: {0.0104, -0.0104}, spd: {2.0000, -1.5000}
6 [player]
x: 17, y: 96, rem: {0.0104, 0.4896}, spd: {1.8500, -1.2900}
7 [player]
x: 20, y: 94, rem: {-0.1396, 0.1996}, spd: {1.7000, -1.0800}
8 [player]
x: 23, y: 92, rem: {-0.4396, 0.1196}, spd: {1.5500, -0.8700}
9 [player]
x: 25, y: 90, rem: {0.1104, 0.2496}, spd: {1.4000, -0.6600}
10 [player]
x: 25, y: 90, rem: {0.0000, -0.4104}, spd: {0.4000, -0.4500}
11 [player]
x: 25, y: 88, rem: {0.4000, 0.1396}, spd: {0.8000, -0.2400}
12 [player]
x: 27, y: 88, rem: {0.2000, -0.1004}, spd: {1.0000, -0.2400}
13 [player]
x: 29, y: 88, rem: {0.2000, -0.3404}, spd: {1.0000, -0.2400}
14 [player]
x: 31, y: 86, rem: {0.2000, 0.4196}, spd: {1.0000, -0.0300}
15 [player]
x: 33, y: 86, rem: {0.2000, 0.3896}, spd: {1.0000, 0.0750}
16 [player]
x: 35, y: 86, rem: {0.2000, 0.4646}, spd: {1.0000, 0.1800}
None
None
None
None
```