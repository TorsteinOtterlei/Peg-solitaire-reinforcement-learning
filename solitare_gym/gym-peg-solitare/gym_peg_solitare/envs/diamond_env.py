import gym
from gym import error, spaces, utils
from gym.utils import seeding

from .cell import Cell
import matplotlib.pyplot as plt
import networkx as nx

class DiamondEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
#        self.size = 4
        self.neighbor_move_values = ((-1,0),(-1,1),(0,1),(1,0),(1,-1),(0,-1))
        self.state_string = ""
        self.viewer = None
        self.is_initialized = False

#        self.cell_list = []                                                     #Init cell-list
#        for row in range(self.size):
#            rowList = []
#            for col in range(self.size):
#                rowList.append(Cell((row,col)))
#            self.cell_list.append(rowList)

#        for cell_pos in nopeg_cell_list:                                        #Remove pins as specified in nopeg_cell_list 
#            self.cell_list[cell_pos[0]][cell_pos[1]].remove_pin()

#        self.init_neighbors()
#        self.update_state_string()

    
    def set_size_and_nopeg(self, size, nopeg_cell_list):
        self.is_initialized = True
        self.cell_list = []                                                     #Init cell-list
        for row in range(self.size):
            rowList = []
            for col in range(self.size):
                rowList.append(Cell((row,col)))
            self.cell_list.append(rowList)
        
        for cell_pos in nopeg_cell_list:                                        #Remove pins as specified in nopeg_cell_list 
            self.cell_list[cell_pos[0]][cell_pos[1]].remove_pin()

        self.size = size
        self.init_neighbors()
        self.update_state_string()
    

    def init_check(self):
        if not self.is_initialized:
            raise Exception("Game board not initialized. Run set_size_and_nopeg(size,nopeg_cell_list) before trying to run a function.")


    def init_neighbors(self):
        self.init_check()
        for row in self.cell_list:
            for cell in row:
                for move in self.neighbor_move_values:
                    row_pos = cell.position[0] + move[0]
                    col_pos = cell.position[1] + move[1]

                    if -1 < row_pos < self.size and -1 < col_pos < self.size:
                        cell.add_neighbor(move,self.cell_list[row_pos][col_pos])

    def get_possible_moves(self):
        self.init_check()
        all_moves = []
        for row in self.cell_list:
            for cell in row:
                if cell.contains_pin:
                    for move in self.neighbor_move_values:
                        if cell.valid_move(move):
                            all_moves.append((cell.position[0],cell.position[1],move[0],move[1]))
        return all_moves



    def step(self, action):
        self.init_check()
        #action = (pin_pos, move)
        pin_cell = self.cell_list[pin_pos[0]][pin_pos[1]]
        if pin_cell.valid_move(move):
            #print("Moving pin at",pin_cell.position,"to position", (pin_cell.position[0]+move[0]*2,pin_cell.position[1]+move[1]*2))
            pin_cell.make_move(move)
            self.update_state_string()


    def reset(self):
        self.init_check()
        #self.state = self.init_state
        #return self.state
        pass


    def render(self, mode='human'):
        self.init_check()
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
        self.viewer = plt.show(block=False)
        plt.pause(frame_delay)



    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    #def reset(self):

    #def compute_reward(self):
    
