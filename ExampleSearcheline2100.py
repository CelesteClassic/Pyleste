from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search2100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.load_room(self.p8, 20) # load 2100m
    utils.suppress_object(self.p8, self.p8.game.balloon) # don't consider balloons
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    return self.p8.game.objects

  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000010] # r
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b100110]) # u + r + x
    return actions

  # from the input restrictions, we won't exit off of a dash- the max y displacement is 4 px off the spring
  def exit_heuristic(self, player, exit_spd_y=4):
    return math.ceil((player.y + 4) / exit_spd_y)

if __name__ == '__main__':
  # search up to depth 40 completely (i.e., don't stop after reaching the optimal depth)
  s = Search2100()
  solutions = s.search(40, complete=True)

  # translate fastest solution to english and print
  print(f"inputs: {s.inputs_to_english(solutions[0])}")