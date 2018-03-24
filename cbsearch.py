from macros import *
from gworld import *
from visualize import *
import astar
import m_astar

def get_m_astar_path(world, start, goal, constraints = None):
    ret_path = m_astar.find_path(world.get_nbor_cells,
              start,
              goal,
              lambda cell: 1,
              lambda cell, constraints = None: world.passable( cell, constraints ),
              world.yxt_dist_heuristic,
              constraints)
    return ret_path

def get_astar_path(world, start, goal):
    ret_path = astar.find_path(world.get_nbor_cells,
              start,
              goal,
              lambda cell: 1,
              lambda cell: world.passable( cell ) )
    return ret_path

def spacetime_conv(path_yx, tstart = 0):
    path_yxt = []
    tcurr = tstart
    for step_yx in path_yx:
        step_yxt = ( step_yx[0], step_yx[1], tcurr )
        path_yxt.append(step_yxt)
        tcurr = tcurr + 1
    return (tcurr - tstart), path_yxt

def get_max_pathlen(agents, path_seq):
    for agent in agents:
        pathlen = len(path_seq[agent])
        max_pathlen = pathlen if pathlen > max_pathlen else max_pathlen
    return max_pathlen

def path_equalize(agents, path_seq, max_pathlen = -1):
    if(max_pathlen < 0):
        max_pathlen = get_maxpathlen(agents, path_seq)
    for agent in agents:
        path = path_seq[agent]
        lstep = path[-1]
        for step in range(len(path), max_pathlen + TWAIT):
            path.append( ( lstep[0], lstep[1], step ) )
        path_seq[agent] = path
    return path_seq

def get_conflicts(agents, path_seq):


def search(agents, world):
    path_seq = dict()
    max_pathlen = 0
    for agent in agents:
        start = world.aindx_cpos[agent]
        goal = world.aindx_goal[agent]
        pathlen, path_seq[agent] = spacetime_conv( get_astar_path(world, start, goal) )
        max_pathlen = pathlen if pathlen > max_pathlen else max_pathlen

    path_seq = path_equalize(agents, path_seq, max_pathlen)

    conflicts = get_conflicts(agents, path_seq)

    for agent in agents:
        print 'Agent: ', agent, '  ', path_seq[agent]
