def solve_map_coloring():
    # Australia map with adjacent regions
    map = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'],
        'V': ['SA', 'NSW'],
        'T': []
    }
    
    colors = ['Red', 'Green', 'Blue']
    
    def backtrack(assignment):
        if len(assignment) == len(map):
            return assignment
        
        var = select_unassigned_variable(assignment)
        for color in colors:
            if is_consistent(var, color, assignment, map):
                new_assignment = assignment.copy()
                new_assignment[var] = color
                result = backtrack(new_assignment)
                if result is not None:
                    return result
        return None
    
    def select_unassigned_variable(assignment):
        # MRV heuristic
        unassigned = [v for v in map if v not in assignment]
        return min(unassigned, key=lambda v: len(get_legal_colors(v, assignment, map)))
    
    def get_legal_colors(var, assignment, map):
        used_colors = {assignment[n] for n in map[var] if n in assignment}
        return [c for c in colors if c not in used_colors]
    
    def is_consistent(var, color, assignment, map):
        for neighbor in map[var]:
            if neighbor in assignment and assignment[neighbor] == color:
                return False
        return True
    
    solution = backtrack({})
    
    if solution:
        print("Map coloring solution:")
        for region, color in solution.items():
            print(f"{region}: {color}")
    else:
        print("No solution found")

solve_map_coloring()
