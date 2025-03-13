'''
Requirements
1. Create a recursive, multithreaded program that finds the exit of each maze.
2. COMMENT every line that you write yourself.
   
Questions:
1. It is not required to save the solution path of each maze, but what would
   be your strategy if you needed to do so?
   >
   >
2. Is using threads to solve the maze a depth-first search (DFS) or breadth-first search (BFS)?
   Which search is "better" in your opinion? You might need to define better. 
   (see https://stackoverflow.com/questions/20192445/which-procedure-we-can-use-for-maze-exploration-bfs-or-dfs)
   >
   >It seems to be breadth-first search (BFS) because it is exploring all possible paths at the same time.
    >BFS is better because it is faster and more efficient than DFS
'''

import math
import threading
from screen import Screen
from maze import Maze
import sys
import cv2
from cse251functions import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (72, 61, 139),
    (143, 143, 188),
    (226, 138, 43),
    (128, 114, 250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False


def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def path_solve_rec(maze, row, col, color):
    # check if maze is at end
    if maze.at_end(row, col):
        return True
    
    # define the color from the passed in color, this will be the starting color
    color = color
    # get the possible moves from current position
    possible_moves = maze.get_possible_moves(row, col)
 
#  loop throughj possible_moves anad check if the current position can be moved to the possible moves
    for r,c in possible_moves:
        print(f"possible moves for{row, col}{r},{c}")

        # if maze can move to the possible moves, move to the possible moves
        if maze.can_move_here(r, c):
            maze.move(r, c, color)
        
        
        # check if the maze is at the end
        if maze.at_end(r, c):
            
            return True
        if threading.Thread(target=path_solve_rec, args=(maze, r, c, color)).start():
            
            return True

        color = get_color()
        
        
    return False


def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    # TODO - add code here


    # find the start position
    row, col = maze.get_start_pos()

    # check if the start position is the end position
    if maze.at_end(row, col):
        return True


# print to the start postion to make sure it's working
    print(row, col)
    # color first position
    maze.move(row, col, COLOR)
    # solve the rest of the maze using recursion

    path_solve_rec(maze, row, col, COLOR)

   
        

 



    






    # change color to go left
    


def find_end(filename, delay):

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    print(f'Number of drawing commands = {screen.get_command_count()}')
    print(f'Number of threads created  = {thread_count}')

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


def find_ends():
    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    print('*' * 40)
    print('Part 2')
    for filename, delay in files:
        print()
        print(f'File: {filename}')
        find_end(filename, delay)
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_ends()


if __name__ == "__main__":
    main()
    create_signature_file("CSE251W25")
