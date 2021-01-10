import sys
import pprint

from solidity_parser import parser

def solidity_parser(file_path):
    sourceUnit = parser.parse_file(file_path)
    sourceUnitObject = parser.objectify(sourceUnit)

    # Type 1: Trace the whole dict of the contract
    # pprint.pprint(sourceUnit)
    # Get require statement
    subNodes = sourceUnit['children'][0]['subNodes']
    for subNode in subNodes:
        # If is a function
        if 'body' in subNode.keys():
            pprint.pprint(subNode['body'])


    # Get condition in require statement

    # Type 2: Trace some common-use part through objectify method.
    # for contract in sourceUnitObject.contracts.keys():
    #     for function in sourceUnitObject.contracts[contract].functions.keys():
    #         print("Function: " + function)
    #         pprint.pprint(sourceUnitObject.contracts[contract].functions[function].declarations)
    #         print("===================================")

    # pprint.pprint(sourceUnitObject.contracts.keys)


if __name__ == '__main__':
    solidity_parser("/Users/luliu/PycharmProjects/solidity-parser-python/EIP.sol")


