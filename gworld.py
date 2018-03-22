from macros import *
import numpy as np

class GridWorld:
    def __init__(self, h, w, rocks = None, agent_sng = None):
        self.h = h
        self.w = h
        self.cells = np.zeros((h, w), dtype=int)
        self.visualize = None
        self.add_rocks(rocks)
        self.aindx_to_cpos = dict()
        self.aindx_to_gpos = dict()

    def xy_saturate(self, x,y):
        if(x<0): x=0
        if(x>self.w-1): x=self.w-1
        if(y<0): y=0
        if(y>self.h-1): y=self.w-1
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
                nagents = len( self.aindx_to_cpos.keys() )
                if(not self.is_blocked(sy, sx) and not self.is_blocked(gy, gx)):
                    if(self.cells[sy][sx] == UNOCCUPIED):
                        self.aindx_to_cpos[nagents + 1] = (sy, sx)
                        self.cells[sy][sx] = nagents + 1
                        self.aindx_to_gpos[nagents + 1] = (gy, gx)
                    else:
                        raise Exception('Cell has already been occupied!')
                else:
                    print 'Failure! agent index:' + str(nagents + 1)
                    return False
            return True
        return False

    def is_validpos(self, y, x):
        if x < 0 or x > self.w - 1 or y < 0 or y > self.h - 1:
            return False
        else:
            return True

    def get_nbors(self, y, x):
        '''
        Return neighbors of given cell
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
        if not self.is_validpos(y, x): return True
        if(self.cells[y][x] == IS_ROCK): return True
        return False

    def agent_action(self, aindx, action):
        if(aindx in self.aindx_to_cpos.keys()):
            y, x = self.aindx_to_cpos[aindx]
        else:
            raise Exception('Agent ' + str(aindx) + ' does not exist!')
        oy, ox = y, x
        nbors = self.get_nbors(y, x)
        if(nbors[action] == UNOCCUPIED):
            y += int(action == Actions.DOWN) - int(action == Actions.UP)
            x += int(action == Actions.RIGHT) - int(action == Actions.LEFT)
            self.aindx_to_cpos[aindx] = (y, x)
            self.cells[oy][ox] = 0
            self.cells[y][x] = aindx
        else:
            raise Exception('Cell is not unoccupied!')
        return 0 if

    def get_size(self):
        return (self.h, self.w)
