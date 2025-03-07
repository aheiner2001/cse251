'''
Requirements
1. Create a recursive program that finds the solution path for each of the provided mazes.
2. COMMENT every line that you write yourself.
'''

import math
from screen import Screen
from maze import Maze
import cv2
import sys
from cse251functions import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


# this is the function that will be called recursively to solve the maze
# it will take in the maze object, the row and column of the current position, and the solution path
def path_solve_rec(maze, row, col, solution_path):
    if maze.at_end(row, col):
        return True

# find possible moves
    possible_moves = maze.get_possible_moves(row, col)

# loop through the possible moves and check if the maze can move to that position
    for r,c in possible_moves:
        print(r,c)
        # append the current position to the solution path
        solution_path.append((r, c))
        

        if maze.can_move_here(r, c):
            maze.move(r, c, COLOR)
        
        

        # recursively call the function to check if the maze can move to the next position
        if path_solve_rec(maze, r, c, solution_path):
            return True
        # remoove from the solution path if the maze cannot move to the next position, and restore
        solution_path.remove((r,c))
        maze.restore(r, c)
    return False


def solve(maze):
    """ Solve the maze. The path object should be a list (x, y) of the positions 
        that solves the maze, from the start position to the end position. """

  

# get the start position of the maze
    row, col = maze.get_start_pos()
    # check if the maze is at the end
    if maze.at_end(row, col):
        return True


# move the maze to the start position
    print(row, col)
    maze.move(row, col, COLOR)
    solution_path = [] 
# start the recursive process
    path_solve_rec(maze, row, col, solution_path)

   
        

 



    


    
    # Remember that an object is passed by reference, so you can pass in the 
    # solution_path object, modify it, and you won't need to return it from 
    # your recursion function
    
    return solution_path
    # return solve(maze) probably dont want to have this be recurise


def get_solution_path(filename):
    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    solution_path = solve(maze)

    print(f'Number of drawing commands for = {screen.get_command_count()}')
    print(solution_path)

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True

    return solution_path


def find_paths():
    files = ('verysmall.bmp',
             'verysmall-loops.bmp',
             'small.bmp', 'small-loops.bmp',
             'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    print('*' * 40)
    print('Part 1')
    for filename in files:
        print()
        print(f'File: {filename}')
        solution_path = get_solution_path(filename)
        print(f'Found path has length          = {len(solution_path)}')
    print('*' * 40)
   


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_paths()


if __name__ == "__main__":
    main()
    create_signature_file("CSE251W25")