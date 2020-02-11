from .cell import Cell
import matplotlib.pyplot as plt
import networkx as nx


class Diamond:

    def __init__(self,size):
        self.cell_list = []
        self.size = size

    
    def create_diamond(self,nopeg_cell_list):
        for row in range(self.size+1):
            rowList = []
            for col in range(self.size+1):
                rowList.append(Cell((row,col)))
            self.cell_list.append(rowList)

        for cell_pos in nopeg_cell_list:
            self.cell_list[cell_pos[0]][cell_pos[1]].remove_pin()

        self.init_neighbors_diamond()


    def init_neighbors_diamond(self):
        neighbor_move_values = ((-1,0),(-1,1),(0,1),(1,0),(1,-1),(0,-1))
        for row in self.cell_list:
            for cell in row:
                for move in neighbor_move_values:
                    row_pos = cell.position[0] + move[0]
                    col_pos = cell.position[1] + move[1]

                    if -1 < row_pos < self.size and -1 < col_pos < self.size:
                        cell.add_neighbor(move,self.cell_list[row_pos][col_pos])

        
    def move(self,pin_cell,move):
        if pin_cell.valid_move(move):
            print("Moving pin at",pin_cell.position,"to position", (pin_cell.position[0]+move[0]*2,pin_cell.position[1]+move[1]*2))
            pin_cell.make_move(move)

    
    def print_diamond(self):
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
        plt.show()


#my_diamond = Diamond(5)
#my_diamond.create_diamond([(0,0)])
#my_diamond.move(my_grid.cell_list[3][5],(1,-1))
#my_diamond.move(my_grid.cell_list[1][2],(0,-1))
#my_diamond.print_diamond()
