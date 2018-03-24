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
              world.tyx_dist_heuristic,
              constraints)
    return ret_path

def get_astar_path(world, start, goal):
    ret_path, pathcost = astar.find_path(world.get_nbor_cells,
                                          start,
                                          goal,
                                          lambda cell: 1,
                                          lambda cell: world.passable( cell ) )
    return ret_path, pathcost

def path_spacetime_conv(path_yx, tstart = 0):
    path_tyx = []
    tcurr = tstart
    for step_yx in path_yx:
        step_tyx = ( tcurr, step_yx[0], step_yx[1] )
        path_tyx.append(step_tyx)
        tcurr = tcurr + 1
    return (tcurr - tstart), path_tyx

def cell_spacetime_conv(cell, t):
    return ( (t, cell[0], cell[1]) )

def get_max_pathlen(agents, path_seq):
    max_pathlen = 0
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
            path.append( ( step, lstep[1], lstep[2] ) )
        path_seq[agent] = path
    return path_seq

def steptime_agtb(a, b):
    if(a[0] > b[0]): return True
    return False

def get_conflicts(agents, path_seq, conflicts_db = None):
    tyx_map = dict()
    if(not conflicts_db):
        conflicts_db = dict()
    for agent in agents:
        if(agent not in conflicts_db):
            conflicts_db[agent] = []
        for step in path_seq[agent]:
            if(step not in tyx_map):
                tyx_map[step] = agent
            else:
                otheragent = tyx_map[step]
                conflicts_db[agent] = step
                if(conflicts_db[otheragent]):
                    otherconflict = conflicts_db[otheragent]
                    if( steptime_agtb(otherconflict, step) ):
                        conflicts_db[otheragent] = step
                else:
                    conflicts_db[otheragent] = step
    return conflicts_db

def search(agents, world):
    path_seq = dict()
    pathcost = dict()
    agent_goal = dict()
    max_pathlen = 0
    for agent in agents:
        start = world.aindx_cpos[agent]
        goal = world.aindx_goal[agent]
        pathseq_yx, pathcost[agent] = get_astar_path(world, start, goal)
        pathlen, path_seq[agent] = path_spacetime_conv( pathseq_yx )
        max_pathlen = pathlen if pathlen > max_pathlen else max_pathlen


    conflicts_db = get_conflicts(agents, path_seq)
    while(True):
        max_pathlen = get_max_pathlen(agents, path_seq)
        path_seq = path_equalize(agents, path_seq, max_pathlen)

        for agent in agents:
            if agent in conflicts_db:
                constraints = conflicts_db[agent]
                start = cell_spacetime_conv(world.aindx_cpos[agent], 0)
                goal = cell_spacetime_conv(world.aindx_goal[agent], max_pathlen)
                path_seq[agent], mpathcost = get_m_astar_path(world, start, goal, constraints)

        conflicts_db = get_conflicts(agents, path_seq, conflicts_db)

        break_loop = True
        for agent in agents:
            if(conflicts_db[agent]):
                break_loop = False

    for agent in agents:
        print '\nAgent ', agent, ' cost:',pathcost[agent], ' Path -- ', path_seq[agent]

    for agent in agents:
        if agent in conflicts_db:
            print '\nAgent ', agent, ' Conflicts -- ', conflicts_db[agent]
