import socket
from _thread import *
import pickle
from game import Game

server = "192.168.1.128"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.bind((server, port))
except socket.error as e:
  str(e)

s.listen()
print("Waiting for connection, server started")

connected = set()
games = {}
id_count = 0

def threaded_client(conn, p, game_id):
  global id_count
  conn.send(str.encode(str(p)))

  reply = ""
  while True:
    try:
      data = pickle.loads(conn.recv(2048))

      if game_id in games:
        game = games[game_id]
        
        if not data:
          break
        else:
          print(data[0])
          game.is_new_rocket[p] = False
          if data[0] == "move player":
            game.p_pos[p] = data[1]
          elif data[0] == "shoot":
            game.r_pos_speed.append(data[1])
            game.is_new_rocket[p] = True
          elif data[0] == "move rockets":
            for i in range(len(data[1])):
              game.r_pos_speed[i][0] = data[1][i]
          elif data == "remove rocket":
            game.r_pos_speed.pop(0)
          
          reply = game
          conn.sendall(pickle.dumps(reply))
      else:
        break
    except:
      break
  
  print("Lost connection")
  try:
    del games[game_id]
    print(f"Closing game:{game_id}")
  except:
    pass
  id_count -= 1
  conn.close()

while True:
  conn, addr = s.accept()
  print(f"Connected to:{addr}")

  id_count += 1
  p = 0
  game_id = (id_count - 1)//2
  if id_count % 2 == 1:
    games[game_id] = Game()
    print("Creating a new game.")
  else:
    games[game_id].ready = True
    p = 1

  start_new_thread(threaded_client, (conn, p, game_id))
