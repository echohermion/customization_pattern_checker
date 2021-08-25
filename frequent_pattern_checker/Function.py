# -*- coding: utf-8 -*-

class Function:
    """
    A class to store syntax info(funciton name, parameters, return_value, require statements condition and if statement condition)
    within a function.
    """
    def __init__(self, func_name, para_list, require_list, assert_list):
        self.func_name = func_name
        self.para_list = para_list
        self.require_list = require_list
        self.assert_list = assert_list

    def add_require_condition(self, require_condition):
        self.require_list.append(require_condition)

    def add_revert_condition(self, assert_condition):
        self.assert_list.append(assert_condition)

