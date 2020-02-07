from cell import Cell
import matplotlib.pyplot as plt
import networkx as nx
#import pylab as py

class Grid:

    def __init__(self):
        self.cell_list = []

    
    def create_diamond(self,nopeg_cell_list):
        for row in range(5):
            rowList = []
            for col in range(5):
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

                    if -1 < row_pos < 4 and -1 < col_pos < 4:
                        cell.add_neighbor(move,self.cell_list[row_pos][col_pos])

        
    def move(self,pin_cell,move):
        if pin_cell.valid_move(move):
            pin_cell.make_move(move)

        
    
    def print_diamond(self):
        #print(self.cell_list[0][0].contains_pin)
        #print(self.cell_list[0][2].get_neighbor((0,-1)).get_neighbor((0,-1)).position)
        #print(self.move(self.cell_list[0][2],(0,-1)))
        #print(self.cell_list[0][2].contains_pin)

        display_grid = []
        for i in range(4):
            for j in range(4):
                display_grid.append(self.cell_list[i][j])

        G = nx.Graph()
        node_colors = []
        for i in range(len(display_grid)):
            y = len(display_grid) - i
            x = (16-len(display_grid))/2
            for cell in display_grid[i]:
                pos=(x,y)
                x += 1
                color = 'lightblue'
                if not cell.contains_pin:
                    color='black'
                G.add_node(cell, pos=pos)
                node_colors.append(color)

        # Add edges
        for row in self.cell_list:
            for cell in row:
                for neighbour in cell.get_neighbor_list():
                    G.add_edge(cell, neighbour)


        ###############################################################3
        pos=nx.get_node_attributes(G,'pos')
        nx.draw(G, pos, node_color=node_colors, node_size=5000, with_labels=True, font_weight='bold')





my_grid = Grid()
my_grid.create_diamond([(0,0)])
my_grid.print_diamond()