if __name__ == '__main__':
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