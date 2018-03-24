from macros import *
from gworld import *
from visualize import *
import astar
import m_astar

conflicts = dict()

path_seq = dict()
yxt_reserve = dict()

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

def search(agents, world):
    path_maxlen = 0
    for agent in agents:
        start = world.aindx_cpos[agent]
        goal = world.aindx_goal[agent]
        # print 'QQ: ', agent, start, goal
        path_seq[agent] = get_astar_path(world, start, goal)

    for agent in agents:
        path_len = len(path_seq[agent])
        path_maxlen = path_len if (path_len > path_maxlen) else path_maxlen

    for agent in agents:
        path_len = len(path_seq[agent])
        if(path_len < path_maxlen + TERMINAL_WAIT):
            last_step = path_seq[agent][-1]
            for tstep in range(path_len, path_maxlen + TERMINAL_WAIT):
                tcell = (last_step[0], last_step[1], tstep)
                path_seq[agent].append( tcell )

    for agent in agents:
        path_yxt = []
        for t, step in enumerate(path_seq[agent]):
            tcell = ( step[0], step[1], t )
            path_yxt.append(tcell)
            if( tcell not in yxt_reserve ):
                yxt_reserve[tcell] = agent
            else:
                other_agent = yxt_reserve[tcell]
                if(other_agent != agent):
                    if( agent in conflicts):
                        conflicts[agent].append(tcell)
                    else:
                        conflicts[agent] = [tcell]
                    if(other_agent in conflicts):
                        if(tcell not in conflicts[other_agent]):
                            conflicts[other_agent].append(tcell)
                    else:
                        conflicts[other_agent] = [tcell]
        path_seq[agent] = path_yxt

    iter_count = 0
    tree_block = []
    while(True):
        iter_count = iter_count + 1
        for agent in agents:
            if not tree_block:
                conflicts[agent] = []
            for tcell in path_seq[agent]:
                if( tcell not in yxt_reserve ):
                    yxt_reserve[tcell] = agent
                else:
                    other_agent = yxt_reserve[tcell]
                    if(other_agent != agent):
                        if( agent in conflicts):
                            if(tcell not in conflicts[agent]):
                                conflicts[agent].append(tcell)
                        else:
                            conflicts[agent] = [tcell]
                        if(other_agent in conflicts):
                            if(tcell not in conflicts[other_agent]):
                                conflicts[other_agent].append(tcell)
                        else:
                            conflicts[other_agent] = [tcell]

        for agent in agents:
            addconflicts = []
            for conflict in conflicts[agent]:
                ty, tx, tt = conflict[0], conflict[1], conflict[2]
                if(tt > 0):
                    movedist = world.yxt_dist_heuristic(conflict, path_seq[agent][tt-1] )
                    while(movedist == 0):
                        addconflicts.append(path_seq[agent][tt-1])
                        tt = tt - 1
                        movedist = world.yxt_dist_heuristic(conflict, path_seq[agent][tt-1] )
                    if(tree_block):
                        if(agent not in tree_block and agent in conflicts):
                            for conflict in conflicts[agent]:
                                tt = conflict[2]
                                if(path_seq[agent][tt-1] not in addconflicts):
                                    addconflicts.append(path_seq[agent][tt-1])
            for conflict in addconflicts:
                if(conflict not in conflicts[agent]):
                    conflicts[agent].append(conflict)

        print 'Iter: ', iter_count, 'conflicts: ', conflicts
        tree_block = []
        for agent in agents:
            if(conflicts[agent]):
                tmin_conflict = MAX_STEPS
                for conflict in conflicts[agent]:
                    if(conflict[2] < tmin_conflict): tmin_conflict = conflict[2]
                olpath = path_seq[agent]
                # print tmin_conflict, olpath
                start = olpath[tmin_conflict - 1]
                goal_yx = world.aindx_goal[agent]
                goal = (goal_yx[0], goal_yx[1], ANY_TIME)
                constraints = conflicts[agent]
                nwpath = get_m_astar_path(world, start, goal, constraints)
                if not nwpath:
                    tree_block.append(agent)
                for step in olpath[tmin_conflict-1:]:
                    if step in yxt_reserve:
                        if(yxt_reserve[step] == agent):
                            del yxt_reserve[step]
                fullpath = olpath[:tmin_conflict - 1]
                for step in nwpath:
                    fullpath.append(step)
                path_seq[agent] = fullpath

        for agent in agents:
            path_len = len(path_seq[agent])
            path_maxlen = path_len if (path_len > path_maxlen) else path_maxlen

        for agent in agents:
            path_len = len(path_seq[agent])
            if(path_len < path_maxlen + TERMINAL_WAIT):
                last_step = path_seq[agent][-1]
                for tstep in range(path_len, path_maxlen + TERMINAL_WAIT):
                    tcell = (last_step[0], last_step[1], tstep)
                    path_seq[agent].append( tcell )

        break_loop = True
        for agent in agents:
            if(conflicts):
                if(conflicts[agent]):
                    break_loop = False
                    print '\nConflicts exist: ', iter_count
                    print 'I:', iter_count,' A', agent, ': ', conflicts[agent], '\n'

        if(break_loop):
            print '\nBreaking while loop: ', iter_count, conflicts
            break

    for agent in agents:
        print '\n\nA:', agent, ' :: ', path_seq[agent]

    # print 'Conflicts: ', conflicts

    return path_seq
