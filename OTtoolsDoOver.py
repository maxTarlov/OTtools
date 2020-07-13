# Restarting OTtools
import unittest

class TableauObject:
    def __str__(self):
        return str(self.value)

class Candidate(TableauObject):
    def __init__(self, value, violations):
        self.value = value
        self.violations = [int(v) for v in violations]

class Constraint(TableauObject):
    def __init__(self, value, candidates, index):
        self.value = value
        self.candidates = candidates
        self.violations = {str(c): c.violations[index] for c in candidates}

class Tableau:
    def __init__(self, input, constraints, candidates):
        self.input = input
        self.candidates = candidates
        _conLen = len(constraints)
        self.constraints = [Constraint(constraints[i], candidates, i) for i in range(_conLen)]

    @classmethod
    def fromMatrix(cls, matrix):
        input = matrix[0][0]
        constraints = matrix[0][1:]
        candidates = [Candidate(c[0], c[1:]) for c in matrix[1:]]
        return cls(input, constraints, candidates)

    def getConstraintList(self):
        return [str(c) for c in self.constraints]

class LEG(Tableau):
    @classmethod
    def fromTableau(cls, tableau):
        return cls(tableau.input, tableau.constraints, tableau.candidates)
    
    def filter(self):
        constraint = self.constraints[0]
        minimum = min(constraint.violations)
        passing = []
        for x in zip(constraint.candidates, constraint.violations):
            if x[1] == minimum:
                passing.append(x[0])
        if len(self.constraints) > 1 and len(passing) > 1:
            return LEG(self.input, self.constraints[1:], passing).filter()
        else:
            return passing

class OTsystem:
    def getConstraintList(self):
        return self.tableaux[0].getConstraintList()

    def __init__(self, tableaux):
        self.tableaux = tableaux
        for t in self.tableaux:
            #maybe this should be value instead of string
            assert t.getConstraintList() == self.getConstraintList()

    @classmethod
    def fromOTW(cls, filepath):
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

            matricies.append(this_matrix)

        tableaux = [Tableau.fromMatrix(i) for i in matricies]
        return cls(tableaux)

if __name__ == '__main__':
    system = OTsystem.fromOTW('shortVT.csv')
    assert len(system.tableaux) == 4
    assert len(system.getConstraintList()) == 5
    assert len(system.tableaux[0].candidates) == 2
    assert len(system.tableaux[3].candidates) == 8
    assert len(LEG.fromTableau(system.tableaux[0]).candidates) == 2
    #print(system.tableaux[0].candidates[0])
    print(LEG.fromTableau(system.tableaux[0]).filter()[0])
    print('green')

        