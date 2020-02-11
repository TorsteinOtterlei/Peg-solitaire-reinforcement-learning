
class Cell:

    #TODO: DICTIONARY FOR NEIGBORING NODES. KEY IS POSITION

    def __init__(self,position,contains_pin=True):
        self.contains_pin = contains_pin
        self.position = position
        self.neighbors = {}
    
    #def get_position(self):
    #    return self.position

    def remove_pin(self):
        if self.contains_pin:
            self.contains_pin = False
        else:
            print("Cant remove pin. There is no pin to remove!")    #Remove this

    def put_pin(self):
        if self.contains_pin:
            print("This cell already contains a pin!")              #Remove this
        else:
            self.contains_pin = True

    def add_neighbor(self,relative_move,cell):
        self.neighbors[relative_move] = cell

    def get_neighbor_list(self):
        return list(self.neighbors.values())
    
    def get_neighbor(self,move):
        if move in self.neighbors:
            return self.neighbors[move]
        raise Exception("This is not a neighbor of this node! Might be out of board.")


    def valid_move(self,move):                                    #Checks himself and the neighbor in question
        if not self.contains_pin:
            print("This cell does not have a pin to move!")       #Checks if himself has peg
            return False

        if not self.get_neighbor(move).contains_pin:
            print("There are no pin to jump over!")                     #Get cell two and check if he has peg
            return False

        if self.get_neighbor(move).get_neighbor(move).contains_pin:     #Get cell three and make sure he has no peg
            print("The final position already has a pin!")
            return False  
        
        #print("This is a valid move")
        return True                                                     #Return true/false

    
    def make_move(self,move):
        self.remove_pin()
        self.get_neighbor(move).remove_pin()
        self.get_neighbor(move).get_neighbor(move).put_pin()
    

