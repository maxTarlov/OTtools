import OTobjects
from OTobjects import Candidate, Constraint

class LEG(OTobjects.OTtable):
    """Linear Extenion of Grammar. OTtable with linearly ordered constraints"""
    
    #Move to Tableau?
    @classmethod
    def fromTableau(cls, tableau):
        return cls(tableau.input, tableau.constraints, tableau.candidates)
    
    def evaluate(self):
        """Return list of optimal candidates under this ordering"""

        passing = self.constraints[0].filter(self.candidates)
        if len(self.constraints) > 1 and len(passing) > 1:
            return LEG(self.input, self.constraints[1:], passing).evaluate()
        else:
            return passing

class Tableau(OTobjects.OTtable):
    """OTtable with unordered constraint set"""

    def getOptima(self):
        """Return list of possible optima as arise from every inear order"""

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
    """A collection of Tableau instances with the same constraint sets"""

    def getConstraintList(self):
        """Return the list of constraints shared by all Tableau instances"""

        return self.tableaux[0].getConstraintList()

    def getOptima(self):
        """Return a new OTsystem with only possible optima in each Tableau"""

        return OTsystem([Tableau(t.input, t.constraints, t.getOptima()) for t in self.tableaux])

    def __init__(self, tableaux):
        """tableaux: [Tableau, ], all must have the equivilant constraint sets"""

        self.tableaux = tableaux
        for t in self.tableaux:
            #maybe this should be value instead of string
            assert t.getConstraintList() == self.getConstraintList()

    @classmethod
    def fromOTW(cls, filepath):
        """Return new OTsystem parsed from OTWorkplace formatted file"""

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
        """Export to OTWorkplace compatable file"""

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
    import unittest

    class TestOTsystem(unittest.TestCase):
        def test_01_fromOTW(self):
            #setup
            self.system = OTsystem.fromOTW('./testing/testVT.csv')

            self.assertEqual(len(self.system.tableaux), 4)
            self.assertEqual(len(self.system.getConstraintList()), 5)
            self.assertEqual(len(self.system.tableaux[0].candidates), 2)
            self.assertEqual(len(self.system.tableaux[1].candidates), 4)
            self.assertEqual(len(self.system.tableaux[2].candidates), 4)
            self.assertEqual(len(self.system.tableaux[3].candidates), 8)

            for tableau in self.system.tableaux:
                #validate special properties of violations in ./testing/testVT.csv
                for candidate, index in zip(tableau.candidates, range(len(tableau.candidates))):
                    checkInt = tableau.constraints[0].violations[candidate]
                    self.assertEqual(checkInt, index)
                    for violations in [con.violations[candidate] for con in tableau.constraints[1:]]:
                        self.assertTrue(violations > checkInt or violations == 0)
                        checkInt = violations
        
        def test_02_toOTW(self):
            #make sure the exported file works in otw, then assert import/export equal
            pass

        def test_03_getOptima(self):
            #setup
            self.system = OTsystem.fromOTW('./testing/nGX.csv')
            self.optima = self.system.getOptima()

            self.assertEqual(len(self.optima.tableaux[0].candidates), 2)
            self.assertEqual(len(self.optima.tableaux[1].candidates), 8)
            self.assertEqual(len(self.optima.tableaux[2].candidates), 6)
            self.assertEqual(len(self.optima.tableaux[3].candidates), 12)

            for optimal, original in zip(self.optima.tableaux, self.system.tableaux):
                for optimum in optimal.candidates:
                    self.assertIn(optimum, original.candidates)


    unittest.main()
            
    #self.assertTrue(len(LEG.fromTableau(system.tableaux[0]).candidates) == 2)
    #print(system.tableaux[0].candidates[0])
    #print(LEG.fromTableau(system.tableaux[3]).evaluate()[0])
    #print(system.tableaux[0].getLEGs())
        