class Game:
  def __init__(self):
    self.ready = False
    self.id = id
    self.p_pos = [(0, 0), (0, 0)]
    self.r_pos_speed = list()
    self.is_new_rocket = [False, False]

  def connected(self):
    return self.ready