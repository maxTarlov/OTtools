# Python module for dealing with OT
def warn(warning):
    print(warning)
    return True
    #TODO perhapse made this mutable and add interactive capabilities

class Candidate:
    def __init__(self, id):
        self.id = str(id)
    def __str__(self):
        return self.id
    #TODO enrich repr

class Constraint:
    def __init__(self, id):
        self.id = str(id)
    def __str__(self):
        return self.id
    #TODO enrich repr

class Tableaux:
    def __init__(self, matrix):
        self.input = matrix[0][0]
        self.constraints = [Constraint(i) for i in matrix[0][1:]]
        self.candidates = [Candidate(i[0]) for i in matrix[1:]]
        self.violations = [i[1:] for i in matrix[1:]]
        self._matrix = [[self.input] + [i for i in self.constraints]]
        self._matrix += [[j] + v for j, v in zip(self.candidates, self.violations)]
    def __str__(self):
        result = [[str(i) for i in j] for j in self._matrix]
        return str(result)

foo = Tableaux([[0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14]])

print(foo)
