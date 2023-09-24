#Mars Frederick H. Songco
#2021 - 00586
#CMSC 170 - WX4L

from sre_parse import State
import pygame as pg
import copy
import ctypes

#colors definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (73, 108, 247)
GREEN = (53, 94, 59)

table = []

with open('puzzle.in','r') as file:
    for line in file:
        data = line.replace('\n', '').split(' ')
        toAppend = [int(x) for x in data]
        table.append(toAppend)

class Button():
    def __init__(self, value, loc, color):
        self.value = value
        self.loc = loc
        self.color = color

    def click_listener(self, cursor_XY):         #boolean value for if a tile has been clicked
        eval = self.loc[0] <= cursor_XY[0] <= self.loc[0] + 50 and self.loc[1] <= cursor_XY[1] <= self.loc[1] + 50
        return eval

class State_record:
    def __init__(self, puzzle, empty_loc, action, parent):
        self.puzzle = puzzle
        self.empty_loc = empty_loc
        self.action = action
        self.parent = parent

class Nums:
    def __init__(self, value, r, c, loc, color):
        self.value = value
        self.r = r
        self.c = c
        self.loc = loc
        self.color = color

    def click_listener(self, cursor_XY):         #boolean value for if a tile has been clicked
        eval = self.loc[0] <= cursor_XY[0] <= self.loc[0] + 50 and self.loc[1] <= cursor_XY[1] <= self.loc[1] + 50
        return eval

def win_condition(array):     # determines if winning condition has been met
    win_table = [[1, 2, 3],[4, 5, 6], [7, 8, 0]]
    eval = array == win_table
    return eval

def movable(num, table):     #for squares that have an adjacent zero
    while True:
        if num.c - 1 >= 0: #zero is in the left
            if table[num.r][num.c - 1] == 0: #swaps values of the squares
                square = table[num.r][num.c]
                table[num.r][num.c] = table[num.r][num.c - 1]
                table[num.r][num.c - 1] = square
                break
        if num.c + 1 <= 2: #checks if we haven't passed-by the last column na
            if table[num.r][num.c + 1] == 0: #zero is in the right
                square = table[num.r][num.c]
                table[num.r][num.c] = table[num.r][num.c + 1]
                table[num.r][num.c + 1] = square
                break
        if num.r - 1 >= 0: #checks if we haven't passed-by the last row na
            if table[num.r - 1][num.c] == 0:
                square = table[num.r][num.c]
                table[num.r][num.c] = table[num.r - 1][num.c]
                table[num.r - 1][num.c] = square
                break
        if num.r + 1 <= 2:
            if table[num.r + 1][num.c] == 0:   
                square = table[num.r][num.c]
                table[num.r][num.c] = table[num.r + 1][num.c]
                table[num.r + 1][num.c] = square
                break
        break

def get_inv_count(arr): #checks if the puzzle is solvable  (source: https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/)
    inv_count = 0
    empty_value = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]: # Count pairs (i, j) such that i appears before j, but i > j
                inv_count += 1
    return inv_count

#gets all possible moves
def actions(currentState):
    table = currentState.puzzle
    moveset = []
    coords = findZero(table)
    if(coords[0] > 0):
        moveset.append('U')
    if(coords[1] < 2):
        moveset.append('R')
    if(coords[0] < 2):
        moveset.append('D')
    if(coords[1] > 0):
        moveset.append('L')
    return moveset

#for debugging
def printTable(table):
    for r in table:
        print(r)

#updating the table list for every action
def result(parent, action):
    table = parent.puzzle
    coords = findZero(table)
    if action == 'U':
        temp =  table[coords[0] - 1][coords[1]]
        table[coords[0]][coords[1]] = temp
        table[coords[0] - 1][coords[1]] = 0
    elif action == 'D':
        temp =  table[coords[0] + 1][coords[1]]
        table[coords[0]][coords[1]] = temp
        table[coords[0] + 1][coords[1]] = 0
    elif action == 'L':
        temp =  table[coords[0]][coords[1]-1]
        table[coords[0]][coords[1]] = temp
        table[coords[0]][coords[1] - 1] = 0
    elif action == 'R':
        temp =  table[coords[0]][coords[1]+1]
        table[coords[0]][coords[1]] = temp
        table[coords[0]][coords[1] + 1] = 0
    return(State_record(table, findZero(table), action, parent))


def findZero(table):
    for r in range(len(table)):
        for c in range(len(table)):
            if table[r][c] == 0:
                return r,c

def BFSearch(table):
    print("BFS")
    initial = State_record(table, findZero(table), '', None)
    frontier = [] #queue
    explored = [] #queue
    frontier.append(initial)
    while(len(frontier) > 0):
        currentState = frontier.pop(0)
        explored.append(currentState.puzzle)
        if(win_condition(currentState.puzzle)):
            print(currentState.puzzle)
            print(currentState)
            print(len(explored))
            return currentState
        else:
            actionset = actions(currentState)
            for action in actionset:
                editable = copy.deepcopy(currentState) #we create a copy of the object itself
                afterAction = result(editable, action)
                if((afterAction not in frontier) and (afterAction.puzzle not in explored)):
                    frontier.append(afterAction)

def DFSearch(table):
    print("DFS")
    initial = State_record(table, findZero(table), '', None)
    frontier = [] #stack
    explored = [] #stack
    frontier.append(initial)
    while(len(frontier) > 0):
        currentState = frontier.pop()
        explored.append(currentState.puzzle)
        print(currentState.puzzle)
        if(win_condition(currentState.puzzle)):
            print(currentState.puzzle)
            print(currentState)
            print(len(explored))
            return currentState
        else:
            actionset = actions(currentState)
            for action in actionset:
                editable = copy.deepcopy(currentState) #we create a copy of the object itself
                afterAction = result(editable, action)
                if((afterAction not in frontier) and (afterAction.puzzle not in explored)):
                    frontier.append(afterAction)

def solveIt(nums, table, move):
    zero_coords = findZero(table)
    coords_trans = (zero_coords[0]*3) + zero_coords[1] #we transalate the coordinates of zero since nums_array is a 1D array
    if move == 'U':
        movable(nums[coords_trans-3], table)
    elif move == 'R':
        movable(nums[coords_trans+1], table)
    elif move == 'D':
        movable(nums[coords_trans+3], table)
    elif move == 'L':
        movable(nums[coords_trans-1], table)
    else:
        print("error")
	

def traceback(puzzleState):
    moves = []
    ptr = puzzleState
    while(ptr is not None):
        print(ptr.action, ptr, ptr.parent)
        moves.append(ptr.action)
        ptr = ptr.parent

    return(moves[::-1])

done = False

move_index = 0                    

solution = []

pg.init()

text_font = pg.font.SysFont('bahnschrift', 25)

window = pg.display.set_mode((650, 450))

commence = True

while commence:
    window.fill(WHITE)

    for event in pg.event.get(): 
        if event.type == pg.QUIT: #user closes the window
            commence = False
        elif event.type == pg.MOUSEBUTTONUP and not win_condition(table): #winning condition has not been met yet and user clicks on a square
            pos = pg.mouse.get_pos()
            for tile in nums_array: #listen for a tile click
                if tile.click_listener(pos):
                    movable(tile, table) #move the tile if it has a zero adjacent to it
                    win_condition(table)  #check if the puzzle is already solved
            if bfs_button.click_listener(pos):
                solution = traceback(BFSearch(table))
                solution.pop(0)
                print(solution)
                f = open("puzzle.out", "w")
                f.write(', '.join(solution))
                f.close()
            if dfs_button.click_listener(pos):
                solution = traceback(DFSearch(table))
                solution.pop(0)
                print(solution)
                f = open("puzzle.out", "w")
                f.write(', '.join(solution))
                f.close()
            if next_button.click_listener(pos):
                solveIt(nums_array, table, solution[move_index])
                move_index = move_index + 1
            

    if not win_condition(table):#check if the puzzle is solvable
        inv_count = get_inv_count([j for sub in table for j in sub])
        if inv_count == 0 or inv_count % 2 == 0:
            t_solvable_text = "Solvable!"
        else:
            t_solvable_text = "Not Solvable!"
        t_solvable = text_font.render(t_solvable_text, 1, BLACK)
    else: #means puzzle is already solved
        t_solvable = text_font.render("Solved!", 1, BLACK)

    if len(solution) > 0 and move_index < len(solution): 
        pg.draw.rect(window, next_button.color, (next_button.loc[0], next_button.loc[1], 100, 100))
        window.blit(text_font.render("Next", 1, WHITE), (400, 300))

    if move_index >= len(solution) and len(solution) > 0:
        window.blit(text_font.render(f'Path cost: {len(solution)}', 1, BLACK), (300, 400))

    window.blit(t_solvable, (60, 250))
    window.blit(text_font.render(', '.join(solution), 1, BLACK), (300, 250))
    #update tile values
    nums_array = []

    for i in range(3):
        for j in range(3):
            nums_array.append(Nums(table[i][j], i, j, (50 + 55 * j, 50 + 55 * i), GREEN if table[i][j] == 0 else BLUE))

    text_array = [text_font.render(str(nums.value), 1, WHITE) if nums.value != 0 else None for nums in nums_array] # Render and re-render the values of each tile
    bfs_text = text_font.render("BFS", 1, WHITE)
    bfs_button = Button(bfs_text, (60, 300), BLUE)
    dfs_button = Button(text_font.render("DFS", 1, WHITE), (200, 300), BLUE)
    next_button = Button(text_font.render("Next", 1, WHITE), (400, 300), BLUE)
 

    #draw bfs button
    pg.draw.rect(window, bfs_button.color, (bfs_button.loc[0], bfs_button.loc[1], 100, 100))
    window.blit(bfs_text, (60, 300))
    pg.draw.rect(window, dfs_button.color, (dfs_button.loc[0], dfs_button.loc[1], 100, 100))
    window.blit(text_font.render("DFS", 1, BLACK), (200, 300))

    # Draw and re-draw nums

    for nums, text in zip(nums_array, text_array): #render tile
        if nums.value != 0: #draw tile only if not zero
            pg.draw.rect(window, nums.color, (nums.loc[0], nums.loc[1], 50, 50))
            if text:
                window.blit(text, (nums.loc[0], nums.loc[1]))


    pg.display.update()

pg.quit()