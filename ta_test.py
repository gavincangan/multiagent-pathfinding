from gworld import *
from visualize import *
import astar

# a = GridWorld(6,10, [(2,1),(1,2)] )
a = GridWorld(5,10)

vis = Visualize(a)

a.add_agents( [ (1,1,2,2) ] ) #, (1,0,2,3)
a.add_rocks( [ (2,1),(1,2),(1,3),(1,4),(3,1),(4,1),(2,3),(3,3),(3,4) ] )

vis.draw_world()
vis.draw_agents()

vis.canvas.pack()
vis.canvas.update()
vis.canvas.after(1000)

path = astar.find_path(a.get_nbor_cells,
              a.aindx_cpos[1],
              a.aindx_goal[1],
              lambda cell: 1,
              lambda cell: not a.is_blocked( cell[0], cell[1] ) )

print path
actions = a.path_to_action(1, path[1:])

print actions

for action in actions:
    a.agent_action(1, action)
    vis.canvas.update()
    vis.canvas.after(1000)

print a.cells
vis.canvas.after(3000)


# a.agent_action(1, Actions.UP)
#
# print a.check_nbors(1,1)
# print a.is_blocked(2,1)
# print a.is_blocked(1,1)
# print a.cells
#
# vis.canvas.pack()
# vis.canvas.update()
# vis.canvas.after(1000)
#
# a.agent_action(2, Actions.RIGHT)
#
# print a.check_nbors(1,1)
# print a.is_blocked(2,1)
# print a.is_blocked(1,1)
# print a.cells
#
# vis.canvas.pack()
# vis.canvas.update()
# vis.canvas.after(1000)
#
# a.agent_action(2, Actions.LEFT)
#
# print a.check_nbors(1,1)
# print a.is_blocked(2,1)
# print a.is_blocked(1,1)
# print a.cells
#
# vis.canvas.pack()
# vis.canvas.update()
# vis.canvas.after(1000)
