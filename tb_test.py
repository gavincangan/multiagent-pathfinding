from gworld import *
from visualize import *
import m_astar

a = GridWorld(5,10)

vis = Visualize(a)

a.add_rocks( [ (2,1),(1,2),(1,3),(1,4),(3,1),(4,1),(2,3),(3,3),(3,4) ] )
a.add_agents( [ (1,1,4,2), (1,0,2,2) ] )

vis.draw_world()
vis.draw_agents()

vis.canvas.pack()
vis.canvas.update()
vis.canvas.after(500)

agents = a.get_agents()

agent_seq = { 1:[], 2:[] }

conflict = False

max_path = 0

start_time = 0

constraints = []

for agent in agents:
    cpos = a.aindx_cpos[agent]
    goal = a.aindx_goal[agent]
    path = m_astar.find_path(a.get_nbor_cells,
                  (cpos[0], cpos[1], start_time),
                  (goal[0], goal[1], ANY_TIME),
                  lambda cell: 1,
                  lambda cell: a.passable( cell ),
                  a.yxt_dist_heuristic,
                  constraints )

    for cell in path:
        if( not cell in a.yxt_res ):
            a.yxt_res[ cell ] = agent
        else:
            constraints.append(cell)
            conflict = True
            print 'Conflict!'

    if not conflict:
        print 'Path [',agent,']: ',path
        if(len(path) > max_path): max_path = len(path)
        agent_seq[agent] = a.path_to_action(agent, path[1:])
        print 'Actions :', agent_seq[agent]

for step in range(max_path - 1):
    for agent in agents:
        if( agent_seq[agent] ):
            action = agent_seq[agent].pop(0)
            a.agent_action(agent, action)
            vis.canvas.update()
            vis.canvas.after(150)
    vis.canvas.update()
    vis.canvas.after(500)

vis.canvas.update()
vis.canvas.after(5000)
