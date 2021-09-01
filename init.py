import sys
import pprint

from solidity_parser import parser
from pattern_checker.Function import Function
import pattern_checker.utils as Utils

# Get function name, parameters and require() and revert() statements for each function in a contract file
def solidity_parser(file_path):
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
            assert_list = []  # Solidity parser does not support the 'throw' keyword.
            general_if_list = []
            transaction_reverting_list = []

            # Get all statements in the function
            statements = subNode['body']['statements']
            for statement in statements:
                # pprint.pprint(statement)
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
                        else:  # Identify general_purpose if statements
                            conditions = statement['condition']
                            general_if_list.append(conditions)

            f = Function(function_name, parameters, require_list, revert_list, assert_list, general_if_list, transaction_reverting_list)
            function_list.append(f)

    return function_list


# Identify customization patterns for two contracts
def identify_cus_patterns(func_list_1, func_list_2, cus_patterns):
    # First find matched functions within two contracts
    for func_1 in func_list_1:
        for func_2 in func_list_2:
            function_name_1 = func_1.func_name
            para_1 = func_1.para_list
            function_name_2 = func_2.func_name
            para_2 = func_2.para_list
            if function_name_1 == function_name_2 and para_1 == para_2:
                if function_name_1 is not None:
                    print("Function Name: " + function_name_1)
                else:
                    print("Constructor Function")
                # If two functions matched, then identify customization patterns.
                cus_patterns = compare_stat_diff(func_1, func_2, cus_patterns)
    return cus_patterns


# Compare the diff in two transaction-reverting statement in two matched functions to identify customization patterns.
def compare_stat_diff(func_1, func_2, cus_patterns):
    require_list_1 = func_1.require_list
    revert_list_1 = func_1.require_list
    require_list_2 = func_2.require_list
    revert_list_2 = func_2.revert_list
    # transaction_reverting_list_1 = func_1.transaction_reverting_list
    # transaction_reverting_list_2 = func_2.transaction_reverting_list

    # First delete the same part
    for i in range(len(require_list_1)):
        for r in require_list_1:
            if r in require_list_2:
                require_list_1.remove(r)
                require_list_2.remove(r)
    for i in range(len(revert_list_1)):
        for r in revert_list_1:
            if r in revert_list_2:
                revert_list_1.remove(r)
                revert_list_2.remove(r)

    # Then compare the different part
    # 1. Compare the require statement part
    # 2. Identify and Compare Comment Field
    if len(require_list_1) == len(require_list_2):
        for i in range(len(require_list_1)):
            stat_1 = require_list_1[i][0]
            stat_2 = require_list_2[i][0]

            comm_1 = ""
            comm_2 = ""
            if len(require_list_1[i]) > 1:
                comm_1 = require_list_1[i][1]
            if len(require_list_2[i]) > 1:
                comm_2 = require_list_2[i][1]

            cus_patterns = Utils.find_cus_patterns(stat_1, stat_2, comm_1, comm_2, cus_patterns)

    elif len(require_list_1) > len(require_list_2):
        for i in range(len(require_list_2)):
            stat_1 = require_list_1[i][0]
            stat_2 = require_list_2[i][0]

            comm_1 = ""
            comm_2 = ""
            if len(require_list_1[i]) > 1:
                comm_1 = require_list_1[i][1]
            if len(require_list_2[i]) > 1:
                comm_2 = require_list_2[i][1]

            cus_patterns = Utils.find_cus_patterns(stat_1, stat_2, comm_1, comm_2, cus_patterns)

        add_count = len(require_list_1) - len(require_list_2)
        cus_patterns["add_stat"] += add_count

    elif len(require_list_1) < len(require_list_2):
        for i in range(len(require_list_1)):
            stat_1 = require_list_1[i][0]
            stat_2 = require_list_2[i][0]

            comm_1 = ""
            comm_2 = ""
            if len(require_list_1[i]) > 1:
                comm_1 = require_list_1[i][1]
            if len(require_list_2[i]) > 1:
                comm_2 = require_list_2[i][1]

            cus_patterns = Utils.find_cus_patterns(stat_1, stat_2, comm_1, comm_2, cus_patterns)

        delete_count = len(require_list_1) - len(require_list_2)
        cus_patterns["add_stat"] += delete_count

    # 3. Compare the revert statement part
    if len(revert_list_1) == len(revert_list_2):
        for i in range(len(revert_list_1)):
            stat_1 = revert_list_1[i]
            stat_2 = revert_list_2[i]

            comm_1 = ""
            comm_2 = ""

            cus_patterns = Utils.find_cus_patterns(stat_1, stat_2, comm_1, comm_2, cus_patterns)

    elif len(revert_list_1) > len(revert_list_2):
        for i in range(len(revert_list_2)):
            stat_1 = revert_list_1[i]
            stat_2 = revert_list_2[i]

            comm_1 = ""
            comm_2 = ""

            cus_patterns = Utils.find_cus_patterns(stat_1, stat_2, comm_1, comm_2, cus_patterns)

        add_count = len(revert_list_1) - len(revert_list_2)
        cus_patterns["add_stat"] += add_count

    elif len(revert_list_1) < len(revert_list_2):
        for i in range(len(revert_list_1)):
            stat_1 = revert_list_1[i]
            stat_2 = revert_list_2[i]

            comm_1 = ""
            comm_2 = ""

            cus_patterns = Utils.find_cus_patterns(stat_1, stat_2, comm_1, comm_2, cus_patterns)

        delete_count = len(revert_list_1) - len(revert_list_2)
        cus_patterns["add_stat"] += delete_count

    cus_patterns = identify_stat_type_change(func_1, func_2, cus_patterns)

    return cus_patterns


# Identify the modify_statement_type patterns from all condition statements
def identify_stat_type_change(func_1, func_2, cus_patterns):
    # Compare conditions for each two statement types
    if len(func_1.require_list) > 0:
        if len(func_2.revert_list) > 0:
            for r_1 in func_1.require_list:
                for r_2 in func_2.revert_list:
                    r_1 = r_1[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
        if len(func_2.assert_list) > 0:
            for r_1 in func_1.require_list:
                for r_2 in func_2.assert_list:
                    r_1 = r_1[0]
                    r_2 = r_2[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
        if len(func_2.general_if_list) > 0:
            for r_1 in func_1.require_list:
                for r_2 in func_2.general_if_list:
                    r_1 = r_1[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
    if len(func_1.revert_list) > 0:
        if len(func_2.require_list) > 0:
            for r_1 in func_1.revert_list:
                for r_2 in func_2.require_list:
                    r_2 = r_2[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
        if len(func_2.assert_list) > 0:
            for r_1 in func_1.revert_list:
                for r_2 in func_2.assert_list:
                    r_2 = r_2[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
        if len(func_2.general_if_list) > 0:
            for r_1 in func_1.revert_list:
                for r_2 in func_2.general_if_list:
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
    if len(func_1.assert_list) > 0:
        if len(func_2.require_list) > 0:
            for r_1 in func_1.assert_list:
                for r_2 in func_2.require_list:
                    r_1 = r_1[0]
                    r_2 = r_2[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
        if len(func_2.revert_list) > 0:
            for r_1 in func_1.assert_list:
                for r_2 in func_2.revert_list:
                    r_1 = r_1[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
        if len(func_2.general_if_list) > 0:
            for r_1 in func_1.assert_list:
                for r_2 in func_2.general_if_list:
                    r_1 = r_1[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
    if len(func_1.general_if_list) > 0:
        if len(func_2.require_list) > 0:
            for r_1 in func_1.general_if_list:
                for r_2 in func_2.require_list:
                    r_2 = r_2[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
        if len(func_2.revert_list) > 0:
            for r_1 in func_1.general_if_list:
                for r_2 in func_2.revert_list:
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
        if len(func_2.assert_list) > 0:
            for r_1 in func_1.general_if_list:
                for r_2 in func_2.assert_list:
                    r_2 = r_2[0]
                    if if_same_cond(r_1, r_2):
                        cus_patterns["modify_stat_type"] += 1
    return cus_patterns


# Check whether the condition between two statements are the same
def if_same_cond(cond_1, cond_2):
    if cond_1 == cond_2:
        return True
    else:
        return False


def init(custom_contract_path, template_contract_path):
    func_list1 = solidity_parser(custom_contract_path)   # custom contract
    func_list2 = solidity_parser(template_contract_path)  # template contract

    cus_patterns = {
        "add_clause": 0,
        "add_var": 0,
        "add_stat": 0,
        "delete_clause": 0,
        "delete_var": 0,
        "delete_stat": 0,
        "modify_clause": 0,
        "modify_stat_type": 0,
        "cosmetic_change": 0,
    }

    cus_patterns = identify_cus_patterns(func_list1, func_list2, cus_patterns)

    pprint.pprint(cus_patterns)


if __name__ == '__main__':
    # custom_contract_path = "../samples/simple.sol"
    # template_contract_path = "../samples/simple1.sol"

    custom_contract_path = sys.argv[1]
    template_contract_path = sys.argv[2]

    init(custom_contract_path, template_contract_path)

