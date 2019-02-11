import board


class Cell:

    def __init__(self, board_x, board_y, row_block, column_block, square_block, solution_pool):
        self.board_x = board_x
        self.board_y = board_y

        self.row_block = row_block
        self.column_block = column_block
        self.square_block = square_block

        self.possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # order is irrelevant
        self.is_solved = False

        self.solution_pool = solution_pool

    def reset(self):
        self.possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.is_solved = False

    def set_number_impossible(self, number):
        if number in self.possible_numbers:
            self.possible_numbers.remove(number)

            # solution found because only one number left as possible for this cell
            if len(self.possible_numbers) == 1:
                self.solution_pool.add_triplet((self, self.possible_numbers[0], "POS_DED"))

            # conflict: now no number is possible in this cell!
            elif not self.possible_numbers:
                # print("Conflict: for cell " + str(self) + " all 9 numbers are impossible!")
                # return False
                raise Exception("Conflict: for cell " + str(self) + " all 9 numbers are impossible!")

        return True

    def get_number(self):
        if len(self.possible_numbers) == 1:
            return self.possible_numbers[0]
        else:
            return -1

    def set_number(self, number, comment):

        if self.is_solved:
            print("(" + comment + ": setting cell (" + str(self.board_x) + "," + str(self.board_y) + ") to number " + str(number) + ")")
        else:
            print(comment + ": setting cell (" + str(self.board_x) + "," + str(self.board_y) + ") to number " + str(number))

        # conflict: this cell is already set to a different number!
        if self.is_solved and self.get_number() != number:
            # print("Conflict: cell " + str(self) + " is assigned numbers " + str(self.get_number()) + " and " + str(number) + "!")
            # return False
            raise Exception("Conflict: cell " + str(self) + " is assigned numbers " + str(self.get_number()) + " and " + str(number) + "!")

        self.is_solved = True
        self.possible_numbers = [number]

        # go through all 3 blocks containing this cell
        for block in [self.row_block, self.column_block, self.square_block]:

            for c in [x for x in block.cells if x != self]:

                # set given number as impossible for all other cells in block
                # if not c.set_number_impossible(number):
                    # return False
                c.set_number_impossible(number)

                # go through number-possible-cells map in block
                for i in range(9):
                    # set current cell as only possible cell for given number in block
                    if i == number - 1:
                        block.number_possible_cells_map[i] = [self]
                    # set current cell as impossible for all other numbers in block
                    else:
                        if self in block.number_possible_cells_map[i]:
                            block.number_possible_cells_map[i].remove(self)
                            # if number can only go in one cell in block
                            if len(block.number_possible_cells_map[i]) == 1:
                                # then solve that cell
                                self.solution_pool.add_triplet((block.number_possible_cells_map[i][0], i + 1, "NEG_DED1(" + block.type_of_block + ")"))

                # go through all 3 (second order) blocks containing current cell
                for c_block in [c.row_block, c.column_block, c.square_block]:
                    # set current cell as impossible for number in current (second order) block
                    if c in c_block.number_possible_cells_map[number - 1]:
                        c_block.number_possible_cells_map[number - 1].remove(c)
                        # if number can only go in one cell in block
                        if len(c_block.number_possible_cells_map[number - 1]) == 1:
                            # then solve that cell using given number
                            self.solution_pool.add_triplet((c_block.number_possible_cells_map[number - 1][0], number, "NEG_DED2(" + block.type_of_block + ", " + c_block.type_of_block + ")"))

        return True

    def __repr__(self):
        return "(" + str(self.board_x + 1) + "," + str(self.board_y + 1) + ")"

    def pretty(self):
        if not self.possible_numbers:
            return "[X]"
        elif len(self.possible_numbers) == 1:
            return str(self.possible_numbers)
        else:
            return "[ ]"