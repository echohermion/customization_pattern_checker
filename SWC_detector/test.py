
import pprint
from SCUtil import FunctionStatement, IfStatement, RequireStatement, AssertStatement
from z3 import *

from solidity_parser import parser


def solidity_parser(file_path):
    sourceUnit = parser.parse_file(file_path)
    sourceUnitObject = parser.objectify(sourceUnit)

    # Type 1: Trace the whole dict of the contract
    # pprint.pprint(sourceUnit)
    # Get subNodes(subNodes are functions and global variables)
    subNodes = sourceUnit['children'][0]['subNodes']
    for subNode in subNodes:
        # If is a function
        if 'body' in subNode.keys():
            function_name = subNode['name']
            print("Function: " + function_name)
            is_Constructor = subNode['isConstructor']
            modifiers = subNode['modifiers']
            parameters = subNode['parameters']
            return_parameter = subNode['returnParameters']
            visibility = subNode['visibility']
            function = FunctionStatement.FunctionStatement(function_name, is_Constructor, modifiers, parameters, return_parameter, visibility)

            # Get all statements in the function
            statements = subNode['body']['statements']
            pprint.pprint(statements)
            for statement in statements:
                # If statement is a if statement
                if statement['type'] == 'IfStatement':
                    true_body = statement['TrueBody']
                    false_body = statement['FalseBody']
                    condition = statement['condition']
                    if_statement = IfStatement.IfStatement(statement, true_body, false_body, condition)
                    function.add_if_statement(if_statement)
                elif statement['type'] == 'ExpressionStatement':
                    # If expression is a require statement:
                    if statement['expression']['expression']['name'] == 'require':
                        arguments = statement['expression']['arguments']
                        require_statement = RequireStatement.RequireStatement(statement['expression'], arguments)
                        function.add_require_statement(require_statement)
                    # If expression is an assert statement
                    elif statement['expression']['expression']['name'] == 'assert':
                        arguments = statement['expression']['arguments']
                        assert_statement = AssertStatement.AssertStatement(statement['expression'], arguments)
                        function.add_assert_statement(assert_statement)







    # Get condition in require statement

    # Type 2: Trace some common-use part through objectify method.
    # for contract in sourceUnitObject.contracts.keys():
    #     for function in sourceUnitObject.contracts[contract].functions.keys():
    #         print("Function: " + function)
    #         pprint.pprint(sourceUnitObject.contracts[contract].functions[function].declarations)
    #         print("===================================")

    # pprint.pprint(sourceUnitObject.contracts.keys)


def test_z3():
    x = Int('x')
    y = Int('y')
    s = Solver()
    print(s) # []

    s.add(x > 10, y == x + 2)
    print(s)
    print(s.check())  # sat

    s.push()
    s.add(y < 11)
    print(s) # [x > 10, y == x + 2, y < 11]
    print(s.check())  # unsat

    s.pop()  # [x > 10, y == x + 2]
    print(s)
    print(s.check()) # sat


if __name__ == '__main__':
    # solidity_parser("/Users/luliu/PycharmProjects/solidity-parser-python/EIP.sol")
    test_z3()


