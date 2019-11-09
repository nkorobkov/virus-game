# Virus Game 

This repo holds game engine for paper and pen game called "Virus War".   

### Game

The Virus War is a complete information strategic game between two players (similar to Chess and Go).
You can read complete rules of the game on the [wiki page](https://github.com/nkorobkov/virus-game/wiki/Rules)

The game usually played on the 9x9 square field. But game size can be changed bu changing field size. 
In a usual game number of legal moves for players fluctuates around 3K and can reach 15K for certain positions.
Such a huge branching factor makes the game difficult for classic minimax approaches.  

### Play with computer

Engine is writen in pure python and do not need any dependencies to run.  

You can play  with simple AI in command line by running 
```shell
git clone  https://github.com/nkorobkov/virus-game.git
python3 ./virus-game/Playground/play.py
```

More sophisticated AI engines and web UI will hopefully be added in the future!
