from gworld import *

# a = GridWorld(6,10, [(2,1),(1,2)] )
a = gworld(5,10)

print a.cells
print a.get_nbors(1,1)
print a.is_blocked(2,1)
print a.is_blocked(1,1)

a.add_agents([ (1,1,3,2), (1,0,2,3) ])

print a.get_nbors(1,1)
print a.is_blocked(2,1)
print a.is_blocked(1,1)
print a.cells

a.agent_action(1, Actions.UP)

print a.get_nbors(1,1)
print a.is_blocked(2,1)
print a.is_blocked(1,1)
print a.cells

a.agent_action(2, Actions.RIGHT)

print a.get_nbors(1,1)
print a.is_blocked(2,1)
print a.is_blocked(1,1)
print a.cells

a.agent_action(3, Actions.UP)

print a.get_nbors(1,1)
print a.is_blocked(2,1)
print a.is_blocked(1,1)
print a.cells
