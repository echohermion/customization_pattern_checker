class FunctionStatement:
    def __init__(self, function_name, is_Constructor, modifiers, parameters, return_parameters, visibility):
        self.function_name = function_name
        self.isConstructor = is_Constructor
        self.modifiers = modifiers
        self.parameters = parameters
        self.return_paramaters = return_parameters
        self.visibility = visibility
        self.rs_list = []
        self.assert_list = []
        self.if_list = []

    def add_require_statement(self, RequireStatement):
        self.rs_list.append(RequireStatement)

    def add_if_statement(self, ifStatement):
        self.if_list.append(ifStatement)

    def add_assert_statement(self, assertStatement):
        self.assert_list.append(assertStatement)

    def get_rs_list(self):
        return self.rs_list

    def get_assert_list(self):
        return self.assert_list

    def get_if_list(self):
        return self.if_list
