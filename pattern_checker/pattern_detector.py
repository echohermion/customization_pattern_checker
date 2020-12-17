# -*- coding: utf-8 -*-

import sys
import pprint
import json
from pattern_checker.function import Function

from solidity_parser import parser


def get_ast_and_output_to_file(filepath, output_path):
    """
    Get the AST for a inout Solidity file and output to output file

    Args:
        filepath: filepath for a Solidity file
        output_path: output AST to a specific file

    Returns:
        An AST for the Solidity file
    """
    sourceUnit = parser.parse_file(filepath)

    with open(output_path, 'w') as f:
        pprint.pprint(sourceUnit, f)

    return sourceUnit


def get_ast(filepath):
    """
    Get the AST for a inout Solidity file and output to output file

    Args:
        filepath: filepath for a Solidity file

    Returns:
        An AST for the Solidity file
    """
    sourceUnit = parser.parse_file(filepath)

    return sourceUnit


def traverse_ast(sourceUnit):
    """
    Traverse the AST and Extract all require statement conditions and if statement conditions from the AST

    Args:
        sourceUnit: a AST generated by parser

    Returns:
        A List of function instances extracted from sourceUnit
    """
    function_list = []
    for node in sourceUnit['children'][0]['subNodes']:
        # Each node represents a function.
        if node['type'] == 'FunctionDefinition':
            func_name = node['name']
            para_list = []
            for para in node['parameters']['parameters']:
                type = para['typeName']['name']
                para_list.append(type)
            if node['returnParameters']:
                return_value = node['returnParameters']['parameters'][0]['typeName']['name']
            else:
                return_value = None
            function = Function(func_name, para_list, return_value)

            require_list = []
            if_list = []

            for stat in node['body']['statements']:
                # Extract require statement condition
                if 'expression' in stat.keys():
                    if 'expression' in stat['expression'].keys():
                        if stat['expression']['expression']['name'] == 'require':
                            require_condition = stat['expression']['arguments']
                            require_list.append(require_condition)
                # Extract if statement condition
                if stat['type'] == 'IfStatement':
                    if_condition = stat['condition']
                    if_list.append(if_condition)

            # Add require_condition and if_condition to Function instance
            function.add_require_condition(require_list)
            function.add_if_condition(if_list)

            function_list.append(function)

    return function_list


def compare(file_a, file_b):
    """
    Compare the require_condition and if_condition in two Solidity files
    Args:
        file_a: Solidity file a
        file_b: Solidity file b
    Returns:
        A List of matched patterns.
    """
    ast_a = get_ast(file_a)
    ast_b = get_ast(file_b)

    function_list_a = traverse_ast(ast_a)
    function_list_b = traverse_ast(ast_b)

    # First, check if two files have the same function(same function name, parameter type and return value type)
    for func_a in function_list_a:
        for func_b in function_list_b:
            if func_a.func_name == func_b.func_name and func_a.para_list == func_b.para_list and func_a.return_value == func_b.return_value:
                require_conditions_a = func_a.require_list
                if_conditions_a = func_a.if_list
                require_conditions_b = func_b.require_list
                if_conditions_b = func_b.if_list

                # print(func_a.func_name)
                # print("Require:")
                # print(require_conditions_a)
                # print(require_conditions_b)
                # print("If:")
                # print(if_conditions_a)
                # print(if_conditions_b)
                # print("=========================")

                # Then, detect require_releated patterns and if-related patterns from the require/if conditions of
                # these two files.
                if require_conditions_a == [[]] and require_conditions_b == [[]] and if_conditions_a == [[]] and if_conditions_b == [[]]:
                    print("No require statements, No if statements!")
                elif require_conditions_a != [[]] and require_conditions_b != [[]]:
                    detect_require_related_patterns(require_conditions_a, require_conditions_b)


def detect_require_related_patterns(require_conditions_a, require_conditions_b):
    """
    Detect patterns only need to compare require statement conditions of two contracts
    Args:
        require_condition_a
        require_condition_b
    Returns:
        A list of detected require-related patterns
    """
    if require_conditions_a != require_conditions_b:
        # compare the diff between two lists， output same key and different value
        for cond_a in require_conditions_a[0][0]:
            for cond_b in require_conditions_b[0][0]:
                print(cond_a)
                print(cond_b)
                diff = cond_a.keys() & cond_b
                diff_vals = [(k, cond_a[k], cond_b[k]) for k in diff if cond_a[k] != cond_b[k]]
                # JSon formatted output
                diff_vals = json.dumps(diff_vals, indent=4, separators=(',', ':'))
                print(diff_vals)

        pass


def find_all_key(target_key, dictData, notFound=[]):
    queue = [dictData]
    result = []
    while len(queue) > 0:
        data = queue.pop()
        for key, value in data.items():
            if key == target_key:
                result.append(value)
            elif type(value) == dict:
                queue.append(value)
    if not result:
        result = notFound
    return result


if __name__ == '__main__':
    compare("EIP20.sol", "EIP.sol")
