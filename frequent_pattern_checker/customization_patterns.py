
class CustomizationPatterns:
    def __init__(self, tem_contract, cus_contract):
        self.tem_contract = tem_contract
        self.cus_contrac = cus_contract
        self.cus_patterns = {
            "add_clause": 0,
            "add_var": 0,
            "add_stat": 0,
            "delete_clause": 0,
            "delete_var": 0,
            "delete_stat": 0,
            "modify_clause": 0,
            "cosmetic_change": 0,   # we manually identify cosmetic_change.
        }

    def update_cus_patterns(self, cus_patterns):
        self.cus_patterns = cus_patterns
