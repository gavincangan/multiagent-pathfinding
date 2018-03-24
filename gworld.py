import numpy as np

from macros import *
from visualize import *

class GridWorld:
    def __init__(self, h, w, rocks = None, agent_sng = None):
        self.h = h
        self.w = w
        self.cells = np.zeros((h, w), dtype=int)
        self.visualize = None
        self.add_rocks(rocks)

        self.aindx_cpos = dict()
        self.aindx_goal = dict()
        self.tyx_res = dict()

    def xy_saturate(self, x,y):
        if(x<0): x=0
        if(x>self.w-1): x=self.w-1
        if(y<0): y=0
        if(y>self.h-1): y=self.h-1
        return(x, y)

    def add_rocks(self, rocks):
        if rocks:
            for rock in rocks:
                rockx, rocky = self.xy_saturate(rock[1], rock[0])
                if( not self.is_blocked(rocky, rockx) ):
                    self.cells[rocky][rockx] = IS_ROCK

    '''
    agent_sng - (sy, sx, gy, gx)
        -- start and goal positions for each agent
    '''
    def add_agents(self, agents_sng):
        if agents_sng:
            print agents_sng
            # Replace list of tuples with a dict lookup for better performance
            for (sy, sx, gy, gx) in agents_sng:
                nagents = len( self.aindx_cpos.keys() )
                if(not self.is_blocked(sy, sx) and not self.is_blocked(gy, gx)):
                    if(self.cells[sy][sx] == UNOCCUPIED):
                        self.aindx_cpos[nagents + 1] = (sy, sx)
                        self.cells[sy][sx] = nagents + 1
                        self.aindx_goal[nagents + 1] = (gy, gx)
                    else:
                        raise Exception('Cell has already been occupied!')
                else:
                    raise Exception( 'Failure! agent index:' + str(nagents + 1) )
                    return False
            return True
        return False

    def path_to_action(self, aindx, path):
        actions = []
        cy, cx = self.aindx_cpos[aindx]
        for step in path:
            ty, tx = step[1], step[2]
            if(tx - cx == 1): action = Actions.RIGHT
            elif(tx - cx == -1): action = Actions.LEFT
            elif(ty - cy == 1): action = Actions.DOWN
            elif(ty - cy == -1): action = Actions.UP
            else: action = Actions.WAIT
            # print 'ToAction: ', cy, cx, ty, tx, tt, action
            actions.append(action)
            cy, cx = ty, tx
        return actions

    def is_validpos(self, y, x):
        if x < 0 or x > self.w - 1 or y < 0 or y > self.h - 1:
            return False
        else:
            return True

    # def get_nbor_cells(self, cell_pos):
    #     y, x = cell_pos[0], cell_pos[1]
    #     nbor_cells = []
    #     if(x > 0):
    #         nbor_cells.append((y, x-1))
    #     if(x < self.w - 1):
    #         nbor_cells.append((y, x+1))
    #     if(y > 0):
    #         nbor_cells.append((y-1, x))
    #     if(y < self.h - 1):
    #         nbor_cells.append((y+1, x))
    #     return nbor_cells

    def get_nbor_cells(self, cell_pos):
        nbor_cells = []
        if(len(cell_pos) == 3):
            t, y, x= cell_pos[0], cell_pos[1], cell_pos[2]
            if(t > MAX_STEPS):
                raise EnvironmentError
            if(x > 0):
                nbor_cells.append((t+1, y, x-1))
            if(x < self.w - 1):
                nbor_cells.append((t+1, y, x+1))
            if(y > 0):
                nbor_cells.append((t+1, y-1, x))
            if(y < self.h - 1):
                nbor_cells.append((t+1, y+1, x))
            nbor_cells.append((t+1, y, x))
        elif(len(cell_pos) == 2):
            y, x = cell_pos[0], cell_pos[1]
            if(x > 0):
                nbor_cells.append((y, x-1))
            if(x < self.w - 1):
                nbor_cells.append((y, x+1))
            if(y > 0):
                nbor_cells.append((y-1, x))
            if(y < self.h - 1):
                nbor_cells.append((y+1, x))
            nbor_cells.append((y, x))
        return nbor_cells

    def check_nbors(self, y, x):
        '''
        Return contents of neighbors of given cell
        return: array [ RIGHT, UP, LEFT, DOWN, WAIT ]
        '''
        nbors = np.ones(5, dtype = int ) * INVALID
        # x, y = self.xy_saturate(x, y)
        if(x > 0):
            nbors[Actions.LEFT] = self.cells[y][x-1]
        if(x < self.w - 1):
            nbors[Actions.RIGHT] = self.cells[y][x+1]
        if(y > 0):
            nbors[Actions.UP] = self.cells[y-1][x]
        if(y < self.h - 1):
            nbors[Actions.DOWN] = self.cells[y+1][x]
        nbors[Actions.WAIT] = self.cells[y][x]
        return nbors

    def is_blocked(self, y, x):
        # print 'Cell :', y, x
        if not self.is_validpos(y, x): return True
        if(self.cells[y][x] == IS_ROCK): return True
        return False

    def agent_action(self, aindx, action):
        if(aindx in self.aindx_cpos):
            y, x = self.aindx_cpos[aindx]
        else:
            raise Exception('Agent ' + str(aindx) + ' does not exist!')
        oy, ox = y, x
        nbors = self.check_nbors(y, x)
        # print 'DoAction: ', aindx, y, x, nbors, action,
        if(nbors[action] == UNOCCUPIED):
        # if(nbors[action] != IS_ROCK and nbors[action] != INVALID):
            y += int(action == Actions.DOWN) - int(action == Actions.UP)
            x += int(action == Actions.RIGHT) - int(action == Actions.LEFT)
            self.aindx_cpos[aindx] = (y, x)
            self.cells[oy][ox] = 0
            self.cells[y][x] = aindx
            if(self.visualize): self.visualize.update_agent_vis(aindx)
        elif(action == Actions.WAIT):
            return (-1)
        else:
            # print 'DoAction: ', aindx, y, x, nbors, action
            raise Exception('Cell is not unoccupied! : (' + str(y) + ',' + str(x) + ') --> ' + str(action) )
        return (0) if self.aindx_cpos[aindx] == self.aindx_goal[aindx] else (-1)

    def passable(self, cell, constraints = None):
        retValue = False
        if(len(cell) == 3):
            t, y, x = cell[0], cell[1], cell[2]
            if(self.is_blocked(y,x)):
                retValue = False
            elif(constraints):
                if(cell in constraints):
                    retValue = False
                else:
                    retValue = True
            else:
                retValue = True
            return retValue
        elif(len(cell) == 2):
            y, x = cell[0], cell[1]
            if(self.is_blocked(y,x)):
                retValue = False
            elif(constraints):
                if(cell in constraints):
                    retValue = False
                else:
                    retValue = True
            else:
                retValue = True
            return retValue

    # @staticmethod
    def tyx_dist_heuristic(self, a, b):
        yx_dist = abs(a[1] - b[1]) + abs(a[2] - b[2])
        if(a[0] == ANY_TIME or b[0] == ANY_TIME or yx_dist == 0 ): t_dist = yx_dist
        else: t_dist = abs(a[2] - b[2])
        return yx_dist + t_dist

    def get_size(self):
        return (self.h, self.w)

    def get_agents(self):
        return self.aindx_cpos.keys()
