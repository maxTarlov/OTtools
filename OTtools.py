# Python module for dealing with OT
def warn(warning):
    print(warning)
    return True
    #TODO perhapse made this mutable and add interactive capabilities

class OTobject:
    """Metaclass for expected contents of a Tableaux instance
    
    Ensures that contents of a Tableaux instance support string casting

    Attrabutes:
        value (any): python representation of the object.
        id (str): string representation of the object.
    """

    def __init__(self, value):
        """Initializes new OTobject instance
        
        Parameter: value (any): representation of the object.
            Must be castable to str
        """
        self.id = str(value)
        self.value = value
    
    def __str__(self):
        return self.id
    #TODO add __repr__

class Candidate(OTobject):
    """Extends OTobject

    Nothing extra yet.
    """
    def foo(self):
        pass

class Constraint(OTobject):
    """Extends OTobject

    Nothing extra yet.
    """
    def foo(self):
        pass

class Tableaux:
    """
    """
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

class OTsystem:
    def __init__(self, data):
        #TODO Check that data has desired properties
        # _data and _keys may not be necessary
        self._data = data
        self._keys = [i.input for i in self._data]
        self._map = {x: y for x, y in zip(self._keys, self._data)}
    def __getitem__(self, key):
        return self._map[key]
    @classmethod
    def fromOTW(cls, filepath):
        pass


foo = Tableaux([[0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14]])

print(OTsystem([foo]))
