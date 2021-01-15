from .cell import Cell
import matplotlib.pyplot as plt
import networkx as nx


class Diamond:

    def __init__(self,size,nopeg_cell_list):
        self.size = size
        self.neighbor_move_values = ((-1,0),(-1,1),(0,1),(1,0),(1,-1),(0,-1))
        self.state_string = ""

        self.cell_list = []                                                     #Init cell-list
        for row in range(self.size):
            rowList = []
            for col in range(self.size):
                rowList.append(Cell((row,col)))
            self.cell_list.append(rowList)

        for cell_pos in nopeg_cell_list:                                        #Remove pins as specified in nopeg_cell_list 
            self.cell_list[cell_pos[0]][cell_pos[1]].remove_pin()

        self.init_neighbors()
        self.update_state_string()


    def init_neighbors(self):
        for row in self.cell_list:
            for cell in row:
                for move in self.neighbor_move_values:
                    row_pos = cell.position[0] + move[0]
                    col_pos = cell.position[1] + move[1]

                    if -1 < row_pos < self.size and -1 < col_pos < self.size:
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

    # (pinpos0,pinpos1,topos0,topos1)

    def move_4tup(self,tup):
        self.move((tup[0],tup[1]),(tup[2],tup[3]))

        
    def move(self,pin_pos,move):
        pin_cell = self.cell_list[pin_pos[0]][pin_pos[1]]
        if pin_cell.valid_move(move):
            #print("Moving pin at",pin_cell.position,"to position", (pin_cell.position[0]+move[0]*2,pin_cell.position[1]+move[1]*2))
            pin_cell.make_move(move)
            self.update_state_string()

    
    def print(self,frame_delay):
        display_grid = []

        diamond_shape = [i for i in range(1,self.size)]                  #diamond_shape is a list of lists defining the shape of the diamond. Ex size 4 makes [1,2,3,4,3,2,1]
        diamond_shape.extend([i for i in range(self.size,0,-1)])

        for i in range(len(diamond_shape)):                              #Here we create display_grid, where we distribute the nodes in lists according to diamond_shape
            display_grid.append([])                                      #Example size=3 : [[node1],[node2, node3],[node4,node5,node6],[node7,node8],[node9]]
            for j in range(diamond_shape[i]):
                if i < self.size:
                    display_grid[i].append(self.cell_list[i-j][j])
                else:
                    display_grid[i].append(self.cell_list[self.size-j-1][i-(self.size-j-1)])

        G = nx.Graph()
        node_colors = []
        for i in range(len(display_grid)):
            y = len(display_grid) - i
            x = (self.size-len(display_grid[i]))/2
            for cell in display_grid[i]:
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


#my_diamond = Diamond(4)
#my_diamond.create_diamond([(1,2),(3,1),(2,2),(2,1)])
#my_diamond.move(my_grid.cell_list[3][5],(1,-1))
#my_diamond.move(my_grid.cell_list[1][2],(0,-1))
#my_diamond.print(2)



    #def is_solveable_check(self):
    #    done_moves = []
    #    moves = self.get_possible_moves()
    #    while len(moves) > 0:
    #        current_move = moves.pop(0)
    #        if current_move not in done_moves:
    #            done_moves.append(current_move)
    #            self.move_4tup(current_move)
    #            if self.check_is_win_state():
    #                return True
    #            for move in moves:
    #                moves.append(moves)
    #    return False


    # def get_state(self):
    #     state_list = []
    #     for i in range(len(self.cell_list)):
    #         state_list.append([])
    #         for j in range(len(self.cell_list[i])):
    #             if self.cell_list[i][j].contains_pin:
    #                 state_list[i].append(1)
    #             else:
    #                 state_list[i].append(0)
    #     return state_list

