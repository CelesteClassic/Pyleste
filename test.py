if __name__ == '__main__':
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