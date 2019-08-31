# Zigsaw-Puzzle-solver
A program which solves any jigsaw puzzle with the help of Computer Vision technique.  
1.py - creates the puzzle - given a image. Just set nx and ny inside code. these are number of pieces you want on x-axis and y-axis respectively.  
2d.py - solves the puzzle. It takes the puzzle (set of images as formed by 1.py) as input and apply max edge matching method to match the pieces. It outputs the result after every piece added so that each one can analyse the output step by step.   
Assumption - puzzle's pieces given to 2d.py as input are not rotated. That is, a given piece can come in final output at any place but without any rotation of angle(90/180/270/360 degrees).  
  
Algorithm:  
***to be explained***  
  
There is a threshold in 2d.py. If while running 2d.py got an error: list index out of range, increase the threshold. For better result, keep threshold as low as possible.
