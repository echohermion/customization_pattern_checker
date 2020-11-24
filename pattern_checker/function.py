# -*- coding: utf-8 -*-

class Function:
    """
    A class to store syntax info(funciton name, parameters, return_value, require statements condition and if statement condition)
    within a function.
    """
    def __init__(self, func_name, para_list, return_value):
        self.func_name = func_name
        self.para_list = para_list
        self.return_value = return_value
        self.require_list = []
        self.if_list = []

    def add_require_condition(self, require_condition):
        self.require_list.append(require_condition)

    def add_if_condition(self, if_condition):
        self.if_list.append(if_condition)

