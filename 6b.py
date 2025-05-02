class CrosswordCSP:
    def __init__(self, variables, domains, overlaps):
        self.variables = variables
        self.domains = domains
        self.overlaps = overlaps  # (var1, var2): (i, j) means var1[i] == var2[j]
        self.assignment = {}

    def is_consistent(self, var, word):
        for other_var in self.assignment:
            if var == other_var:
                continue
            if (var, other_var) in self.overlaps:
                i, j = self.overlaps[(var, other_var)]
                if word[i] != self.assignment[other_var][j]:
                    return False
            elif (other_var, var) in self.overlaps:
                j, i = self.overlaps[(other_var, var)]
                if word[i] != self.assignment[other_var][j]:
                    return False
        return True

    def backtrack(self):
        if len(self.assignment) == len(self.variables):
            return self.assignment

        unassigned_vars = [v for v in self.variables if v not in self.assignment]
        var = unassigned_vars[0]

        for word in self.domains[var]:
            if self.is_consistent(var, word):
                self.assignment[var] = word
                result = self.backtrack()
                if result:
                    return result
                del self.assignment[var]
        return None

# Variables
variables = ['H1', 'H2', 'V1', 'V2']

# Domains (word list of length 3)
word_list = ['CAT', 'DOG', 'RAT', 'MAT', 'CAR', 'BAR']
domains = {v: word_list for v in variables}

# Overlap constraints: (var1, var2): (i, j)
# H1[0] == V1[0], H1[2] == V2[0], H2[0] == V1[2], H2[2] == V2[2]
overlaps = {
    ('H1', 'V1'): (0, 0),
    ('H1', 'V2'): (2, 0),
    ('H2', 'V1'): (0, 2),
    ('H2', 'V2'): (2, 2),
}

# Solve
csp = CrosswordCSP(variables, domains, overlaps)
solution = csp.backtrack()

# Display
if solution:
    for var in sorted(solution):
        print(f"{var}: {solution[var]}")
else:
    print("No solution found.")
