class FunctionRequireStatement:
    def __init__(self, function_name):
        self.function_name = function_name
        self.rs_list = []

    def add_require_statement(self, RequireStatement):
        self.rs_list.append(RequireStatement)

    def get_rs_list(self):
        return self.rs_list
