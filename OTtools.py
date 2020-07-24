# Restarting OTtools
import unittest

class TableauObject:
    _keyType = object  

    def __init__(self, value):
        self.value = value
        self.violations = None

    def setViolations(self, violations):
        if self.violations:
            pass
            #TODO: raise an exception
        else:
            for k, v in violations.items():
                assert isinstance(k, self._keyType)
                assert isinstance(v, int)
            self.violations = violations

    def __str__(self):
        return str(self.value)

class Candidate(TableauObject):
    pass
    # _keyType defined below

class Constraint(TableauObject):
    # _keyType defined below
    def filter(self, candidates):
        minimum = min([c.violations[self] for c in candidates])
        result = []
        for c in candidates:
            if self.violations[c] == minimum:
                result.append(c)
        return result

Candidate._keyType = Constraint
Constraint._keyType = Candidate

class OTobject:
    def __init__(self, input, constraints, candidates):
        self.input = input
        self.candidates = candidates
        for c in candidates:
            assert isinstance(c, Candidate)
        self.constraints = constraints
        for c in constraints:
            assert isinstance(c, Constraint)
        
        if candidates[0].violations and not constraints[0].violations:
            for con in constraints:
                con.setViolations({can: can.violations[con] for can in candidates})
        elif constraints[0].violations and not candidates[0].violations:
            for can in candidates:
                can.setViolations({con: con.violations[can] for con in constraints})

    @classmethod
    def fromMatrix(cls, matrix):
        input = matrix[0][0]
        constraints = [Constraint(con) for con in matrix[0][1:]]
        candidates = [Candidate(row[0]) for row in matrix[1:]]
        for can, row in zip(candidates, matrix[1:]):
            can.setViolations({con: int(v) for con, v in zip(constraints, row[1:])})
        return cls(input, constraints, candidates)

    def getConstraintList(self):
        return [str(c) for c in self.constraints]

class LEG(OTobject):
    @classmethod
    def fromTableau(cls, tableau):
        return cls(tableau.input, tableau.constraints, tableau.candidates)
    
    def evaluate(self):
        passing = self.constraints[0].filter(self.candidates)
        if len(self.constraints) > 1 and len(passing) > 1:
            return LEG(self.input, self.constraints[1:], passing).evaluate()
        else:
            return passing

class Tableau(OTobject):
    def getOptima(self):
        optima = []
        for c in self.constraints:
            passing = c.filter(self.candidates)
            if len(self.constraints) > 1 and len(passing) > 1:
                newCON = [x for x in self.constraints if x != c]
                optima += Tableau(self.input, newCON, passing).getOptima()
            else:
                optima += passing
        result = []
        for c in optima:
            if c not in result:
                result.append(c)
        return result

    def getLEGs(self):
        raise Exception('Unfinished method')
        result = []
        if len(self.constraints) > 1:
            for c in self.constraints:
                newCON = [x for x in self.constraints if x != c]
                for o in Tableau(self.input, newCON, self.candidates).getLEGs():
                    result.append(o)
        return [LEG.fromTableau(t) for t in result]

class OTsystem:
    def getConstraintList(self):
        return self.tableaux[0].getConstraintList()

    def getOptima(self):
        return OTsystem([Tableau(t.input, t.constraints, t.getOptima()) for t in self.tableaux])

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

    #TODO re-evaluate this:
    @staticmethod
    def _writeCandidates(csv_writer, candidates, constraints):
        for cand in candidates:
            violations = [con.violations[cand] for con in constraints]
            csv_writer.writerow(['', str(cand), ''] + violations)

    def toOTW(self, filepath):
        import csv

        with open(filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([])
            csv_writer.writerow(['', '', ''] + self.getConstraintList())
            for t in self.tableaux:
                violations0 = [con.violations[t.candidates[0]] for con in t.constraints]
                csv_writer.writerow([str(t.input), str(t.candidates[0]), ''] + violations0)
                self._writeCandidates(csv_writer, t.candidates[1:], t.constraints)


if __name__ == '__main__':
    """
    system = OTsystem.fromOTW('./testing/testVT.csv')
    assert len(system.tableaux) == 4
    assert len(system.getConstraintList()) == 5
    assert len(system.tableaux[0].candidates) == 2
    assert len(system.tableaux[3].candidates) == 8
    assert len(LEG.fromTableau(system.tableaux[0]).candidates) == 2
    #print(system.tableaux[0].candidates[0])
    #print(LEG.fromTableau(system.tableaux[3]).evaluate()[0])
    #print(system.tableaux[0].getLEGs())
    optima = system.getOptima()
    print([[c.value for c in t.candidates] for t in optima.tableaux])
    system.toOTW('./testing/testExport.csv')
    print('green')
    """

    nGX = OTsystem.fromOTW('./testing/nGX.csv')
    tab = nGX.tableaux[1]
    optima = tab.getOptima()
    print([__.value for __ in optima])
        