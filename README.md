# Pyleste
Python Celeste Classic emulator. Comes with useful utils (CelesteUtils.py) for setting up and simulating specific situations in both existing and custom-specified levels.

## Sample Usage
```python
# import PICO-8 emulator and Celeste
from PICO8 import PICO8
from Carts.Celeste import Celeste

# useful Celeste utils
import CelesteUtils as utils

# create a PICO-8 instance with Celeste loaded
p8 = PICO8(Celeste)

# swap 100m with this level and reload it
room_data = '''
w w w w w w w w w w . . . . w w
w w w w w w w w w . . . . . < w
w w w v v v v . . . . . . . < w
w w > . . . . . . . . . . . . .
w > . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . .
. . . . . . . . . b . . . b . .
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

# skip the player spawn
utils.skip_player_spawn(p8)

# view the room
print(p8.game)

# hold right + x
p8.set_inputs(r=True, x=True)

# run for 10f while outputting player info
print(p8.game.get_player())
for f in range(20):
  p8.step()
  print(p8.game.get_player())
```

```
████████████████████        ████
██████████████████           <██
██████vvvvvvvv               <██
████>                           
██>                             
                                
                                
                                
                  ()      ()    
                                
                                
        ʌʌ                      
        ██>                     
        ██>                     
        ██>     :D              
████████████████████████████████

[player] x: 64, y: 112, rem: {0.0000, 0.0000}, spd: {0.0000, 0.0000}
[player] x: 64, y: 112, rem: {0.0000, 0.0000}, spd: {5.0000, 0.0000}
[player] x: 64, y: 112, rem: {0.0000, 0.0000}, spd: {5.0000, 0.0000}
[player] x: 64, y: 112, rem: {0.0000, 0.0000}, spd: {5.0000, 0.0000}
[player] x: 70, y: 112, rem: {0.0000, 0.0000}, spd: {3.5000, 0.0000}
[player] x: 75, y: 112, rem: {-0.5000, 0.0000}, spd: {2.0000, 0.0000}
[player] x: 78, y: 112, rem: {-0.5000, 0.0000}, spd: {2.0000, 0.0000}
[player] x: 81, y: 112, rem: {-0.5000, 0.0000}, spd: {2.0000, 0.0000}
[player] x: 84, y: 112, rem: {-0.5000, 0.0000}, spd: {1.8500, 0.0000}
[player] x: 86, y: 112, rem: {0.3500, 0.0000}, spd: {1.7000, 0.0000}
[player] x: 89, y: 112, rem: {0.0500, 0.0000}, spd: {1.5500, 0.0000}
[player] x: 92, y: 112, rem: {-0.4000, 0.0000}, spd: {1.4000, 0.0000}
[player] x: 94, y: 112, rem: {0.0000, 0.0000}, spd: {1.2500, 0.0000}
[player] x: 96, y: 112, rem: {0.2500, 0.0000}, spd: {1.1000, 0.0000}
[player] x: 98, y: 112, rem: {0.3500, 0.0000}, spd: {1.0000, 0.0000}
[player] x: 100, y: 112, rem: {0.3500, 0.0000}, spd: {1.0000, 0.0000}
[player] x: 102, y: 112, rem: {0.3500, 0.0000}, spd: {1.0000, 0.0000}
[player] x: 104, y: 112, rem: {0.3500, 0.0000}, spd: {1.0000, 0.0000}
[player] x: 106, y: 112, rem: {0.3500, 0.0000}, spd: {1.0000, 0.0000}
[player] x: 108, y: 112, rem: {0.3500, 0.0000}, spd: {1.0000, 0.0000}
[player] x: 110, y: 112, rem: {0.3500, 0.0000}, spd: {1.0000, 0.0000}
```

# Searcheline
An iterative-deepening depth-first-search solver for Celeste Classic, built on Pyleste.

## Usage
To define and run a search problem:

1. Create a class which inherits from Searcheline
2. Override the following methods as needed:
    - `init_state(self)` **[REQUIRED]**
      - Initial state (list of game objects) to search from
      - e.g., load the room and place maddy in Searcheline's game instance (`self.p8.game`), return `self.p8.game.objects`
    - `allowable_actions(self, objs, player, h_movement, can_jump, can_dash)`
      - Get list of available inputs for a state, with the following checks already computed:
        - `h_movement`: `True` if horizontal movement/jumps available (player x speed <= 1)
        - `can_jump`: `True` if jump available (in grace frames, next to wall, didn't jump previous frame)
        - `can_dash`: `True` if dash available (dashes > 0)
      - **Default**: all actions
      - Override this to restrict inputs (e.g., only up-dashes, no directional movement when player's y < 50, etc.)
    - `h_cost(self, objs)`
      - Estimated number of steps to satisfy the goal condition
      - **Default**: infinity if `is_rip`, `exit_heuristic` otherwise (See below)
      - Override to change or include additional heuristics
      - `is_rip(self, objs)`
        - RIP conditions (situations not worth considering further)
        - **Default**: player dies
        - Override to change or include other rip conditions (e.g., don't consider cases where player's x > 64, etc.)
      - `exit_heuristic(self, player)`
        - Underestimated number of steps to exit off the top
        - **Default**: assumes player zips upward at a speed of 6 px/step
        - Override to specify a less conservative estimate (e.g., if exit will be off a jump, can use 3 px/step)
    - `is_goal(self, objs)`
      - Define goal conditions
      - **Default**: exited the level
      - Override to change goal conditions (e.g., reach certain coordinates with a dash available)
3. Instantiate the class, and call `instance.search(max_depth)`
    - Use optional argument `complete=True` to search up to `max_depth`, even if a solution has already been found

## Example - 2100m

Here we'll set up a search problem to solve 2100m. Specifically, we'll work with the assumption that the player will be dashing toward the spring, like in the following GIF:

<img src="https://celesteclassic.github.io/gifs/gifs/2100/1.gif">

First import some useful stuff:

```python
from Searcheline import Searcheline
import Carts.CelesteUtils as utils
import math
```

Create a class which inherits from Searcheline:

```python
class Search2100(Searcheline):
```

In this class, override `init_state(self)`. Because we're only considering the player dashing toward the spring, we can remove the balloons to speed things up. By default, Searcheline comes with its own PICO-8 instance with a Celeste instance loaded, `self.p8`. We can use CelesteUtils to load 2100m into this PICO-8 instance, suppress the balloons, and skip to after the player has spawned. The function should then return the Celeste instance's list of objects, `self.p8.game.objects`:

```python
  # initial state to search from
  def init_state(self):
    utils.load_room(self.p8, 20) # load 2100m
    utils.suppress_object(self.p8, self.p8.game.balloon) # don't consider balloons
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    return self.p8.game.objects
```

Again, assuming the player will dash toward the spring, we only need to consider the option of holding right, jumping while holding right, as well as dashing while holding up and right. To restrict the search to these inputs, we override `allowable_actions(self, objs, player, h_movement, can_jump, can_dash)`, where given a situation (specified by the list of objects), it should build and return a list of inputs to consider. We can make use of the `can_jump` and `can_dash` checks to only consider inputs when they're applicable:

```python
  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000010] # r
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b100110]) # u + r + x
    return actions
```

By default, Searcheline's exit heuristic assumes that the player zips straight up at a speed of 6 px/step, based on an upward dash moving you at most 6 px in a single step. With prior knowledge that, from how high up the spring is, the player will be exiting off of a spring bounce, we can use a tighter heuristic of the player zipping upward at a speed of 4 px/step. Having a better estimate of the number of steps to exit the level (*while strictly being an underestimate*), we can greatly reduce the search space by pruning situations that provably can't exit within the current search depth. This can be done by overriding `exit_heuristic(self)`:

```python
  # from the input restrictions, we won't exit off of a dash- the max y displacement is 4 px off the spring
  def exit_heuristic(self, player, exit_spd_y=4):
    return math.ceil((player.y + 4) / exit_spd_y)
```

And that's it! We can instantiate this search problem, and use `search(self, max_depth)` to run the search. In this example, we'll search up to a maximum depth of 40, and set the optional `complete` argument to `True`. This optional argument makes it exhaustively search until the maximum depth, as opposed to stopping at the earliest depth a solution was found at:

```python
# search up to depth 40 completely (i.e., don't stop after reaching the optimal depth)
s = Search2100()
solutions = s.search(40, complete=True)
```

```
searching...
depth 1...
  elapsed time: 0.00 [s]
depth 2...
  elapsed time: 0.00 [s]
depth 3...
  elapsed time: 0.00 [s]
depth 4...
  elapsed time: 0.00 [s]
depth 5...
  elapsed time: 0.00 [s]
depth 6...
  elapsed time: 0.00 [s]
depth 7...
  elapsed time: 0.00 [s]
depth 8...
  elapsed time: 0.00 [s]
depth 9...
  elapsed time: 0.00 [s]
depth 10...
  elapsed time: 0.00 [s]
depth 11...
  elapsed time: 0.00 [s]
depth 12...
  elapsed time: 0.00 [s]
depth 13...
  elapsed time: 0.00 [s]
depth 14...
  elapsed time: 0.00 [s]
depth 15...
  elapsed time: 0.00 [s]
depth 16...
  elapsed time: 0.00 [s]
depth 17...
  elapsed time: 0.01 [s]
depth 18...
  elapsed time: 0.02 [s]
depth 19...
  elapsed time: 0.04 [s]
depth 20...
  elapsed time: 0.08 [s]
depth 21...
  elapsed time: 0.13 [s]
depth 22...
  elapsed time: 0.19 [s]
depth 23...
  elapsed time: 0.27 [s]
depth 24...
  elapsed time: 0.37 [s]
depth 25...
  elapsed time: 0.48 [s]
depth 26...
  elapsed time: 0.62 [s]
depth 27...
  elapsed time: 0.78 [s]
depth 28...
  elapsed time: 0.97 [s]
depth 29...
  elapsed time: 1.17 [s]
depth 30...
  elapsed time: 1.41 [s]
depth 31...
  elapsed time: 1.67 [s]
depth 32...
  elapsed time: 1.97 [s]
depth 33...
  elapsed time: 2.32 [s]
depth 34...
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
  frames: 33
  elapsed time: 2.69 [s]
depth 35...
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
  frames: 34
  inputs: [2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
  frames: 34
  elapsed time: 3.08 [s]
depth 36...
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0]
  frames: 35
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0]
  frames: 35
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0]
  frames: 35
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0]
  frames: 35
  elapsed time: 3.48 [s]
depth 37...
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0]
  frames: 36
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0]
  frames: 36
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0]
  frames: 36
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0]
  frames: 36
  inputs: [2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0]
  frames: 36
  inputs: [2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0]
  frames: 36
  inputs: [2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0]
  frames: 36
  inputs: [2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0]
  frames: 36
  elapsed time: 3.88 [s]
depth 38...
  elapsed time: 4.32 [s]
depth 39...
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 18, 2, 2, 2]
  frames: 38
  elapsed time: 4.74 [s]
depth 40...
  inputs: [2, 2, 2, 2, 2, 2, 18, 2, 2, 2, 2, 38, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 18, 2, 2, 2]
  frames: 39
  elapsed time: 5.16 [s]
```

Note that the frame counts are one less than the search depth (i.e., the number of inputs)- this is due to the first input being a *buffered* input. For readability, we can use `inputs_to_english(self, inputs)` to see the shortest solution in english:

```python
# translate fastest solution to english and print
print(f"inputs: {s.inputs_to_english(solutions[0])}")
```

```
inputs: right, right, right, right, right, right, jump right, right, right, right, right, right, right, right, up-right dash, no input, no input, no input, no input, no input, no input, right, right, right, right, right, right, right, right, right, right, right, right, right
```

Of note, despite the assumption of dashing toward and bouncing off of the spring, the search managed to find solutions which don't use it! Recreating the depth 39 (38 frame) solution with a [TAS tool](https://github.com/CelesteClassic/UniversalClassicTas/), we see that it found a frame perfect [corner jump](https://celesteclassic.github.io/glossary/#cornerjump) to get around the spring:

<img src="https://i.imgur.com/ZY8Gktp.gif">