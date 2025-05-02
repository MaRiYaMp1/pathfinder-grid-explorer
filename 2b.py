from collections import deque

def waterJugSolverBFS(jug1, jug2, aim):
    queue = deque([(0, 0)])
    visited = set([(0, 0)])
    parents = {}

    while queue:
        current_state = queue.popleft()
        amt1, amt2 = current_state

        if amt1 == aim or amt2 == aim:
            steps = []
            while current_state != (0, 0):
                steps.append(current_state)
                current_state = parents[current_state]
            steps.append((0, 0))
            steps.reverse()
            return steps

        next_states = [
            (jug1, amt2),  
            (amt1, jug2),  
            (0, amt2),     
            (amt1, 0),     
            (min(jug1, amt1 + amt2), max(0, amt1 + amt2 - jug1)),  
            (max(0, amt1 + amt2 - jug2), min(jug2, amt1 + amt2))   
        ]

        for state in next_states:
            if state not in visited:
                queue.append(state)
                visited.add(state)
                parents[state] = current_state

    return None

# Example usage:
jug1_capacity = 5
jug2_capacity = 3
desired_quantity = 4

solution = waterJugSolverBFS(jug1_capacity, jug2_capacity, desired_quantity)
if solution:
    for step in solution:
        print(step)
else:
    print("No solution found.")
