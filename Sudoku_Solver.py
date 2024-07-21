import random

def display(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")
        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

def find(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None

def valid(bo, value, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == value and pos[1] != i:
            return False
    for i in range(len(bo)):
        if bo[i][pos[1]] == value and pos[0] != i:
            return False
    box_i = pos[0] // 3
    box_j = pos[1] // 3
    for i in range(box_i * 3, box_i * 3 + 3):
        for j in range(box_j * 3, box_j * 3 + 3):
            if bo[i][j] == value:
                return False
    return True

def Solve(bo):
    find_element = find(bo)
    if not find_element:
        return True
    else:
        row, col = find_element

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if Solve(bo):
                return True

            bo[row][col] = 0

    return False

def fill_board(bo):
    nums = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                random.shuffle(nums)
                for num in nums:
                    if valid(bo, num, (i, j)):
                        bo[i][j] = num
                        if fill_board(bo):
                            return True
                        bo[i][j] = 0
                return False
    return True

def remove_elements(bo, attempts=20):
    num_removed = 0
    while num_removed < attempts:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if bo[row][col] != 0:
            backup = bo[row][col]
            bo[row][col] = 0
            copy_board = [row[:] for row in bo]
            if Solve(copy_board):
                num_removed += 1
            else:
                bo[row][col] = backup 

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    remove_elements(board)
    return board
def main():
    board = generate_sudoku()
    print("Generated Sudoku board :")
    display(board)
    print("Solving")
    Solve(board)
    display(board)

if __name__=='__main__':
    main()