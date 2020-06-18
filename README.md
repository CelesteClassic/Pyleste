# Pyleste
Python Celeste Classic physics simulator.

# Usage
```python
# import PICO-8 emulator and Celeste
from PICO8 import PICO8
from Celeste import Celeste

# create a PICO-8 instance with Celeste loaded
p8 = PICO8(Celeste)

# hold jump key down
p8.set_button_state(0b010000)

# get the game object
g = p8.game

# run for 60 frames
print(g.get_player())
for f in range(60):
  p8.step()
  print(g.get_player())
```

```
0 [player_spawn]
x: 8, y: 128, rem: {0.0000, 0.0000}, spd: {0.0000, -4.0000}
1 [player_spawn]
x: 8, y: 124, rem: {0.0000, 0.0000}, spd: {0.0000, -4.0000}
2 [player_spawn]
x: 8, y: 120, rem: {0.0000, 0.0000}, spd: {0.0000, -4.0000}
3 [player_spawn]
x: 8, y: 116, rem: {0.0000, 0.0000}, spd: {0.0000, -4.0000}
4 [player_spawn]
x: 8, y: 112, rem: {0.0000, 0.0000}, spd: {0.0000, -4.0000}
5 [player_spawn]
x: 8, y: 108, rem: {0.0000, 0.0000}, spd: {0.0000, -4.0000}
6 [player_spawn]
x: 8, y: 104, rem: {0.0000, 0.0000}, spd: {0.0000, -3.5000}
7 [player_spawn]
x: 8, y: 101, rem: {0.0000, -0.5000}, spd: {0.0000, -3.0000}
8 [player_spawn]
x: 8, y: 98, rem: {0.0000, -0.5000}, spd: {0.0000, -2.5000}
9 [player_spawn]
x: 8, y: 95, rem: {0.0000, 0.0000}, spd: {0.0000, -2.0000}
10 [player_spawn]
x: 8, y: 93, rem: {0.0000, 0.0000}, spd: {0.0000, -1.5000}
11 [player_spawn]
x: 8, y: 92, rem: {0.0000, -0.5000}, spd: {0.0000, -1.0000}
12 [player_spawn]
x: 8, y: 91, rem: {0.0000, -0.5000}, spd: {0.0000, -0.5000}
13 [player_spawn]
x: 8, y: 90, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
14 [player_spawn]
x: 8, y: 90, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
15 [player_spawn]
x: 8, y: 90, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
16 [player_spawn]
x: 8, y: 90, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
17 [player_spawn]
x: 8, y: 90, rem: {0.0000, 0.0000}, spd: {0.0000, 0.5000}
18 [player_spawn]
x: 8, y: 91, rem: {0.0000, -0.5000}, spd: {0.0000, 1.0000}
19 [player_spawn]
x: 8, y: 92, rem: {0.0000, -0.5000}, spd: {0.0000, 1.5000}
20 [player_spawn]
x: 8, y: 93, rem: {0.0000, 0.0000}, spd: {0.0000, 2.0000}
21 [player_spawn]
x: 8, y: 95, rem: {0.0000, 0.0000}, spd: {0.0000, 2.5000}
22 [player_spawn]
x: 8, y: 96, rem: {0.0000, -0.5000}, spd: {0.0000, 0.0000}
23 [player_spawn]
x: 8, y: 96, rem: {0.0000, -0.5000}, spd: {0.0000, 0.0000}
24 [player_spawn]
x: 8, y: 96, rem: {0.0000, -0.5000}, spd: {0.0000, 0.0000}
25 [player_spawn]
x: 8, y: 96, rem: {0.0000, -0.5000}, spd: {0.0000, 0.0000}
26 [player_spawn]
x: 8, y: 96, rem: {0.0000, -0.5000}, spd: {0.0000, 0.0000}
27 [player_spawn]
x: 8, y: 96, rem: {0.0000, -0.5000}, spd: {0.0000, 0.0000}
28 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
29 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, -2.0000}
30 [player]
x: 8, y: 93, rem: {0.0000, 0.0000}, spd: {0.0000, -1.7900}
31 [player]
x: 8, y: 90, rem: {0.0000, 0.2100}, spd: {0.0000, -1.5800}
32 [player]
x: 8, y: 88, rem: {0.0000, -0.3700}, spd: {0.0000, -1.3700}
33 [player]
x: 8, y: 85, rem: {0.0000, 0.2600}, spd: {0.0000, -1.1600}
34 [player]
x: 8, y: 83, rem: {0.0000, 0.1000}, spd: {0.0000, -0.9500}
35 [player]
x: 8, y: 81, rem: {0.0000, 0.1500}, spd: {0.0000, -0.7400}
36 [player]
x: 8, y: 79, rem: {0.0000, 0.4100}, spd: {0.0000, -0.5300}
37 [player]
x: 8, y: 79, rem: {0.0000, -0.1200}, spd: {0.0000, -0.3200}
38 [player]
x: 8, y: 79, rem: {0.0000, -0.4400}, spd: {0.0000, -0.1100}
39 [player]
x: 8, y: 77, rem: {0.0000, 0.4500}, spd: {0.0000, -0.0050}
40 [player]
x: 8, y: 77, rem: {0.0000, 0.4450}, spd: {0.0000, 0.1000}
41 [player]
x: 8, y: 79, rem: {0.0000, -0.4550}, spd: {0.0000, 0.2050}
42 [player]
x: 8, y: 79, rem: {0.0000, -0.2500}, spd: {0.0000, 0.4150}
43 [player]
x: 8, y: 79, rem: {0.0000, 0.1650}, spd: {0.0000, 0.6250}
44 [player]
x: 8, y: 81, rem: {0.0000, -0.2100}, spd: {0.0000, 0.8350}
45 [player]
x: 8, y: 83, rem: {0.0000, -0.3750}, spd: {0.0000, 1.0450}
46 [player]
x: 8, y: 85, rem: {0.0000, -0.3300}, spd: {0.0000, 1.2550}
47 [player]
x: 8, y: 87, rem: {0.0000, -0.0750}, spd: {0.0000, 1.4650}
48 [player]
x: 8, y: 89, rem: {0.0000, 0.3900}, spd: {0.0000, 1.6750}
49 [player]
x: 8, y: 92, rem: {0.0000, 0.0650}, spd: {0.0000, 1.8850}
50 [player]
x: 8, y: 95, rem: {0.0000, -0.0500}, spd: {0.0000, 2.0000}
51 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
52 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
53 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
54 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
55 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
56 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
57 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
58 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
59 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
60 [player]
x: 8, y: 96, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
```