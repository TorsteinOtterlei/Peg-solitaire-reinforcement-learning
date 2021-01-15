from .cell import Cell
import matplotlib.pyplot as plt
import networkx as nx

class Triangle:

    def __init__(self,size, nopeg_cell_list):
        self.cell_list = []
        self.size = size
        self.neighbor_move_values = ((0,-1),(-1,-1),(-1,0),(0,1),(1,1),(1,0))
        self.state_string = ""

        for row in range(self.size):
            rowList = []
            for col in range(row+1):
                rowList.append(Cell((row,col)))
            self.cell_list.append(rowList)

        for cell_pos in nopeg_cell_list:
            self.cell_list[cell_pos[0]][cell_pos[1]].remove_pin()
            
        self.init_neighbors()
        self.update_state_string()

    def init_neighbors(self):
        for row in self.cell_list:
            for cell in row:
                for move in self.neighbor_move_values:
                    row_pos = cell.position[0] + move[0]
                    col_pos = cell.position[1] + move[1]

                    if cell.position[0] == cell.position[1] and move in [(-1,0),(0,1)]:        #If we are on the "hypotenuse" of the triangle, do not try to add cells above or to the right
                        pass
                    elif -1 < row_pos < self.size and -1 < col_pos < self.size:
                        cell.add_neighbor(move,self.cell_list[row_pos][col_pos])


    def get_possible_moves(self):
        all_moves = []
        for row in self.cell_list:
            for cell in row:
                if cell.contains_pin:
                    for move in self.neighbor_move_values:
                        if cell.valid_move(move):
                            all_moves.append((cell.position[0],cell.position[1],move[0],move[1]))
        return all_moves

    def update_state_string(self):
        self.state_string = ""
        for row in self.cell_list:
            for cell in row:
                if cell.contains_pin:
                    self.state_string += "1"
                else:
                    self.state_string += "0"

    def check_is_win_state(self):
        return self.state_string.count('1') == 1

    def move_4tup(self,tup):
        self.move((tup[0],tup[1]),(tup[2],tup[3]))

    def move(self,pin_pos,move):
        pin_cell = self.cell_list[pin_pos[0]][pin_pos[1]]
        if pin_cell.valid_move(move):
            #print("Moving pin at",pin_cell.position,"to position", (pin_cell.position[0]+move[0]*2,pin_cell.position[1]+move[1]*2))
            pin_cell.make_move(move)
            self.update_state_string()
            

    def print(self,frame_delay):                           #Because the cell_list is already in the correct format, we do not need create a display_grid like we did with the diamond implementation
        G = nx.Graph()
        node_colors = []
        for i in range(len(self.cell_list)):
            y = len(self.cell_list) - i
            x = (self.size-len(self.cell_list[i]))/2
            for cell in self.cell_list[i]:
                pos=(x,y)
                x += 1
                color = 'lightblue'
                if not cell.contains_pin:
                    color='black'
                G.add_node(cell, pos=pos)
                node_colors.append(color)

        for cell in list(G.nodes):
            for neighbour in cell.get_neighbor_list():
                G.add_edge(cell, neighbour)

        pos = nx.get_node_attributes(G,'pos')
        nx.draw(G, pos, node_color=node_colors, node_size=5000, with_labels=False, font_weight='bold')
        plt.show(block=False)
        plt.pause(frame_delay)



#my_triangle = Triangle(4)
#my_triangle.create_triangle([(2,0)])
#my_triangle.move(my_triangle.cell_list[0][0],(1,0))
#my_triangle.move(my_triangle.cell_list[1][2],(0,-1))
#print(my_triangle.get_possible_moves())
#my_triangle.print(10)

    

