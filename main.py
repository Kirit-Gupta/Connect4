#CONNECT FOUR

#7 column, 6 rows
#counters dropped in column in turns
#when counter is dropped it will occupy the lowest point on the column
# four in a row can be vertical, horizontal or diagonal.
#If board is full then there is no winner
#minimax AI

from Code.Game import Game

game = Game()

game.main()