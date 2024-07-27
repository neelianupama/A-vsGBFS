"""
The program implements a route search in a board of NxN size, in order to
get from the start point A to endpoint B using the algorithms: Greedy Best
First and A*. Each cell on the board depicts an area cell. The area cell 
can be through paved R, through unpaved D, or water W.

You can move on the board from the current cell to the adjacent cell using
 the following actions: up U, down D, right R, left L. 
 Note: the movement to the water or out of the board is prohibited.

The cost of the passage (function g) is calculated according to the type of
area cell: use of through paved = 1, use of through unpaved = 4.

The program reads from the 'input.txt' input file containing:
1. The type of algorithm to be run (line number 1 in the file).
2. Board size (row number 2 in the file).
3. Initial board mode (line number 3 to the end of the file).

At the end of the program the search results, the route from A to B, and
its cost are written to the output file 'output.txt'.

@author: Bari Arviv
"""
import copy 
# Global variables
BALK = 'W'
G = {'R': 1, 'D': 4, 'B': 0}


def read_file(file_name):
    """The function reads from the file in the resulting
       path the initial state of the graph and the name 
       of the function with which we will perform the search.
       :param file_name: file path
       :type  file_name: string
       :return: initial state, the name of the function
                and the size of initial state.
       :rtype:  typle 
    """
    init_state = []
    with open("D:/SASTRA/ACADEMICS/5TH SEM/AI/ASSIGNMENT/Astar-Greedy-Best-First-master/Astar-Greedy-Best-First-master/input.txt", 'r') as input_file:
        func = input_file.readline()
        size = input_file.readline()
        
        for line in input_file:
            init_state.append([word for word in line.rstrip('n')])

    return func, int(size), init_state


def print_state(state, size):
    """The function prints the received state.
       :param state: state
       :type  state: list of lists
       :param size:  the size of the state.
       :type  size:  int
    """
    for i in range(size):
        for j in range(size):
            print(state[i][j], end =" ")
        # print new line
        print()
 
    
def find_index(state, cell, size):
    """The function searches for the cell index in the received state.
       :param state: state
       :type  state: list of lists
       :param cell:  the name of the cell.
       :type  cell:  string
       :param size:  the size of the state.
       :type  size:  int
       :return: coordinates x, y where the cell in the state, if the 
                cell does not exist in the state, returns None.
       :rtype:  list of ints
    """
    for x in range(size):
        for y in range(size):
            if state[x][y] == cell:
                return [x, y]   
    
    return None
            

def goal_state(target, position):
    """The function checks if we have reached the target state.
       :param target:   target x,y coordinates
       :type  target:   list of ints
       :param position: current x,y coordinates
       :type  position: list of ints
       :return: true if position is a target index, otherwise, false.
       :rtype:  boolean
    """
    return (target == position)


def get_successors(state, position):
    """The function activates the possible operators on the current 
       state and produces a new state from the operation of the operator.
       The operator moves up/down/left/right the cekk if possible.
       :param state:    current state
       :type  state:    list of lists
       :param position: current x,y coordinates
       :type  position: list of ints
       :return: list of dicts, each dict includes the operator activated
                on the current state, g value, new index, and the new 
                state obtained from the operation of the operator.
       :rtype: list of dicts
    """
    pairs_list = []
    size = len(state)
    
    # finding the position of the digit zero in the current state
    x, y = position
    
    # for up operation -> if x != 0 and not W (water)
    if x and (state[x - 1][y] != BALK): 
        new, g = replace_position(state, x, y, x - 1, y)
        pairs_list.append({'state': new, 'g': g, 
                           'index': [x - 1, y], 'operation': 'U'})
    
    # for down operation -> if x != len - 1 and not W (water)
    if (x != size - 1) and (state[x + 1][y] != BALK): 
        new, g = replace_position(state, x, y, x + 1, y)
        pairs_list.append({'state': new, 'g': g, 
                           'index': [x + 1, y], 'operation': 'D'})
        
    # for left operation -> if y != 0 and not W (water)
    if y and (state[x][y - 1] != BALK): 
        new, g = replace_position(state, x, y, x, y - 1)
        pairs_list.append({'state': new, 'g': g, 
                           'index': [x, y - 1], 'operation': 'L'})
    
    # for right operation -> if y != len - 1 and not W (water)
    if (y != size - 1) and (state[x][y + 1] != BALK): 
        new, g = replace_position(state, x, y, x, y + 1)
        pairs_list.append({'state': new, 'g': g, 
                           'index': [x, y + 1], 'operation': 'R'})
    
    return pairs_list


def replace_position(state, x, y, new_x, new_y):
    """The function creates a new state and swaps between the old 
       (x, y) coordinates and the new (new_x, new_y) coordinates.
       :param state: current state
       :type  state: list of lists
       :param x, y:  old coordinates
       :type  x, y:  int
       :param new_x, new_y: new coordinates
       :type  new_x, new_y: int
       :return: new state and the cost of the step.
       :rtype:  tuple
    """
    new_st = copy.deepcopy(state)
    new_st[x][y], new_st[new_x][new_y] = new_st[new_x][new_y], new_st[x][y]
    return new_st, G[new_st[x][y]]


def find_state(index, states_list): 
    """The function searches if the index exists in the list.
       :param index: index of the current state
       :type  index: int
       :param states_list: the list of states.
       :type  states_list: list of dicts
       :return: if the index exists in the list.
       :rtype:  boolean
    """
    for st in states_list:
        if index == st['index']:
            return True
        
    return False


def manhattan(position, target):
    """The function calculates the distance at an absolute  
       value between the current index and the target index.
       :param position: current x,y coordinates
       :type  position: list of ints
       :param target:   target x,y coordinates
       :type  target:   list of ints
       :return: the distance in absolute value is between 
                the current index and the target index.
       :rtype:  int
    """
    return (abs(position[0] - target[0]) + abs(position[1] - target[1]))


def improvement_on_edges(index, new_g, states_list, new_parent, pop_close): 
    """The function checks if there is a need for improvement 
       at the edges, that is, whether the new g value is smaller
       than the current value. If the state does not exist in 
       the list, we will return None. Otherwise, we will update
       the values g, f, and the new parent state. In addition, 
       if the state exists in the closed list, we will remove 
       it from the list and return the tuple, whether the state 
       should be added to the open list and the state.
       :param index: index of the current state
       :type  index: int
       :param new_g: the new g value
       :type  new_g: int
       :param states_list: the list of states.
       :type  states_list: list of dicts
       :param new_parent:  the new parent of the current state.
       :type  new_parent:  list of lists
       :param pop_close:   does the state exist on the close list.
       :type  pop_close:   boolean
       :return: whether the state should be added to the 
                open list and the state.
       :rtype:  tuple
    """
    # for each state in states_list
    for i in range(len(states_list)):
        if index == states_list[i]['index']:
            # improvement on the edges
            if states_list[i]['g'] > new_g:
                # update f, g and parent
                states_list[i]['g'] = new_g
                states_list[i]['f'] = new_g + states_list[i]['h']
                states_list[i]['parent'] = new_parent
                
                if pop_close:
                    return True, states_list.pop(states_list[i])
                   
            return False, states_list[i]
            
    return None, None


def backpropagation(close):
    """The function restores the optimal route to the target state.
       :param close: the list of states.
       :type  close: list of dicts
       :return: a string containing the route to the target state.
       :rtype:  string 
    """
    path = ""

    for i in range(len(close) - 1, 0, -1):
        if close[i]['parent'] == close[i - 1]['state']:
            path += close[i]['operation'] + "-"
            _ = close.pop(i)
        else:
            _ = close.pop(i - 1)
                  
    return path[:-1]


def greedy_best_first(state, h, start_index, target_index):
    """Greedy Best First algorithm:
       1. Build a search graph G, with an init state, state, 
          and put state in the OPEN list.
       2. Create an empty CLOSE list.
       3. Loop: As long as OPEN is not empty:
       4. Sort the OPEN according to h (distance manhattan).
       5. Select the first state (next_state) in OPEN, remove 
          next_state from OPEN and insert it into CLOSE.
       6. If next_state is a target state, return the cost and route.
       7. Expand next_state and create its sons M in G.
       8. For states from M not in OPEN or CLOSE - calculate h, enter
          OPEN, and create a pointer from them to next_state (the parent).
       :param state: init state
       :type  state: list of lists
       :param h: a function that calculates the heuristic value for each state.
       :type  h: manhattan function
       :param start_index:  start x,y coordinates
       :type  start_index:  list of ints
       :param target_index: target x,y coordinates
       :type  target_index: list of ints
       :return:  if we were able to get the goal, return the
                 cost and route, otherwise, return None.
       :rtype:   tuple
    """    
    count = 0    
    close = []
    opens = [{'state': state, 'h': h(start_index, target_index), 'g': 0,
               'index': start_index, 'operation': "", 'parent': None}]
    
    # as long as OPEN is not empty
    while opens:
        opens.sort(key=lambda x: x['h'], reverse=True)
        next_state = opens.pop()
        close.append(next_state)
        
        count += 1
        print('step{}:\tindex={},\th={},\tg={},\top={}'
              .format(count, next_state['index'], next_state['h'], 
                      next_state['g'], next_state['operation']))
        
         # goal condition is satisfied
        if goal_state(target_index, next_state['index']):
            return backpropagation(close)[::-1], next_state['g'] 
        
        # for each new state obtained from operating the operators
        for st in get_successors(next_state['state'], next_state['index']):
            if not find_state(st['index'], opens) and not find_state(st['index'], close):
                opens.append({'state': st['state'], 'index': st['index'], 
                              'operation': st['operation'],
                              'g': next_state['g'] + st['g'], 
                              'h': h(st['index'], target_index),
                              'parent': next_state['state']})

    # opens is empty -> no solution
    return None, None


def astar(state, h, start_index, target_index):
    """A* algorithm:
       1. Build a search graph G, with an init state, state, 
          and put state in the OPEN list.
       2. Create an empty CLOSE list.
       3. Loop: As long as OPEN is not empty:
       4. Sort the OPEN according to f.
       5. Select the first state (next_state) in OPEN, remove 
          next_state from OPEN and insert it into CLOSE.
       6. If next_state is a target state, return the cost and route.
       7. Expand next_state and create its sons M in G.
       8. For states from M not in OPEN or CLOSE - calculate f, enter
          OPEN, and create a pointer from them to next_state (the parent).
       9. For the rest of the M states that are in OPEN or CLOSE, 
          you need to decide if update f and put a pointer to 
          next_state (the new parent) or not.
       :param state: init state
       :type  state: list of lists
       :param h: a function that calculates the heuristic value for each state.
       :type  h: manhattan function
       :param start_index:  start x,y coordinates
       :type  start_index:  list of ints
       :param target_index: target x,y coordinates
       :type  target_index: list of ints
       :return:  if we were able to get the goal, return the
                 cost and route, otherwise, return None.
       :rtype:   tuple
    """
    count = 0
    h_state = h(start_index, target_index)
    
    close = []
    opens = [{'state': state, 'h': h_state, 'g': 0, 'index': start_index, 
              'operation': "", 'f': h_state, 'parent': None}]
    
    # as long as OPEN is not empty
    while opens:
        opens.sort(key=lambda x: x['f'], reverse=True)
        next_state = opens.pop()
        close.append(next_state)
        
        count += 1
        print('step{}:\tindex={},\th={},\tg={},\tf={},\top={}'
              .format(count, next_state['index'], next_state['h'], 
                      next_state['g'], next_state['f'], 
                      next_state['operation']))
        
        # goal condition is satisfied
        if goal_state(target_index, next_state['index']):
            return backpropagation(close)[::-1], next_state['f'] 
        
        # for each new state obtained from operating the operators
        for st in get_successors(next_state['state'], next_state['index']):
            new_g = next_state['g'] + st['g']
            in_close = find_state(st['index'], close)
            
            if not find_state(st['index'], opens) and not in_close:
                h_state = h(st['index'], target_index)
                opens.append({'state': st['state'], 'index': st['index'],  
                              'operation': st['operation'], 'g': new_g,
                              'f': h_state + new_g, 'h': h_state,
                              'parent': next_state['state']})
            else:
                if not in_close:
                    _ = improvement_on_edges(st['index'], new_g, opens, 
                                             next_state['state'], in_close)
                else:
                    res, s = improvement_on_edges(st['index'], new_g, close,
                                                  next_state['state'], 
                                                  in_close)
                    if res:
                        opens.append(s)
                    
    # opens is empty -> no solution
    return None, None


def main():
    start = 'A'
    target = 'B'
    input_file = 'input.txt'
    output_file = 'output.txt'
    
    # reading the initial state from the file
    func, size, init_state = read_file(input_file)

    print('The init state is:')
    print_state(init_state, size)
    
    # checking the position of the start cell and the target cell
    start_index = find_index(init_state, start, size)
    target_index = find_index(init_state, target, size)
    
    if not start_index or not target_index:
        print("""\nThe input file is invalid! Please repair 
                 the file and try running the program again.""")
        return None
    
    # func[:-1]: the name of the function without \n
    title = 'The output for the {} algorithm is:\n'.format(func[:-1])
    print('\n' + title[:-1])
    
    if 'A*' in func: 
        # Astar
        path, cost = astar(init_state, manhattan, start_index, target_index)
    else:           
        # Greedy Best First
        path, cost = greedy_best_first(init_state, manhattan, 
                                       start_index, target_index)
    
    print('\nThe result is:\n{} {}'.format(path, cost))
   
    # write the results to an output file
    with open(output_file, 'w') as output_file:
        output_file.write(title)
        if path:
            output_file.write(path + ' ' + str(cost))
        else:
            output_file.write('no path')


if __name__ == "__main__":
    main()