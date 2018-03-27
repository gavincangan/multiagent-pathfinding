# ECE6405 Autonomous Coordination

Implementation of Multi-Agent Path Finding in a gridworld simulation.

- Find independent paths for each agent without considering other agents
    - Uses space-time A* for low-level search.
- Make reservations in a space-time reservation table
- Check all paths against the table for conflicts with other agents.
- When a conflict is found, add a constraint to the agent's low-level path planning and re-plan.

- To avoid agents passing right through each other, currently each agent makes multiple reservations in the reservation table.
- This sometimes causes a noticeable delay, where one or more agents may end up waiting in their location although a path is clearly  available.
- To fix this, I need to be able to add two different sorts of constraints as in the original Conflict Based Search paper - for vertext collisions and edge collisions.

- Link to YouTube video: https://youtu.be/b5KMm729b_4

--
The priority queue in A* is from a gridworld simluator on GitHub: https://github.com/TheLastBanana
And implementation of A* is based on an implementation in the same repository.
