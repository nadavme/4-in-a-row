# 4-in-a-row
##                      Description:                       ##


In this exercise we used object oriented programming to create the classic
game "Four In A Row". The game uses three main classes:

### Game ### 

Handles the logic of the game. Determines the state of the board and
whether one of the players has won. This class an integral part of the program
that acts as a "puppet master" for the GUI.


### Four in a row ### 
The main program that runs the game and handles the graphic
user interface. The order of the commands is important for the smooth execution
of the game. The two players must have the same board status at all times for
them to be able to play. In addition, the GUI manages the input in a way that
enables only the current player to make a move. It was easy to achieve this
with humans, a bit harder to get consistent results with A.I.

### A.i. ### 
In this short class defined how the "computer"  decides on a move.
We chose to implement the naive random solution.

From the beginning we chose to go with a minimalistic design theme. We chose to
prioritize intuitiveness and clearness. We tried to make a game that wouldn't
compromise on these two values while still being pleasing to the eye.
Rather than adding many textures and pictures that might make it hard to focus
on the game itself, we chose to go with a bare bones approach that takes some
inspiration from operating systems such as mac OS and android.

## Dilemmas ##

Initially, we created the whole game without using a class for the GUI.
Only later, when we arrived at the communication part we decided to convert the
code to a class. Before this adaptation the code was a mess, and it was hard to
implement simple changes since every function needed to receive many more
arguments, and only in order to send them to other functions. using Classes
helped us manage changes easily, detect bugs and fix them swiftly and
effectively.

Another issue that we were ambivalent about, was to decide which class was to
be the main class: Should the GUI use the game or should it be the other way
around? Finally, we decided to run things from the GUI, and use the game
for the specific actions of making a move, and checking for a win.
