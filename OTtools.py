# Python module for dealing with OT
def warn(warning):
    print(warning)
    return True
    #TODO perhapse made this mutable and add interactive capabilities

class OTobject:
    def __init__(self, value):
        self.id = str(value)
        self.value = value
    def __str__(self):
        return self.id
    #TODO add __repr__

class Candidate(OTobject):
    def foo(self):
        pass

class Constraint(OTobject):
    def foo(self):
        pass

class Tableaux:
    def __init__(self, matrix):
        self.input = matrix[0][0]
        self.violations = [i[1:] for i in matrix[1:]]
        self.constraintSet = [Constraint(i) for i in matrix[0][1:]]
        self.candidateSet = [Candidate(i[0]) for i in matrix[1:]]
        self.constraints = {c: v for c, v in zip(self.constraintSet, self.violations)}
        #self.candidates = {c: v for c, v in zip(self.candidateSet, )}
        self._matrixRows = [[self.input] + [i for i in self.constraintSet]]
        self._matrixRows += [[j] + v for j, v in zip(self.candidateSet, self.violations)]
        #self._matrixColumns = 
    def __str__(self):
        result = [[str(i) for i in j] for j in self._matrixRows]
        return str(result)

foo = Tableaux([[0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14]])

print(foo)
