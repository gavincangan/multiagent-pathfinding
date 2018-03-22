from macros import *
import numpy as np
from world import world
import grid_agent as ga
from Tkinter import *

class Visualize:
    def __init__(self, world_data):
        self.frame = Tk()
        self.canvas = Canvas(self.frame, width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.canvas.grid()
        self.world = world_data
        world_data.visualize = self
        self.cell_h, self.cell_w = self.get_cell_size()
        self.agent_h, self.agent_w = self.get_agent_size(1)
        self.vis_world_ptr = []

    def draw_world(self):
        nrows, ncols = self.world.get_size()
        for row in range(nrows):
            curr_row = []
            for col in range(ncols):
                cell = self.canvas.create_rectangle(FRAME_MARGIN + self.cell_w * col, FRAME_MARGIN + self.cell_h * row, FRAME_MARGIN + self.cell_w * (col+1), FRAME_MARGIN + self.cell_h * (row+1) )
                curr_row.append(cell)
            self.vis_world_ptr.append(curr_row)

    def get_pos_in_cell(self, crow, ccol, index, nagents):
        if(MAX_AGENTS_IN_CELL == 1):
            agent_h = self.agent_h
            agent_w = self.agent_w
            agent_y1 = FRAME_MARGIN + (crow * self.cell_h) + CELL_MARGIN
            agent_y2 = agent_y1 + agent_h
            agent_x1 = FRAME_MARGIN + (ccol * self.cell_w) + CELL_MARGIN
            agent_x2 = agent_x1 + agent_w
        elif(MAX_AGENTS_IN_CELL < 5):
            agent_h, agent_w = self.get_agent_size(MAX_AGENTS_IN_CELL)
            agent_y1 = FRAME_MARGIN + (crow * self.cell_h) + CELL_MARGIN + ((index/2) * (CELL_MARGIN + agent_h))
            agent_y2 = agent_y1 + agent_h
            agent_x1 = FRAME_MARGIN + (ccol * self.cell_w) + CELL_MARGIN + ((index%2) * (CELL_MARGIN + agent_w))
            agent_x2 = agent_x1 + agent_w
        else:
            raise NotImplementedError
        return (agent_y1, agent_x1, agent_y2, agent_x2)

    def draw_agents(self):
        for crow in range(self.world.nrows):
            for ccol in range(self.world.ncols):
                cell = self.world.ptr_map[crow][ccol]
                if(cell):
                    nagents = len(cell)
                    for agent in range(nagents):
                        y1, x1, y2, x2 = self.get_pos_in_cell(crow, ccol, agent, nagents)
                        cell[agent].vis_obj = self.canvas.create_oval(x1, y1, x2, y2, fill=COLORS[cell[agent].aindex])
                        # print gy, gx, self.vis_world_ptr
                        goal_cell = self.vis_world_ptr[cell[agent].gy][cell[agent].gx]
                        self.canvas.itemconfig(goal_cell, outline=COLORS[cell[agent].aindex], width=2)

    def move_agent_vis(self, agent_obj, vis_obj, orow, ocol, crow, ccol):
        ocell = self.world.ptr_map[orow][ocol]
        ncell = self.world.ptr_map[crow][ccol]
        if(ocell):
            nagents = len(ocell)
            for agent in range(nagents):
                y1, x1, y2, x2 = self.get_pos_in_cell(orow, ocol, agent, nagents)
                self.canvas.coords(ocell[agent].vis_obj, x1, y1, x2, y2)
        if(ncell):
            nagents = len(ncell)
            for agent in range(nagents):
                y1, x1, y2, x2 = self.get_pos_in_cell(crow, ccol, agent, nagents)
                self.canvas.coords(ncell[agent].vis_obj, x1, y1, x2, y2)

    def get_cell_size(self):
        avail_h = FRAME_HEIGHT - 2 * FRAME_MARGIN
        avail_w = FRAME_WIDTH - 2 * FRAME_MARGIN
        nrows, ncols = self.world.get_size()
        cell_h = avail_h / nrows
        cell_w = avail_w / ncols
        return (cell_h, cell_w)

    def get_agent_size(self, nagents):
        if(MAX_AGENTS_IN_CELL == 1):
            agent_h = self.cell_h - 2 * CELL_MARGIN
            agent_w = self.cell_w - 2 * CELL_MARGIN
        elif(MAX_AGENTS_IN_CELL < 5):
            agent_h = (self.cell_h - 3 * CELL_MARGIN) / 2
            agent_w = (self.cell_w - 3 * CELL_MARGIN) / 2
        else:
            raise NotImplementedError
        return (agent_h, agent_w)

    def do_loop(self):
        self.frame.mainloop()

    def do_pack(self):
        self.canvas.pack()
