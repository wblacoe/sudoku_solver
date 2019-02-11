class Pool:

    def __init__(self):
        self.init_queue = []  # contains triplets (cell, number, comment)
        self.init_index = 0
        
        self.later_queue = []  # contains triplets (cell, number, comment)
        self.later_index = 0

    def reset(self, clear_init_queue):
        if(clear_init_queue):
            self.init_queue = []
        self.init_index = 0
        self.later_queue = []
        self.later_index = 0

    @property
    def init_queue_has_more(self):
        return self.init_index < len(self.init_queue)

    @property
    def later_queue_has_more(self):
        return self.later_index < len(self.later_queue)

    def add_triplet(self, triplet):
        if triplet[2] == "INIT":
            self.init_queue.append(triplet)
        else:
            self.later_queue.append(triplet)

    def execute_next_init_triplet(self):
        if self.init_queue_has_more:
            triplet = self.init_queue[self.init_index]
            self.init_index += 1
            return triplet[0].set_number(triplet[1], triplet[2])
        else:
            return False

    def execute_next_later_triplet(self):
        if self.later_queue_has_more:
            triplet = self.later_queue[self.later_index]
            self.later_index += 1
            return triplet[0].set_number(triplet[1], triplet[2])
        else:
            return False

    def execute_next_triple(self):
        return self.execute_next_init_triplet() or self.execute_next_later_triplet()

    def execute_all_init_triplets(self):
        while self.execute_next_init_triplet():
            pass

    def __repr__(self):

        s = "[ init queue ] (executed " + str(self.init_index) + "/" + str(len(self.init_queue)) + " triplets)\n"
        for triplet in self.init_queue:
            s += "\t" + str(triplet) + "\n"

        s += "[ later queue ] (executed " + str(self.later_index) + "/" + str(len(self.later_queue)) + " triplets)\n"
        for triplet in self.later_queue:
            s += "\t" + str(triplet) + "\n"

        return s