# Skeleton Program for the AQA AS Summer 2022 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in a Python 3 environment

# Version number: 0.0.0

import random

EMPTY_STRING = ""
SPACE = ' '
GRID_SIZE = 9 

def ResetDataStructures():
  Puzzle = [EMPTY_STRING for Line in range(GRID_SIZE * GRID_SIZE)]
  PuzzleGrid = [[SPACE for Column in range(GRID_SIZE + 1)] for Row in range(GRID_SIZE + 1)]
  Solution = [EMPTY_STRING for Line in range(GRID_SIZE + 1)]
  Answer = [EMPTY_STRING for Line in range(2 * GRID_SIZE * GRID_SIZE)]
  return PuzzleGrid, Puzzle, Answer, Solution

def LoadPuzzleFile(PuzzleName, Puzzle):
  try:
    Line = 0
    FileIn = open(f"{PuzzleName}.txt", 'r')
    CellInfo = FileIn.readline()
    CellInfo = CellInfo[:-1]
    while CellInfo != EMPTY_STRING:
      Puzzle[Line] = CellInfo
      CellInfo = FileIn.readline()
      CellInfo = CellInfo[:-1]
      Line += 1
    FileIn.close()
    if Line == 0:
      print("Puzzle file empty")
      OK = False
    else:
      OK = True
  except:
    print("Puzzle file does not exist")
    OK = False
  return Puzzle, OK

def LoadSolution(PuzzleName, Solution):
  OK = True
  try:
    FileIn = open(f"{PuzzleName}S.txt", 'r')
    for Line in range(1, GRID_SIZE + 1):
      Solution[Line] = SPACE + FileIn.readline()
      Solution[Line] = Solution[Line][:-1]
      if len(Solution[Line]) != GRID_SIZE + 1:
        OK = False
        print("File data error")
    FileIn.close()  
  except:
    print("Solution file does not exist")
    OK = False
  return Solution, OK

def ResetAnswer(PuzzleName, Answer):
  Answer[0] = PuzzleName
  Answer[1] = "0"
  Answer[2] = "0"
  for Line in range(3, 2 * GRID_SIZE * GRID_SIZE):
    Answer[Line] = EMPTY_STRING
  return Answer

def TransferPuzzleIntoGrid(PuzzleName, PuzzleGrid, Puzzle, Answer):
  OK = True
  try:
    Line = 0
    CellInfo = Puzzle[Line]
    while CellInfo != EMPTY_STRING:
      Row = int(CellInfo[0])
      Column = int(CellInfo[1])
      Digit = CellInfo[2]
      PuzzleGrid[Row][Column] = Digit
      Line += 1
      CellInfo = Puzzle[Line]
    PuzzleGrid[0][0] = 'X'
    Answer = ResetAnswer(PuzzleName, Answer)
  except:
    print("Error in puzzle file")
    OK = False
  return PuzzleGrid, Answer, OK

def LoadPuzzle(PuzzleGrid, Puzzle, Answer, Solution):
  PuzzleGrid, Puzzle, Answer, Solution = ResetDataStructures()
  PuzzleName = input("Enter puzzle name to load: ")
  Puzzle, OK = LoadPuzzleFile(PuzzleName, Puzzle)
  if OK:
    Solution, OK = LoadSolution(PuzzleName, Solution)
  if OK:
    PuzzleGrid, Answer, OK = TransferPuzzleIntoGrid(PuzzleName, PuzzleGrid, Puzzle, Answer)
  if not OK:
    PuzzleGrid, Puzzle, Answer, Solution = ResetDataStructures()
  return PuzzleGrid, Puzzle, Answer, Solution

def TransferAnswerIntoGrid(PuzzleGrid, Answer):
  for Line in range(3, int(Answer[2]) + 3):
    CellInfo = Answer[Line]
    Row = int(CellInfo[0])
    Column = int(CellInfo[1])
    Digit = CellInfo[2]
    PuzzleGrid[Row][Column] = Digit
  return PuzzleGrid

def LoadPartSolvedPuzzle(PuzzleGrid, Puzzle, Answer, Solution):
  PuzzleGrid, Puzzle, Answer, Solution = LoadPuzzle(PuzzleGrid, Puzzle, Answer, Solution)
  try:
    PuzzleName = Answer[0]
    FileIn = open(f"{PuzzleName}P.txt", 'r')
    CellInfo = FileIn.readline()
    CellInfo = CellInfo[:-1]
    if PuzzleName != CellInfo:
      print("Partial solution file is corrupt")
    else:
      Line = 0
      while CellInfo != EMPTY_STRING:
        Answer[Line] = CellInfo
        Line += 1
        CellInfo = FileIn.readline()
        CellInfo = CellInfo[:-1]
    FileIn.close()
    PuzzleGrid = TransferAnswerIntoGrid(PuzzleGrid, Answer)
  except:
    print("Partial solution file does not exist")
  return PuzzleGrid, Puzzle, Answer, Solution

def DisplayGrid(PuzzleGrid):
  print()
  print("   1   2   3   4   5   6   7   8   9  ")
  print(" |===.===.===|===.===.===|===.===.===|")
  for Row in range(1, GRID_SIZE + 1):
    print(f"{Row}|", end='')    
    for Column in range(1, GRID_SIZE + 1):
      if Column % 3 == 0:
        print(f"{SPACE}{PuzzleGrid[Row][Column]}{SPACE}|", end='')
      else:
        print(f"{SPACE}{PuzzleGrid[Row][Column]}{SPACE}.", end='')
    print()
    if Row % 3 == 0:
      print(" |===.===.===|===.===.===|===.===.===|") 
    else:
      print(" |...........|...........|...........|")
  print()

def SolvePuzzle(PuzzleGrid, Puzzle, Answer):
  DisplayGrid(PuzzleGrid)
  if PuzzleGrid[0][0] != 'X':
    print("No puzzle loaded")
  else:
    print("Enter row column digit: ")
    print("(Press Enter to stop)")
    CellInfo = input()
    while CellInfo != EMPTY_STRING:
      InputError = False
      if len(CellInfo) != 3:
        InputError = True
      else:
        Digit = CellInfo[2]
        try:
          Row = int(CellInfo[0])
        except:
          InputError = True
        try:
          Column = int(CellInfo[1])
        except:
          InputError = True
        if (Digit < '1' or Digit > '9'):
          InputError = True
      if InputError:
        print("Invalid input")
      else:
        PuzzleGrid[Row][Column] = Digit
        Answer[2] = str(int(Answer[2]) + 1)
        Answer[int(Answer[2]) + 2] = CellInfo
        DisplayGrid(PuzzleGrid)
      print("Enter row column digit: ")
      print("(Press Enter to stop)")
      CellInfo = input()
  return PuzzleGrid, Answer

def DisplayMenu():
  print()
  print("Main Menu")
  print("=========")
  print("L - Load new puzzle")
  print("P - Load partially solved puzzle")
  print("S - Solve puzzle") 
  print("C - Check solution")
  print("K - Keep partially solved puzzle")
  print("X - Exit") 
  print()

def GetMenuOption():
  Choice = EMPTY_STRING
  while len(Choice) != 1:
    Choice = input("Enter your choice: ")
  return Choice[0]

def KeepPuzzle(PuzzleGrid, Answer):
  if PuzzleGrid[0][0] != 'X':
    print("No puzzle loaded")
  else:
    if int(Answer[2]) > 0:
      PuzzleName = Answer[0]
      FileOut = open(f"{PuzzleName}P.txt", 'w')
      for Line in range(int(Answer[2]) + 3):
        FileOut.write(Answer[Line])
        FileOut.write('\n')
      FileOut.close()
    else:
      print("No answers to keep")

def CheckSolution(PuzzleGrid, Answer, Solution):
  ErrorCount = 0
  Solved = False
  Correct = True
  Incomplete = False
  for Row in range(1, GRID_SIZE + 1):
    for Column in range(1, GRID_SIZE + 1):
      Entry = PuzzleGrid[Row][Column]
      if Entry == SPACE:
        Incomplete = True
      if not (Entry == Solution[Row][Column] or Entry == SPACE):
        Correct = False
        ErrorCount += 1
        print(f"You have made an error in row {Row} column {Column}")
  if not Correct:
    print(f"You have made {ErrorCount} error(s)")
  elif Incomplete:
    print("So far so good, carry on")
  elif Correct:
    Solved = True
  return ErrorCount, Solved

def CalculateScore(Answer, ErrorCount):
  Answer[1] = str(int(Answer[1]) - ErrorCount)
  return Answer

def DisplayResults(Answer): 
  if int(Answer[2]) > 0:
    print(f"Your score is {Answer[1]}")
    print(f"Your solution for {Answer[0]} was: ")
    for Line in range(3, int(Answer[2]) + 3):
      print(Answer[Line])
  else:
    print("You didn't make a start")

def NumberPuzzle():
  Finished = False
  PuzzleGrid, Puzzle, Answer, Solution = ResetDataStructures()
  while not Finished:
    DisplayMenu()
    MenuOption = GetMenuOption()
    if MenuOption == 'L':
      PuzzleGrid, Puzzle, Answer, Solution = LoadPuzzle(PuzzleGrid, Puzzle, Answer, Solution)
    elif MenuOption == 'P':
      PuzzleGrid, Puzzle, Answer, Solution = LoadPartSolvedPuzzle(PuzzleGrid, Puzzle, Answer, Solution)
    elif MenuOption == 'K':
      KeepPuzzle(PuzzleGrid, Answer) 
    elif MenuOption == 'C':
      if PuzzleGrid[0][0] != 'X':
        print("No puzzle loaded")
      else:
        if int(Answer[2]) > 0:
          ErrorCount, Solved = CheckSolution(PuzzleGrid, Answer, Solution)
          Answer = CalculateScore(Answer, ErrorCount) 
          if Solved:
            print("You have successfully solved the puzzle")
            Finished = True
          else:
            print(f"Your score so far is {Answer[1]}")
        else:
          print("No answers to check")
    elif MenuOption == 'S':
        PuzzleGrid, Answer = SolvePuzzle(PuzzleGrid, Puzzle, Answer)
    elif MenuOption == 'X':
      Finished = True
    else:
      ResponseNumber = random.randint(1, 5)
      if ResponseNumber == 1:
        print("Invalid menu option. Try again")
      elif ResponseNumber == 2:
        print("You did not choose a valid menu option. Try again")
      elif ResponseNumber == 3:
        print("Your menu option is not valid. Try again")
      elif ResponseNumber == 4:
        print("Only L, P, S, C, K or X are valid menu options. Try again")
      elif ResponseNumber == 5:
        print("Try one of L, P, S, C, K or X ")
  if Answer[2] != EMPTY_STRING:
    DisplayResults(Answer)

if __name__ == "__main__":
  NumberPuzzle()
