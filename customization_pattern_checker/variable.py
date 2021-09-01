
class Variable:
    def __init__(self, var_type, name):
        self.var_type = var_type
        self.name = name

    # # For simple var type(e.g., Identifier)
    # @classmethod
    # def simple_var(cls, name):
    #     cls.name = name
    #
    # # For complex var type(e.g., IndexAccess)
    # @classmethod
    # def complex_var(cls, var_type, base, index):
    #     cls.var_type = var_type
    #     cls.var_base = base
    #     cls.var_index = index
