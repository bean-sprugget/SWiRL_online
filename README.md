# SWiRL online

## Overview

SWiRL stands for Scouts With Rocket Launchers. Currently it is not complete and barely works. The idea was: it is a 2D game with two players that can move around and double jump (hence the "Scout", from Team Fortress 2), platformer-style. They would then shoot rockets at each other (hence the "Rocket Launchers", also from Team Fortress 2). If their opponent was grounded, it would launch them in the air; if they were airborne, it would kill them. Currently, all that's implemented is moving around and double jumping, which syncs between clients. Trying to shoot with left click crashes the game.

## Installation and Running

Install the entire file. I suppose if you are not running the server you shouldn't have to install `server.py`. Ideally I would like to just have an executable and somehow be able to have the user set up the IP and port and whatnot. But currently, you have to go into `network.py` and `server.py`, and near the top of each file, change `self.server = 192.168.1.128` and `server = "192.168.1.128"` respectively. See below:

![image](https://user-images.githubusercontent.com/63476667/176989474-93801092-ebd3-4229-8c87-f59574c3c746.png)
![image](https://user-images.githubusercontent.com/63476667/176989478-59d354c7-8298-4aae-b2e8-256353edcbff.png)


After the assignment operator `=` change the IP address to your own wifi IP. You can find this by opening Command Prompt and typing `ipconfig`. I'm PRETTY SURE (but I have not tested with multiple computers nor on other networks) that you should select the one under "Wireless LAN adapter Wi-Fi" and then the one after "IPv4 Address" (basically, if you are on the same connection as the other computer you should be able to play together). See below:

![image](https://user-images.githubusercontent.com/63476667/176989450-e4803bc3-b123-460f-bec6-62799ad27c8a.png)

Install the modules as specified in `requirements.txt` (it's just `pygame`). You can do `pip install [module name]` or `pip3 install [module name]`.

Now, have one computer run `server.py` and have each computer run `client.py` (eg in PowerShell do `python [file]`). Now you should be able to play:

![2022-07-02 01-45-01](https://user-images.githubusercontent.com/63476667/176990018-306b1274-d69a-46a9-be19-596a521e344d.gif)

## Other

A lot of credit to TechWithTim and FreeCodeCamp for this video tutorial on the online aspect (https://www.youtube.com/watch?v=McoDjOCb2Zo) which I basically took a lot of code from.
