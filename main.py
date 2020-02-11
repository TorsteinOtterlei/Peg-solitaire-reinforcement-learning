import json
from game.triangle import Triangle
from game.diamond import Diamond

with open('parameters.json') as f:
        parameters = json.load(f)

def open_cell_list_gen(json_list):
    open_cell_list = []
    for val in parameters['open_cells']:
            open_cell_list.append((int(val[1]),int(val[3])))
    return open_cell_list


def main():

    open_cell_list = open_cell_list_gen(parameters['open_cells'])

    if parameters['board_type'] == "diamond":
        my_diamond = Diamond(parameters['board_size'])                  #Initiate diamond-board

        my_diamond.create_diamond(open_cell_list)                       #Adds open cells specified in json

        #If parameters['display_var']:
        my_diamond.print_diamond()                                      #Prints board with networkx

    elif parameters['board_type'] == "triangle":
        my_triangle = Triangle(parameters['board_size'])                #Initiate traingle-board

        my_triangle.create_triangle(open_cell_list)                     #Adds open cells specified in json

        #If parameters['display_var']:
        my_triangle.print_triangle()                                    #Prints board with networkx

        

if __name__ == "__main__":
    main()