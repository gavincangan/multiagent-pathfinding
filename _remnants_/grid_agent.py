#!/usr/bin/env python
from macros import *
from builtins import object
import numpy as np
from collections import deque
import world

class CentralizedAgent:
    def_move_actions = (AgentActions.WAIT, AgentActions.UP, AgentActions.DOWN, AgentActions.LEFT, AgentActions.RIGHT)
    def_obs_actions = (Quadrants.QUAD1, Quadrants.QUAD2, Quadrants.QUAD3, Quadrants.QUAD4)
    comm_actions = range(MSG_LIMITLOWER, MSG_LIMITUPPER + 1)
    agent_count = 0
    agent_by_index = dict()
    verbose = True
    def __init__(self, world_obj, y, x, gy, gx):
        self.world_act = world_obj
        self.obs_map = np.ones_like(world_obj.occ_map)
        self.y = INVALID
        self.x = INVALID
        self.gy = gy
        self.gx = gx
        self.reachedGoal = False
        self.aindex = CentralizedAgent.agent_count
        self.states = (self.x, self.y, self.obs_map)
        self.vis_obj = 0
        self.world_act.add_agent(self, y, x, gy, gx)
        CentralizedAgent.agent_by_index[CentralizedAgent.agent_count] = self
        CentralizedAgent.agent_count +=1

    @staticmethod
    def __move_cmd_to_vector__(move_cmd):
        dy = 0
        dx = 0
        if(move_cmd == AgentActions.UP):
            dy = -MOVE_SPEED
        elif(move_cmd == AgentActions.DOWN):
            dy = MOVE_SPEED
        elif(move_cmd == AgentActions.LEFT):
            dx = -MOVE_SPEED
        elif(move_cmd == AgentActions.RIGHT):
            dx = MOVE_SPEED
        else:
            pass
        return (dy, dx)

    # Represent the view of the agewnt in matrix indices
    # => Q1 has a negative dy, for example
    @staticmethod
    def __quadrant_to_dxdy__(quadrant):
        if(quadrant == 1):
            dx = SENSE_RANGE
            dy = -SENSE_RANGE
        elif(quadrant == 2):
            dx = -SENSE_RANGE
            dy = -SENSE_RANGE
        elif(quadrant == 3):
            dx = -SENSE_RANGE
            dy = SENSE_RANGE
        else: #(quadrant == 4)
            dx = SENSE_RANGE
            dy = SENSE_RANGE
        return (dy, dx)

    def move(self, move_cmd):
        # 0 - wait, 1 - up, 2 - down
        # 3 - left, 4 - right
        if(move_cmd in self.get_move_actions()):
            wnrows, wncols = self.world_act.get_size()
            (dy, dx) = self.__move_cmd_to_vector__(move_cmd)
            # print 'dy:', dy, ' dx:', dx
            new_y = (self.y + dy) % wnrows
            new_x = (self.x + dx) % wncols
            # print 'New position: ', new_y, new_x
            self.update_position(new_y, new_x)
            if(self.x == self.gx and self.y == self.gy):
                self.reachedGoal = True
        else:
            print 'Error! Cmd:', move_cmd, 'PosYX:', self.y, self,x
            raise EnvironmentError

    def __str__(self):
        return('#' + str(self.aindex) + ' @ (' + str(self.y) + ', ' + str(self.x) + ') -> (' + str(self.gy) + ', ' + str(self.gx)+ ')')

    def update_position(self, pos_y, pos_x):
        old_x = self.x
        old_y = self.y
        self.x = pos_x
        self.y = pos_y
        if not(old_x == self.x and old_y == self.y):
            if (old_x >= 0 and old_x < self.world_act.ncols and old_y >= 0 and old_y < self.world_act.nrows):
                self.world_act.occ_map[old_y][old_x] -= 1
                self.world_act.ptr_map[old_y][old_x].remove(self)
            self.world_act.occ_map[self.y][self.x] += 1
            self.world_act.ptr_map[self.y][self.x].append(self)
            if(self.vis_obj):
                self.world_act.visualize.move_agent_vis(self, self.vis_obj, old_y, old_x, pos_y, pos_x)

    def get_move_actions(self):
        ret_moveactions = []
        ymin, xmin = 0, 0
        ysize, xsize = self.world_act.get_size()
        xmax = xsize - 1
        ymax = ysize - 1
        if(self.x < xmax - MOVE_SPEED + 1):
            next_cell = self.world_act.ptr_map[self.y][self.x + MOVE_SPEED]
            if(not next_cell):
                ret_moveactions.append(AgentActions.RIGHT)
        if(self.x > xmin + MOVE_SPEED - 1):
            next_cell = self.world_act.ptr_map[self.y][self.x - MOVE_SPEED]
            if(not next_cell):
                ret_moveactions.append(AgentActions.LEFT)
        if(self.y < ymax - MOVE_SPEED + 1):
            next_cell = self.world_act.ptr_map[self.y + MOVE_SPEED][self.x]
            if(not next_cell):
                ret_moveactions.append(AgentActions.DOWN)
        if(self.y > ymin + MOVE_SPEED - 1):
            next_cell = self.world_act.ptr_map[self.y - MOVE_SPEED][self.x]
            if(not next_cell):
                ret_moveactions.append(AgentActions.UP)
        # print '##RM:', ret_moveactions, self.y, self.x
        return ret_moveactions
