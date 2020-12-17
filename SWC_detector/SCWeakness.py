

class SCWeakness:
    def __init__(self, ast_tree):
        self.ast_tree = ast_tree
        self.is_guarded = self.check_guarded()


    def is_weakness(self):
        return self.is_guarded

    def check_guarded(self):
        pass


class IntegerOverflowUnderflow(SCWeakness):
    def __init__(self, ast_tree):
        self.name = 'Integer Overflow/Overflow'
        SCWeakness.__init__(ast_tree)


class UncheckedCallReturnValue(SCWeakness):
    def __init__(self, ast_tree):
        self.name = "Unchecked Call Return Value"
        SCWeakness.__init__(ast_tree)


class UnprotectedEtherWithdrawal(SCWeakness):
    def __init__(self, ast_tree):
        self.name = "Unprotected Ether Withdrawal"
        SCWeakness.__init__(ast_tree)


class UnprotectedSelfdestrcutInstruction(SCWeakness):
    def __init__(self, ast_tree):
        self.name = "Unprotected SELFDESTRUCT Instruction"
        SCWeakness.__init__(ast_tree)


class Reentrancy(SCWeakness):
    def __init__(self, ast_tree):
        self.name = "Reentrancy"
        SCWeakness.__init__(ast_tree)


class AssertViolation(SCWeakness):
    def __init__(self, ast_tree):
        self.name = "Assert Violation"
        SCWeakness.__init__(ast_tree)


class RequirementViolation(SCWeakness):
    def __init__(self, ast_tree):
        self.name = "Requirement Violation"
        SCWeakness.__init__(ast_tree)


class UnexpectedEtherBalance(SCWeakness):
    def __init__(self, ast_tree):
        self.name = "Unexpected Ether balance"
        SCWeakness.__init__(ast_tree)


class CodeWithNoEffects(SCWeakness):
    def __init__(self, ast_tree):
        self.name = "Code With No Effects"
        SCWeakness.__init__(ast_tree)
