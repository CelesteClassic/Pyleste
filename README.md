# Pyleste
Python Celeste Classic physics simulator.

# Usage
```python
# import PICO-8 emulator and Celeste
from PICO8 import PICO8
from Celeste import Celeste

# create a PICO-8 instance with Celeste loaded
p8 = PICO8(Celeste)

# get the game object
g = p8.game

# create a player in the game at 0, 0 (loading rooms/maps not implemented yet)
p = g.init_object(g.Player, 0, 0)

# simulate a jump for 10 frames
p.spd.y = -2
print(p)
for f in range(10):
  p8.step()
  print(p)
```

```
x: 0, y: -3
rem.x: 0.0000, rem.y: 0.0000
spd.x: 0.0000, spd.y: -1.7900
x: 0, y: -6
rem.x: 0.0000, rem.y: 0.2100
spd.x: 0.0000, spd.y: -1.5800
x: 0, y: -8
rem.x: 0.0000, rem.y: -0.3700
spd.x: 0.0000, spd.y: -1.3700
x: 0, y: -11
rem.x: 0.0000, rem.y: 0.2600
spd.x: 0.0000, spd.y: -1.1600
x: 0, y: -13
rem.x: 0.0000, rem.y: 0.1000
spd.x: 0.0000, spd.y: -0.9500
x: 0, y: -15
rem.x: 0.0000, rem.y: 0.1500
spd.x: 0.0000, spd.y: -0.7400
x: 0, y: -17
rem.x: 0.0000, rem.y: 0.4100
spd.x: 0.0000, spd.y: -0.5300
x: 0, y: -17
rem.x: 0.0000, rem.y: -0.1200
spd.x: 0.0000, spd.y: -0.3200
x: 0, y: -17
rem.x: 0.0000, rem.y: -0.4400
spd.x: 0.0000, spd.y: -0.1100
x: 0, y: -19
rem.x: 0.0000, rem.y: 0.4500
spd.x: 0.0000, spd.y: -0.0050
```