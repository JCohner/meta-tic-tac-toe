# Meta Tic Tac Toe
Name pending.

## Rules
Meta tic tic toe is essentially tic tac toe within tic tac toe. There are 4 key rules:
1. X starts and can choose any "mini board" to play in
2. From that point on the next player must play in mini board that corresponds to the square played in the previous miniboard
3. **If** a player sends another player to a board that is already won, the first player gets to choose any *not* won board to send their opponent to
4. The game is won when the miniboards make a tic tac toe on the major board

## How to run the software:
1. Clone this repo. 
2. Run the command: `make run`

### Prerequisites
1. You will for sure need `git make`
2. May need `python-virtualenv`
3. May need to edit the `Makefile` of this project if your `python` executable is *not* aliased to `python3`

## Video Of Gameplay
### Quick Win
https://github.com/JCohner/meta-tic-tac-toe/assets/19911908/03834c1b-caab-47bb-8ff1-1193e7927b90

### Sending Opponent To Other MiniBoards
https://github.com/JCohner/meta-tic-tac-toe/assets/19911908/8a64f14f-57f3-460e-855e-097ce45ba639

### Sending Opponent To Already Won Board
https://github.com/JCohner/meta-tic-tac-toe/assets/19911908/90cff67a-1338-45c9-9127-e7548540433b

### Meandering Gamplay
https://github.com/JCohner/meta-tic-tac-toe/assets/19911908/c0ea4872-75e6-4680-adb8-ae3d3c27b05f


