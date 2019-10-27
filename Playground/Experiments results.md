### MiniMaxGames

| Pair                             | Winner         | Score | Field Size |
|----------------------------------|----------------|-------|------------|
| ColoredCells 2 vs ColoredCells 1 | ColoredCells 2 | 2:0   | 9x9        |
|----------------------------------|----------------|-------|------------|
| ColoredCells 1 vs MovesCount 1   | MovesCount 1   | 0:2   | 9x9        |
| ColoredCells 1 vs MovesCount 1   | None           | 1:1   | 10x10      |
| ColoredCells 1 vs MovesCount 2   | MovesCount 2   | 0:2   | 9x9        |
| ColoredCells 2 vs MovesCount 1   | None           | 1:1   | 9x9        |
| ColoredCells 2 vs MovesCount 2   | ColoredCells 2 | 2:0   | 9x9        |
| ColoredCells 2 vs MovesCount 2   | ColoredCells 2 | 2:0   | 8x8        |

### Avg number of possible moves through game

It is  unclear how to sample big amount of reasonable games yet. 
For games with random policy   --> average number of available moves through first 20 moves of the game on 9x9 field is 3264
Table for number of available moves per move of the game looks like this:

0  --> 56.0  
1  --> 380.635  
2  --> 979.315  
3  --> 1765.72  
4  --> 2609.595  
5  --> 3371.01  
6  --> 4073.525  
7  --> 4638.59  
8  --> 5024.765  
9  --> 5148.385  
10  --> 5377.085  
11  --> 5304.645  
12  --> 5100.315  
13  --> 4683.115  
14  --> 4197.255  
15  --> 3655.635  
16  --> 3113.175  
17  --> 2499.69  
18  --> 1914.6  
19  --> 1388.93