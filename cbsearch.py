from macros import *
from gworld import *
from visualize import *
import astar
import m_astar
import random

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

def tplusone(step):
    return ( (step[0]+1, step[1], step[2]) )

def get_conflicts(agents, path_seq, conflicts_db = None):
    tyx_map = dict()
    if(not bool(conflicts_db)):
        conflicts_db = dict()
    random.shuffle(agents)
    for agent in agents:
        if(agent not in conflicts_db):
            conflicts_db[agent] = set()
        if(path_seq[agent]):
            pathlen = len(path_seq[agent])
            for t, tstep in enumerate(path_seq[agent]):
                twosteps = [tstep] #, tplusone(tstep)]
                if(t > 0 ): twosteps.append( tplusone(path_seq[agent][t-1]) )
                for step in twosteps:
                    # print 'bTYXMap: ', tyx_map
                    if(step not in tyx_map):
                        tyx_map[step] = agent
                    else:
                        otheragent = tyx_map[step]
                        if(step not in conflicts_db[agent] and agent!=otheragent):
                            conflicts_db[agent].update( {step} )
                            # if(t > 0): conflicts_db[agent].update( { tplusone( path_seq[agent][t-1] ) } )
                        # if(bool(conflicts_db[otheragent])):
                        #     otherconflict = conflicts_db[otheragent]
                        #     # if( steptime_agtb(otherconflict, step) ):
                        #     if(step not in conflicts_db[otheragent]):
                        #         conflicts_db[otheragent].update( {step} )
                        # else:
                        #     conflicts_db[otheragent].update( {step} )
                    # print 'bTYXMap: ', tyx_map
    return conflicts_db

def evaluate_path(path_seq, agent, conflicts_db):
    all_okay = True
    tpath = path_seq[agent]
    tconstraints = conflicts_db[agent]
    for constraint in tconstraints:
        if(constraint in tpath):
            all_okay = False

def search(agents, world):
    path_seq = dict()
    pathcost = dict()
    agent_goal = dict()
    max_pathlen = 0
    restart_loop = False

    for agent in agents:
        start = world.aindx_cpos[agent]
        goal = world.aindx_goal[agent]
        pathseq_yx, pathcost[agent] = get_astar_path(world, start, goal)
        pathlen, path_seq[agent] = path_spacetime_conv( pathseq_yx )
        max_pathlen = pathlen if pathlen > max_pathlen else max_pathlen

    conflicts_db = get_conflicts(agents, path_seq)

    iter_count = 1
    pickd_agents = []
    while(True): # iter_count < 5):
        max_pathlen = get_max_pathlen(agents, path_seq)
        path_seq = path_equalize(agents, path_seq, max_pathlen)

        if(iter_count % 2 == 1):
            pickd_agents = []
            nagents = len(agents)
            random.shuffle(agents)
            pickd_agents = agents[(nagents/2):]
        else:
            temp_pickd_agents = []
            for agent in agents:
                if agent not in pickd_agents:
                    temp_pickd_agents.append(agent)
            pickd_agents = temp_pickd_agents

        if(restart_loop):
            restart_loop = False
            print '\n\nStuck between a rock and a hard place?\nRapid Random Restart to the rescue!\n\n'
            # something = input('Press 1 + <Return> to continue...')
            for agent in agents:
                conflicts_db[agent] = set()
                start = world.aindx_cpos[agent]
                goal = world.aindx_goal[agent]
                pathseq_yx, pathcost[agent] = get_astar_path(world, start, goal)
                pathlen, path_seq[agent] = path_spacetime_conv( pathseq_yx )
                max_pathlen = pathlen if pathlen > max_pathlen else max_pathlen

        conflicts_db = get_conflicts(agents, path_seq, conflicts_db)

        for agent in pickd_agents:
            if (agent in conflicts_db):
                constraints = conflicts_db[agent]
                constraints.update({})
                if(bool(constraints)):
                    start = cell_spacetime_conv(world.aindx_cpos[agent], 0)
                    goal = cell_spacetime_conv(world.aindx_goal[agent], SOMETIME)
                    print 'Agent',agent,': S',start, ' G', goal, '\n\t  C', constraints, '\n\t  OP', path_seq[agent]
                    nw_path, nw_pathlen = get_m_astar_path(world, start, goal, constraints)
                    if(nw_path):
                        path_seq[agent] = nw_path
                        evaluate_path(path_seq, agent, conflicts_db)
                    else:
                        path_seq[agent] = [start]
                        restart_loop = True
                    print 'Agent',agent,': S',start, ' G', goal, '\n\t  C', constraints, '\n\t  NP', nw_path, 'Len: ', nw_pathlen

        if not restart_loop:
            path_seq = path_equalize(agents, path_seq, SOMETIME)
            conflicts_db = get_conflicts(agents, path_seq, conflicts_db)

        break_loop = True
        for agent in agents:
            ubrokn_conflicts = []
            constraints = conflicts_db[agent]
            for step in path_seq[agent]:
                if(step in constraints):
                    ubrokn_conflicts.append(step)
            if(ubrokn_conflicts):
                print '## A', agent, 'UC:', ubrokn_conflicts
                print 'Yes, there are conflicts!'
                break_loop = False
            goal = cell_spacetime_conv(world.aindx_goal[agent], SOMETIME)
            if(path_seq[agent][-1] != goal):
                break_loop = False
        iter_count = iter_count + 1

        if(break_loop and not restart_loop):
            print 'Loop break!'
            break

        # something = input('Press any key to continue...')

    for agent in agents:
        print '\nAgent ', agent, ' cost:',pathcost[agent], ' Path -- ', path_seq[agent]

    for agent in agents:
        if agent in conflicts_db:
            print '\nAgent ', agent, ' Conflicts -- ', conflicts_db[agent]

    return path_seq
