import cell
import block
import pool
import random


class Board:

    def __init__(self):
        self.solution_pool = pool.Pool()

        self.all_cells = []
        self.row_blocks = []
        self.column_blocks = []
        self.square_blocks = []

        for i in range(9):
            self.row_blocks.append(block.Block("row"))
            self.column_blocks.append(block.Block("column"))
            self.square_blocks.append(block.Block("square"))

        for y in range(9):
            row = []
            for x in range(9):

                # identify row, column and square blocks containing given cell
                row_block = self.row_blocks[y]
                column_block = self.column_blocks[x]
                square_block = self.square_blocks[(y // 3) * 3 + (x // 3)]

                # create new cell and save pointers to the row, column and square block containing it
                c = cell.Cell(x, y, row_block, column_block, square_block, self.solution_pool)

                # save cell in row, column and square block containing it
                row.append(c)
                row_block.add_cell(c)
                column_block.add_cell(c)
                square_block.add_cell(c)

            self.all_cells.append(row)

        self.amount_of_resets = 0
        self.amount_of_guesses = 0

    def get_cell(self, x, y):
        return self.all_cells[y][x]

    def get_amount_of_solved_cells(self):
        amount = 0
        for row in self.all_cells:
            for c in row:
                if c.is_solved:
                    amount += 1

        return amount

    def is_solved(self):
        return self.get_amount_of_solved_cells() == 81
        
    def add_solution(self, cell_to_be_solved, number, type_of_solution):
        self.solution_pool.add_triplet((cell_to_be_solved, number, type_of_solution))

    def add_solutions(self, triplets_as_string):
        triplets = triplets_as_string.split(", ")
        for triplet in triplets:
            entries = triplet.split(" ")
            try:
                x = int(entries[0]) - 1
                y = int(entries[1]) - 1
                number = int(entries[2])
            except ValueError:
                print("Invalid input! If you are trying to set values on the board your input needs to be a (comma-separated) list of triplets 'x y number' where x, y and number must be numbers from 1 to 9.")
                print("The following example would put an 8 in the top right corner and a 7 in the center of the board: 9 1 8, 5 5 7")
                break
            self.add_solution(self.get_cell(x, y), number, "INIT")

    def solve_one_cell(self):
        return self.solution_pool.execute_next_triple()

    def guess_one_cell(self):
        if self.is_solved():
            print("Sudoku is already solved.")
        else:
            self.amount_of_guesses += 1
        
            # collect all unsolved cells
            unsolved_cells = []
            for y in range(9):
                for x in range(9):
                    c = self.all_cells[y][x]
                    if not c.is_solved:
                        unsolved_cells.append(c)
    
            # pick a random unsolved cells
            random_unsolved_cell = random.choice(unsolved_cells)
    
            # pick a random possible number for this cell
            random_possible_number = random.choice(random_unsolved_cell.possible_numbers)
    
            # use these as guessed solution
            self.solution_pool.add_triplet((random_unsolved_cell, random_possible_number, "GUESS"))

    def solve_sudoku(self):
        while True:
            try:
                while self.solve_one_cell():
                    pass
                if self.is_solved():
                    break
                self.guess_one_cell()
            except Exception as e:
                print(str(e))
                self.reset(False)
        print("Solved sudoku with " + str(self.amount_of_resets) + " reset(s) and " + str(self.amount_of_guesses) + " guess(es) (in the final pass)")

    def reset(self, clear_init_queue):
        self.solution_pool.reset(clear_init_queue)

        for i in range(9):
            self.row_blocks[i].reset()
            self.column_blocks[i].reset()
            self.square_blocks[i].reset()

        for row in self.all_cells:
            for c in row:
                c.reset()

        self.amount_of_guesses = 0
        self.amount_of_resets += 1

    def __repr__(self):
        s = ""
        for i in range(9):
            if i % 3 == 0:
                s += "\n"
            s += str(self.row_blocks[i])

        return s