import copy
import time

class succesor:
  def __init__(self,board,g,h,parent):
    self.board = copy.deepcopy(board)
    self.g = g
    self.h = h
    self.parent = parent
  
  def getCost(self):
    return self.g + self.h
  
  def getBoard(self):
    return self.board
  
  def isGoal(self):
    if(self.h==0):
      return True
    else:
      return False
  
  def getParent(self):
    return self.parent


def calculateManhattan(board,goal,dimension):
  total_distance = 0
  for i in range(dimension):
    for j in range(dimension):
      entity = board[i][j]
      if(entity == "_"):
        continue
      entity = int(entity)
      (target_row,target_column) = findEntity(entity,goal,dimension)
      distance = abs(i-target_row) + abs(j-target_column)
      total_distance += distance
  return total_distance

def findEntity(target, board, dimension):
  for i in range(dimension):
    for j in range(dimension):
      entity = board[i][j] 
      if(entity=="_" and target == "_"):
        return (i,j)
      elif(entity=="_"):
        continue
      if(int(entity)==target):
        return (i,j)

def ASearch(dimension,board,goal,max_cost):
  board_obj = succesor(board,0,calculateManhattan(board,goal,dimension,),-1)
  open_list = [board_obj]
  close_list = []
  step = 1
  found = False
  goal_state = -1
  while(len(open_list)):
    if(found):
      break
    board_obj = open_list[0]
    open_list = open_list[1:]
    if(board_obj.getCost()>max_cost):
      continue
    successors = findSuccesors(board_obj, goal,step, dimension) # List of successor objects
    for i in range(len(successors)):
      if(successors[i].isGoal()):
        found = True
        goal_state = copy.deepcopy(successors[i])
        break
      isIn = False
      # Search for open list
      for j in range(len(open_list)):
        if(successors[i].getBoard() == open_list[j]):
          isIn = True
          break
      if(isIn and successors[i].getCost() > open_list[j].getCost()):
        continue
      isIn = False
      # Search for close list
      for j in range(len(close_list)):
        if(successors[i].getBoard() == close_list[j]):
          isIn = True
          break
      if(isIn and successors[i].getCost() > close_list[j].getCost()):
        continue
      # Add this successor to open list
      open_list.append(copy.deepcopy(successors[i]))
    #After all successors processed sort open list and push this state to close list
    open_list.sort(key=lambda tup: tup.getCost())
    step += 1
  solution_stack = []
  if(goal_state == -1):
    print("FAILURE")
    return
  while(goal_state.getParent() != -1):
    solution_stack.append(goal_state.getBoard())
    goal_state = goal_state.getParent()
  solution_stack.append(goal_state.getBoard())
  solution_stack = solution_stack[::-1]
  print("SUCCESS\n")
  for i in range(len(solution_stack)):
    printBoard(solution_stack[i],dimension)
    if(i!=len(solution_stack)-1):
      print("\n")

def printBoard(board,dimension):
  for i in range(dimension):
    for j in range(dimension):
      print(str(board[i][j]), end = ' ')
    if(i != dimension-1):
      print()

def findSuccesors(board,goal,step,dimension):
  blank = findEntity("_", board.getBoard(), dimension)
  succesors = []
  if(blank[0] != dimension-1): #Blank tile is not at the bottom of the board
    res_board = findUp(board.getBoard(),blank,goal)
    res_successor = succesor(res_board,step,calculateManhattan(res_board,goal,dimension),board)
    succesors.append(res_successor)
  if(blank[0] != 0): #Blank tile is not at the top of the board
    res_board = findDown(board.getBoard(),blank,goal)
    res_successor = succesor(res_board,step,calculateManhattan(res_board,goal,dimension),board)
    succesors.append(res_successor)
  if(blank[1] != dimension-1): #Blank tile is not at the right of the board
    res_board = findLeft(board.getBoard(),blank,goal)
    res_successor = succesor(res_board,step,calculateManhattan(res_board,goal,dimension),board)
    succesors.append(res_successor)
  if(blank[1] != 0): #Blank tile is not at the left of the board
    res_board = findRight(board.getBoard(),blank,goal)
    res_successor = succesor(res_board,step,calculateManhattan(res_board,goal,dimension),board)
    succesors.append(res_successor)
  return succesors

def findUp(board,blank,goal):
  succesor = copy.deepcopy(board)
  succesor[blank[0]][blank[1]] = board[blank[0]+1][blank[1]]
  succesor[blank[0]+1][blank[1]] = board[blank[0]][blank[1]]
  return succesor

def findDown(board,blank,goal):
  succesor = copy.deepcopy(board)
  succesor[blank[0]][blank[1]] = board[blank[0]-1][blank[1]]
  succesor[blank[0]-1][blank[1]] = board[blank[0]][blank[1]]
  return succesor

def findLeft(board,blank,goal):
  succesor = copy.deepcopy(board)
  succesor[blank[0]][blank[1]] = board[blank[0]][blank[1]+1]
  succesor[blank[0]][blank[1]+1] = board[blank[0]][blank[1]]
  return succesor

def findRight(board,blank,goal):
  succesor = copy.deepcopy(board)
  succesor[blank[0]][blank[1]] = board[blank[0]][blank[1]-1]
  succesor[blank[0]][blank[1]-1] = board[blank[0]][blank[1]]
  return succesor

def getInput():
  algorithm = input()
  max_cost = int(input())
  dimension = int(input())
  board = [[0 for i in range(dimension)] for i in range(dimension)]
  goal = [[0 for i in range(dimension)] for i in range(dimension)]
  for i in range(dimension):
    row = input().split(" ")
    for j in range(dimension):
      board[i][j] = row[j]
  for i in range(dimension):
    row = input().split(" ")
    for j in range(dimension):
      goal[i][j] = row[j]
  return(algorithm,max_cost,dimension,board,goal)

def main():
  (algorithm,max_cost,dimension,board,goal) = getInput()
  if(algorithm == "A*"):
    ASearch(dimension,board,goal,max_cost)
  else:
    return 0

if __name__ == "__main__":
  main()


