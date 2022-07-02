from distutils.log import error
from logging import exception
import pygame
import math
import sys
from network import Network

pygame.font.init()

win = pygame.display.set_mode((500, 500))
(width, height) = pygame.display.get_window_size()
pygame.display.set_caption("client")

red = (240, 20, 20)
blue = (20, 20, 240)
white = (255, 255, 255)
transparent = (1, 1, 1)

max_speed = 10
rocket_speed = 15

rockets = pygame.sprite.Group()

class Rocket(pygame.sprite.Sprite):
  def __init__(self, diameter, spawn_pos, angle, player):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface([diameter, diameter])
    self.image.fill(transparent)
    self.image.set_colorkey(transparent)
    pygame.draw.circle(self.image, (0, 0, 0), (diameter // 2, diameter // 2), diameter // 2)
    self.rect = self.image.get_rect()
    self.rect.center = spawn_pos
    self.player = player

    self.speed = [rocket_speed * math.cos(angle), rocket_speed * math.sin(angle)]

  def update(self):
    self.rect = self.rect.move(self.speed)
    if self.rect.center[0] <= 0 or self.rect.center[0] >= width or self.rect.center[1] <= 0 or self.rect.center[1] >= height:
      rockets.remove(self)

class Scout(pygame.sprite.Sprite):
  def __init__(self, s_width, s_height, player):
    pygame.sprite.Sprite.__init__(self)
    
    self.airborne = False
    self.num_jumps = 2
    self.speed = [0, 0]

    self.player = player

    # if player == 0:
    self.color = red
    self.position = ((1 * width) / 4, height - (s_height / 2))

    if player == 1:
      self.color = blue
      self.position = ((3 * width) / 4, height - (s_height / 2))

    # set the image to 's_width' x 's_height' rectangle of 'color' color
    self.image = pygame.Surface([s_width, s_height])
    self.image.fill(self.color)

    self.rect = self.image.get_rect() # make object have same dimensions as the image
    self.rect.center = self.position

  def movement(self):
    key = pygame.key.get_pressed()

    # air speed
    if self.airborne:
      if key[pygame.K_a] and self.speed[0] > -max_speed and self.rect.left > 0:
        self.speed[0] -= 1
      if key[pygame.K_d] and self.speed[0] < max_speed and self.rect.right < width:
        self.speed[0] += 1
      
      self.speed[1] += 2 # gravity
      
    else:
      if key[pygame.K_a] != key[pygame.K_d]:
        if key[pygame.K_a] and self.rect.left > 0:
          self.speed[0] = -max_speed
        elif key[pygame.K_d] and self.rect.right < width:
          self.speed[0] = max_speed
      else:
        self.speed[0] *= 0.75 # friction

      # stop gravity
      self.speed[1] = 0
      self.rect.bottom = height
      self.num_jumps = 2
    
    if self.rect.left < 0:
      self.rect.left = 0
      self.speed[0] = 0
    if self.rect.right > width:
      self.rect.right = width
      self.speed[0] = 0
    
  def jump(self):
    if (self.num_jumps > 0):
      key = pygame.key.get_pressed()
      if key[pygame.K_a] != key[pygame.K_d]:
        if key[pygame.K_a] and self.rect.left > 0:
          self.speed[0] = -max_speed
        elif key[pygame.K_d] and self.rect.right < width:
          self.speed[0] = max_speed
      else:
        self.speed[0] = 0 # neutral jump
      self.rect = self.rect.move([0, -1])
      self.speed[1] = -20
      self.num_jumps -= 1

  def shoot(self):
    mouse_pos = pygame.mouse.get_pos()
    shot_tuple = (mouse_pos[0] - self.rect.center[0], mouse_pos[1] - self.rect.center[1])
    rocket = Rocket(8, self.rect.center, math.atan2(shot_tuple[1], shot_tuple[0]), self.player)
    rockets.add(rocket)
    return rocket

  def update(self):
    self.airborne = self.rect.bottom < height
    self.movement()
    # TODO: rocket interaction

    self.rect = self.rect.move(self.speed)

players = (pygame.sprite.Group(), pygame.sprite.Group())
player_0 = Scout(50, 50, 0)
players[0].add(player_0)
player_1 = Scout(50, 50, 1)
players[1].add(player_1)

def redraw_window(win, game, player):
  win.fill((255, 255, 255))
  
  if not game.connected():
    font = pygame.font.SysFont("monospace", 60)
    text = font.render("waiting for player...", 1, (0, 0, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
  else:
    players[0].draw(win)
    players[1].draw(win)
    rockets.draw(win)

    players[player].update()
    other_player = (player + 1) % 2
    players[other_player].sprites()[0].rect.center = game.p_pos[other_player]

    if game.is_new_rocket[other_player]: # somehow enters this twice, even though we only shoot once
      print("entered is new rocket check")
      new_pos = game.r_pos_speed[-1][0]
      new_speed = game.r_pos_speed[-1][1]
      new_rocket = Rocket(8, new_pos, math.atan2(new_speed[1], new_speed[0]), other_player)
      rockets.add(new_rocket)
      # game.is_new_rocket[other_player] = False

    for i in range(len(rockets)):
      print(f"game.r_pos_speed {len(game.r_pos_speed)}")
      print(f"i {i}")
      print(f"len(rockets) {len(rockets)}")
      rockets.sprites()[i].rect.center = game.r_pos_speed[i][0]

    print(f"game.r_pos_speed {len(game.r_pos_speed)}")
    print(f"len(rockets) {len(rockets)}")
    rockets.update()
  
  pygame.display.update()

def main():
  run = True
  clock = pygame.time.Clock()
  n = Network()
  player = int(n.get_p())
  print(f"You are player {player}.")

  while run:
    clock.tick(60)
    try:
      game = n.send(("move player", players[player].sprites()[0].rect.center)) # all data will be sent as ("action", actual data)
      rocket_positions = list()
      for rocket in rockets:
        rocket_positions.append(rocket.rect.center)
      n.send(("move rockets", rocket_positions))
      if len(game.r_pos_speed) > len(rockets):
        n.send("remove rocket")
    except:
      run = False
      print("Couldn't get game.")
      break
    
    redraw_window(win, game, player)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
      elif game.connected():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_w:
            players[player].sprites()[0].jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            new_rocket = players[player].sprites()[0].shoot()
            n.send(("shoot", [new_rocket.rect.center, new_rocket.speed]))

def menu_screen():
  run = True
  clock = pygame.time.Clock()
  
  while run:
    clock.tick(60)
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("monospace", 60)
    text = font.render("click to play", 1, (0, 0, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    pygame.display.update()

    for event in pygame.event.get():
      if event.type  == pygame.QUIT:
        pygame.quit()
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        run = False
  main()

while True:
  menu_screen()