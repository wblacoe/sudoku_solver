class Block:

    def __init__(self, type_of_block):
        self.type_of_block = type_of_block
        self.cells = []
        self.number_possible_cells_map = [[], [], [], [], [], [], [], [], []]

    def add_cell(self, cell):
        self.cells.append(cell)
        for possible_cells in self.number_possible_cells_map:
            possible_cells.append(cell)

    def reset(self):
        self.number_possible_cells_map = [[], [], [], [], [], [], [], [], []]
        for c in self.cells:
            for possible_cells in self.number_possible_cells_map:
                possible_cells.append(c)

    def __repr__(self):
        s = ""
        for i in range(9):
            if i % 3 == 0:
                s += "\t"
            s += self.cells[i].pretty()
        s += "\n"

        return s