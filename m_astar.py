import pqueue

def manhattan_dist(a, b):
    """
    Returns the Manhattan distance between two points.

    >>> manhattan_dist((0, 0), (5, 5))
    10
    >>> manhattan_dist((0, 5), (10, 7))
    12
    >>> manhattan_dist((12, 9), (2, 3))
    16
    >>> manhattan_dist((0, 5), (5, 0))
    10
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def extract_fn(a):
    # print 'a :', a, 'Extract :', a[:-1]
    return a[:-1]

def find_path(neighbour_fn,
              start,
              end,
              cost = lambda pos: 1,
              passable = lambda pos, constraints = None : True,
              heuristic = manhattan_dist,
              constraints = None,
              extract = extract_fn):
    """
    Returns the path between two nodes as a list of nodes using the A*
    algorithm.
    If no path could be found, an empty list is returned.

    The cost function is how much it costs to leave the given node. This should
    always be greater than or equal to 1, or shortest path is not guaranteed.

    The passable function returns whether the given node is passable.

    The heuristic function takes two nodes and computes the distance between the
    two. Underestimates are guaranteed to provide an optimal path, but it may
    take longer to compute the path. Overestimates lead to faster path
    computations, but may not give an optimal path.
    """
    # tiles to check (tuples of (x, y), cost)
    todo = pqueue.PQueue()
    todo.update(start, 0)

    # tiles we've been to
    visited = set()

    # associated G and H costs for each tile (tuples of G, H)
    costs = { start: (0, heuristic(start, end)) }

    # parents for each tile
    parents = {}

    if( heuristic(start, end) == 0):
        return [start]

    while todo and (extract(end) not in visited):
        cur, c = todo.pop_smallest()

        # tcur = cur
        # cur_chain = [cur]
        # while(tcur != start):
        #     cur_chain.append(parents[tcur])
        #     tcur = parents[tcur]
        # print 'Current :', cur, '\tChain: ', cur_chain

        visited.add(extract(cur))

        # check neighbours
        for n in neighbour_fn(cur):
            # skip it if we've already checked it, or if it isn't passable
            if ((extract(n) in visited) or
                (not passable(n, constraints))):
                print 'Nbor: ', n, (not passable(n, constraints)), (extract(n) in visited)
                continue

            if not (n in todo):
                # we haven't looked at this tile yet, so calculate its costs
                g = costs[cur][0] + cost(cur)
                h = heuristic(n, end)
                costs[n] = (g, h)
                parents[n] = cur
                todo.update(n, g + h)
            else:
                # if we've found a better path, update it
                g, h = costs[n]
                new_g = costs[cur][0] + cost(cur)
                if new_g < g:
                    g = new_g
                    todo.update(n, g + h)
                    costs[n] = (g, h)
                    parents[n] = cur
            print 'Visited: ', visited

    # we didn't find a path
    if extract(end) not in visited:
        return []

    # build the path backward
    path = []
    while extract(end) != extract(start):
        path.append(end)
        end = parents[end]
    path.append(start)
    path.reverse()

    return path, len(path)
