import board


# start with empty board
board = board.Board()

def print_help():
    print("Commands:\n\nh or help\tfor this help\nx or exit\tto exit\nx y n\t\tto add the value 'n' at cell (x,y)\nb or board\tto show the board\na or amount\tto show how many cells have been solved\ns or solve\tto solve the sudoku\ns1 or solve1\tto solve only one cell\np or pool\tto show the solution pool\ng1 or guess1\tto guess the value of one cell\nc or clear\tto clear the board\n\ne or example\tto run an example")

def run_example():
    board.reset(True)
    board.add_solutions("3 1 9, 7 1 7, 8 1 3, 9 1 1, 2 2 3, 6 2 7, 4 3 3, 5 3 4, 7 3 8, 1 4 7, 8 4 5, 1 5 8, 2 5 9, 4 5 5, 6 5 6, 8 5 4, 9 5 7, 2 6 5, 9 6 6, 3 7 6, 5 7 5, 6 7 9, 4 8 2, 8 8 1, 1 9 5, 2 9 8, 3 9 2, 7 9 3")
    board.solution_pool.execute_all_init_triplets()
    print(str(board.get_amount_of_solved_cells()) + " cells have been solved.")
    print(str(board))
    print("Above is an example setting. Input 'solve' to solve the sudoku. Or input 'help' to show all commands.")

#print("SUDOKU SOLVER\n")
#print_help()
#print(str(board))
run_example()

# input board values
while True:
    s = input(">> ")

    if s == "":
        pass

    elif s == "help" or s == "h":
        print_help()

    elif s == "exit" or s == "x":
        break

    elif s == "board" or s == "b":
        print(str(board))

    elif s == "amount" or s == "a":  # amount of solved cells
        print(str(board.get_amount_of_solved_cells()) + " cells have been solved.")

    elif s == "debug" or s == "d":
        pass

    elif s == "example" or s == "e":
        run_example()

    elif s == "solve" or s == "s":
        board.solve_sudoku()
        print(str(board.get_amount_of_solved_cells()) + " cells have been solved.")
        print(str(board))

    elif s == "solve1" or s == "s1":
        board.solve_one_cell()
        print(str(board.get_amount_of_solved_cells()) + " cells have been solved.")
        print(str(board))

    elif s == "pool" or s == "p":
        print(str(board.solution_pool))

    elif s == "guess1" or s == "g1":
        board.guess_one_cell()

    elif s == "clear" or s == "c":
        board.reset(True)

    else:
        board.add_solutions(s)