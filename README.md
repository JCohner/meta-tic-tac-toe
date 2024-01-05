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
![quickwin](https://github.com/JCohner/meta-tic-tac-toe/assets/19911908/449ab87f-c023-4031-a570-670c12499260)
### More Representative
![gameplay](https://github.com/JCohner/meta-tic-tac-toe/assets/19911908/d188a9d2-8386-459d-88e9-1981f120d7b0)


