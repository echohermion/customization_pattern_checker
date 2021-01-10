class ContractRequireStatement:
    def __init__(self, contract_name):
        self.contract_name = contract_name
        self.function_rs_list = []

    def add_function_rs_list(self, FunctionRequireStatement):
        self.function_rs_list.append(FunctionRequireStatement)

    def get_function_rs_list(self):
        return self.function_rs_list