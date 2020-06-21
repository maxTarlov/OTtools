# Python module for dealing with OT
def warn(warning):
    print(warning)
    return True
    #TODO perhapse made this mutable and add interactive capabilities

class OTobject:
    """Metaclass for expected contents of a Tableau instance
    
    Ensures that contents of a Tableau instance support string casting

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
    TODO: Add property self.optimal and 
    """
    def foo(self):
        pass

class Constraint(OTobject):
    """Extends OTobject

    Nothing extra yet.
    """
    def foo(self):
        pass

class Tableau:
    """Datatype for an OT violation Tableau

    Properties:
        input (any): input to the tableau
        violations (list): 2D array of violation counts
        constraintSet (list): Constraint objects in the tableau
        constraints (dict): constraint : violations for constraint
        candidateSet (list): Candidate objects in the tableau
        TODO:
        candidates (dict): candidate : violations for candidate
        _matrixColumns (list)
        test _matrixRows
    """

    def __init__(self, matrix):
        """Default Tableau constructor

        Parameter: matrix (list): expected form:
        [[input,     constraint1, ... constraintN],
         [candiateA, violations,  ... violations],
         :
         :
         [candidateN, violations, ... violations]
        ]
        """
        self.input = matrix[0][0]
        self.violations = [i[1:] for i in matrix[1:]]
        self.constraintSet = [Constraint(i) for i in matrix[0][1:]]
        self.candidateSet = [Candidate(i[0]) for i in matrix[1:]]
        #this might need to be cast to a string:
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
        """OTsystem constructor that accepts csv file in OTWorkplace layout

        Parameter: filepath (str): path of the OTW file

        Expected layout of file:
            '', ...
            '',       '', '',           'constraint1', 'constraint2', ...
            'input1', 'candidateA', '', 'violations',  'violations',  ...
            '',       'candidateB', '', 'violations',  'violations',  ...
            :
            :
            'inputN', 'candidateA', '', 'violations',  'violations',  ...
            :
            :
            newline
        
        TODO: add csv reading options, add support for optima
        """

        import csv
        
        matricies = []

        with open(filepath) as csv_file:
            csv_reader = list(csv.reader(csv_file))
            constraintSet = csv_reader[1][3:]
            this_matrix = [[csv_reader[2][0]] + constraintSet]
            this_matrix.append([csv_reader[2][1]] + csv_reader[2][3:])

            for row in csv_reader[3:]:
                if len(row[0]):
                    matricies.append(this_matrix)
                    this_matrix = [[row[0]] + constraintSet]
                this_matrix.append([row[1]] + row[3:])

        tableaux = [Tableau(i) for i in matricies]
        return cls(tableaux)

foo = Tableau([[0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14]])

bar = OTsystem.fromOTW('shortVT.csv')
print(bar['[[workers] [helped]]'])
