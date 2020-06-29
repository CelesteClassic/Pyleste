from Searcheline import Searcheline
import CelesteUtils as utils

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.load_room(self.p8, 0) # load 100m
    utils.suppress_object(self.p8, self.p8.game.fake_wall) # don't consider berry block
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    # execute this list of initial inputs
    for a in [18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
      self.p8.set_btn_state(a)
      self.p8.step()
    # alternatively, using output from a TAS tool:
    # utils.place_maddy(self.p8, 55, 79, 0.2, 0.185, 1.4, 0.63, 0, 0)
    return self.p8.game.objects

  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000010] # r
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b100010, 0b100100, 0b100110]) # r + x, u + x, u + r + x
    return actions

if __name__ == '__main__':
  # search up to depth 50, but stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(50)