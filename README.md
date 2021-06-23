# Virus Game 

This repo holds game engine for paper and pen game called "Virus War".   

You can explore the game and play it with your friends or with one of the ai engines from this repo on the deployed frontend at
https://virusvar.nkorobkov.com
(if it still works by the time you find the link)

[![Build Status](https://travis-ci.org/nkorobkov/virus-game.svg?branch=master)](https://travis-ci.org/nkorobkov/virus-game)

### Game

The Virus War is a complete information strategic game between two players (similar to Chess and Go).
You can read complete rules of the game on the [project page](https://nkorobkov.github.io/projects/virus)

The game usually played on the 8x8 square field. But game size can be changed bu changing field size. 
In a usual game number of legal moves for players fluctuates around 3K and can reach 15K for certain positions.
Such a huge branching factor makes the game difficult for classic minimax approaches.  

### Play with computer localy

Engine is writen in pure python and do not need any dependencies to run.  

You can play  with simple AI in command line by running 
```shell
git clone  https://github.com/nkorobkov/virus-game.git
python3 ./virus-game/Playground/play.py
```

More sophisticated AI engines and web UI will hopefully be added in the future!
