
def SolvePuzzle(PuzzleGrid, Puzzle, Answer):
    DisplayGrid(PuzzleGrid)
    if PuzzleGrid[0][0] != 'X':
        print("No puzzle loaded")
    else:
        print("Enter row column digit: ")
        print("(Press Enter to stop)")
        CellInfo = input()
        while CellInfo.strip() != "":
            InputError = False
            if len(CellInfo) != 3:
                InputError = True
            else:
                Digit = CellInfo[2]
                try:
                    Row = int(CellInfo[0])
                    Column = int(CellInfo[1])
                except ValueError:
                    InputError = True
                else:
                    if (Digit < '1' or Digit > '9'):
                        InputError = True
                    elif Puzzle[Row][Column] == 'X':
                         print("Cell is protected. Cannot change.")
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

return solvePuzzle