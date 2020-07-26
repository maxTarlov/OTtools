import logging

class TableauObject:
    """
    Metaclass for objects contained in an OT
    
    Ensures that contents of an OTtable support string casting
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Candidate(TableauObject):
    """
    Representaion of a candidate in Optimality Theory
    
    Subclasses TableauObject, contained in Constraint and OTtable
    """

    pass

class Constraint(TableauObject):
    """
    Representation of a constraint and its evaluation of candidates in OT

    Subclasses TableauObject, contained in OTtable, contains Candidate
    
    Attributes: 
        value: usually the constraint name
        violations: mapping of Candidate instances to violation counts (integers)

    Methods:
        addViolations
    """

    def __init__(self, value, violations=None):
        self.value = value
        if not violations:
            violations = {}
        for k, v in violations.items():
            assert isinstance(k, Candidate)
            assert isinstance(v, int)
        self.violations = violations

    def addViolations(self, violations):
        assert violations.items()
        for k, v in violations.items():
            assert k not in self.violations.keys()
            assert isinstance(k, Candidate)
            assert isinstance(v, int)
            self.violations[k] = v
    
    def filter(self, candidates):
        minimum = min([self.violations[c] for c in candidates])
        result = []
        for c in candidates:
            if self.violations[c] == minimum:
                result.append(c)
        assert len(result)
        return result

class OTtable:
    def __init__(self, input, constraints, candidates):
        self.input = input
        self.candidates = candidates
        for c in candidates:
            assert isinstance(c, Candidate)
        self.constraints = constraints
        for c in constraints:
            assert isinstance(c, Constraint)

    @classmethod
    def fromMatrix(cls, matrix):
        input = matrix[0][0]
        logging.debug('Input: ' + str(input))
        constraints = [Constraint(con) for con in matrix[0][1:]]
        candidates = [Candidate(row[0]) for row in matrix[1:]]
        for can, row in zip(candidates, matrix[1:]):
            for con, violations in zip(constraints, row[1:]):
                logging.debug('{}({}): {}'.format(str(con), str(can), str(violations)))
                con.addViolations({can: int(violations)})
        return cls(input, constraints, candidates)

    def getConstraintList(self):
        return [str(c) for c in self.constraints]

if __name__ == '__main__':
    import unittest
    #logging.basicConfig(level=logging.DEBUG)

    class TestConstraint(unittest.TestCase):
        def setUp(self):
            self.candidate = Candidate('Test')
            self.constraint = Constraint('Test')

        def test__init__(self):
            self.assertIsNotNone(Constraint(''))
            self.assertRaises(Exception, Constraint, 'Test', violations={'String': 0})
            self.assertRaises(Exception, Constraint, 'Test', violations={self.candidate: 'String'})

        def test_addViolations(self):
            self.constraint2 = Constraint('Test')
            
            self.constraint2.addViolations({self.candidate: 0})
            self.assertNotEqual(self.constraint.violations, self.constraint2.violations)

            self.assertRaises(Exception, self.constraint.addViolations, 0)
            self.assertRaises(Exception, self.constraint.addViolations, {'String': 0})
            self.assertRaises(Exception, self.constraint.addViolations, {self.candidate: '0'})

        def test_filter(self):
            self.candidate = lambda : Candidate('Test')
            self.allPassing = {self.candidate(): __ for __ in [0, 0, 0, 0, 0]}
            self.mostPassing = {self.candidate(): __ for __ in [0, 0, 0, 1, 1]}
            self.somePassing = {self.candidate(): __ for __ in [0, 0, 1, 1, 1]}
            self.onePassing = {self.candidate(): __ for __ in range(5)}

            self.constraint.addViolations(self.allPassing)
            self.constraint.addViolations(self.mostPassing)
            self.constraint.addViolations(self.somePassing)
            self.constraint.addViolations(self.onePassing)

            self.assertEqual(len(self.constraint.filter(self.allPassing)), 5)
            self.assertEqual(len(self.constraint.filter(self.mostPassing)), 3)
            self.assertEqual(len(self.constraint.filter(self.somePassing)), 2)
            self.assertEqual(len(self.constraint.filter(self.onePassing)), 1)

    unittest.main()