from gworld import *
from visualize import *
import m_astar
import cbsearch as cbs

def get_m_astar_path(world, start, goal, constraints = None):
    ret_path = m_astar.find_path(world.get_nbor_cells,
              start,
              goal,
              lambda cell: 1,
              lambda cell, constraints : world.passable( cell, constraints ),
              world.yxt_dist_heuristic,
              constraints)
    return ret_path

## Go around block. Wait aside for agent1 to pass
## Takes too long. Need better conflict handling
# a = GridWorld(6,10)
# a.add_rocks( [ (2,1),(1,2),(1,3),(1,4),(3,1),(2,3),(3,3),(3,4) ] )
# a.add_agents( [ (1,0,3,2), (1,1,2,2) ] )

## 2 agents. Narrow path with a open slot on the wall
## Waits too long. Need better conflict handling
a = GridWorld(6,10)
a.add_rocks( [ (1,0),(1,1),(1,2),(1,3),(1,4),(2,5),(1,6),(1,7),(1,8),(1,9),(0,9) ] )
a.add_agents( [ (0,0,0,8), (0,1,0,7) ] )

## 3 agents. Few rocks. More space to swerve around
# a = GridWorld(6,10)
# a.add_rocks( [ (4,0),(4,1),(4,2),(1,7),(1,8),(1,9) ] )
# a.add_agents( [ (0,7,5,1), (5,3,0,9), (0,3,5,9) ] )

## 3 agents. Single passable block
# a = GridWorld(6,10)
# a.add_rocks( [ (4,0),(4,1),(4,2),(4,3),(4,4),(3,4),(1,6),(1,7),(1,8),(1,9) ] )
# a.add_agents( [ (0,7,5,1), (5,3,0,9), (0,3,5,9) ] )

## 4 agents. Few rocks. More space to swerve around
## Need better conflict handling for an optimal path
# a = GridWorld(6,10)
# a.add_rocks( [ (4,0),(4,1),(4,2),(1,7),(1,8),(1,9) ] )
# a.add_agents( [ (0,7,5,1), (5,3,0,9), (0,3,5,9), (3,0,3,9) ] )


vis = Visualize(a)

vis.draw_world()
vis.draw_agents()

vis.canvas.pack()
vis.canvas.update()
vis.canvas.after(500)

agents = a.get_agents()

conflict = False

path_maxlen = 0

constraints = []


# cpos = a.aindx_cpos[agent]
# goal = a.aindx_goal[agent]
# start_cell = (cpos[0], cpos[1], 0)
# goal_cell = (goal[0], goal[1], ANY_TIME)

path_seq = dict()

path_seq = cbs.search(agents, a)

# path_seq[1] = [(0,7),(0,6]

action_seq = dict()

for agent in agents:
    path_len = len(path_seq[agent])
    path_maxlen = path_len if (path_len > path_maxlen) else path_maxlen
    action_seq[agent] = a.path_to_action(agent, path_seq[agent])

something = input('Press 2 + <Return> to continue...')

for step in range(path_maxlen):
    for agent in agents:
        # print 'ActSeq: ', agent, action_seq[agent]
        if( action_seq[agent] ):
            action = action_seq[agent].pop(0)
            a.agent_action(agent, action)
            vis.canvas.update()
            vis.canvas.after(150)
    vis.canvas.update()
    vis.canvas.after(500)

vis.canvas.update()
vis.canvas.after(5000)
