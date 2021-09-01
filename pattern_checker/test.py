from solidity_parser import parser
from pattern_checker.Function import Function
import pattern_checker.utils as Utils
import pprint
import json

'''
Only for TESTING
'''

def get_revert(file_path):
    sourceUnit = parser.parse_file(file_path)

    # Get subNodes(subNodes are functions and global variables)
    subNodes = sourceUnit['children'][0]['subNodes']
    function_list = []

    for subNode in subNodes:
        # If it is a function
        if 'body' in subNode.keys():
            function_name = subNode['name']
            parameters = subNode['parameters']

            require_list = []
            revert_list = []
            assert_list = []            # Solidity parser does not support the 'throw' keyword.
            general_if_list = []
            transaction_reverting_list = []

            # Get all statements in the function
            statements = subNode['body']['statements']
            for statement in statements:
                pprint.pprint(statement)
                if statement['type'] == 'ExpressionStatement':
                    if 'expression' in statement['expression'].keys():
                        # Identify require statements
                        if statement['expression']['expression']['name'] == 'require':
                            arguments = statement['expression']['arguments']
                            require_list.append(arguments)
                            transaction_reverting_list.append(arguments)
                        # Identify assert statements
                        elif statement['expression']['expression']['name'] == 'assert':
                            arguments = statement['expression']['arguments']
                            assert_list.append(arguments)
                elif statement['type'] == 'IfStatement':
                    # debug
                    pprint.pprint(statement)
                    if statement['TrueBody']['statements'][0]:
                        if_block = statement['TrueBody']['statements'][0]
                        if if_block == ';':
                            continue
                        if 'expression' in if_block['expression'].keys():
                            # Identify revert statements
                            if if_block['expression']['expression']['name'] == 'revert':
                                conditions = statement['condition']
                                revert_list.append(conditions)
                                transaction_reverting_list.append(conditions)
                        else:   # Identify general_purpose if statements
                            conditions = statement['condition']
                            general_if_list.append(conditions)
            #
            # if len(require_list) > 0:
            #     f = Function(function_name, parameters, require_list)
            #     function_list.append(f)


if __name__ == '__main__':
    custom_contract_path = "../samples/simple.sol"
    get_revert(custom_contract_path)