import sys
import pprint

from solidity_parser import parser
from frequent_pattern_checker.Function import Function
import frequent_pattern_checker.utils as Utils
# def remove_require_statement(contract_filepath):
#     sourceUnit = parser.parse_file(contract_filepath)
#     # pprint.pprint(sourceUnit)
#
#     sourceUnitObject = parser.objectify(sourceUnit)
#     for contract in sourceUnitObject.contracts.keys():
#         for function in sourceUnitObject.contracts[contract].functions.keys():
#             for identifier in sourceUnitObject.contracts[contract].functions[function].identifiers.keys():
#                 print(identifier)

'''
Get require() and revert() statements in a contract file
'''
def solidity_parser(file_path):
    sourceUnit = parser.parse_file(file_path)
    sourceUnitObject = parser.objectify(sourceUnit)

    # Type 1: Trace the whole dict of the contract
    # Get subNodes(subNodes are functions and global variables)
    subNodes = sourceUnit['children'][0]['subNodes']
    function_list = []

    for subNode in subNodes:
        # If is a function
        if 'body' in subNode.keys():
            function_name = subNode['name']
            parameters = subNode['parameters']
            # print(function_name)
            # print(parameters)

            require_list = []
            assert_list = []

            # Get all statements in the function
            statements = subNode['body']['statements']
            # pprint.pprint(statements)
            for statement in statements:
                # If statement is a if statement
                # if statement['type'] == 'IfStatement':
                #     true_body = statement['TrueBody']
                #     false_body = statement['FalseBody']
                #     condition = statement['condition']
                #     if_statement = IfStatement.IfStatement(statement, true_body, false_body, condition)
                #     function.add_if_statement(if_statement)
                if statement['type'] == 'ExpressionStatement':
                    # print("Statement: ")
                    # pprint.pprint(statement)
                    # print("===================")
                    # If expression is a require statement:
                    if 'expression' in statement['expression'].keys():
                        if statement['expression']['expression']['name'] == 'require':
                            arguments = statement['expression']['arguments']
                            # print("Require Statement:")
                            # pprint.pprint(arguments)
                            require_list.append(arguments)
                    # If expression is an assert statement
                        elif statement['expression']['expression']['name'] == 'assert':    # change to revert
                            arguments = statement['expression']['arguments']
                            # print("Assert Statement:")
                            # pprint.pprint(arguments)
                            assert_list.append(arguments)
            if len(require_list) > 0 or len(assert_list) > 0:
                f = Function(function_name, parameters, require_list, assert_list)
                function_list.append(f)

    return function_list


'''
Find matched functions
'''
def get_same_func(func_list_1, func_list_2, cus_patterns):
    for func_1 in func_list_1:
        for func_2 in func_list_2:
            function_name_1 = func_1.func_name
            para_1 = func_1.para_list
            function_name_2 = func_2.func_name
            para_2 = func_2.para_list
            if function_name_1 == function_name_2 and para_1 == para_2:
                print(function_name_1)
                compare_stat_diff(func_1, func_2, cus_patterns)
    return cus_patterns

'''
Compare the diff in two transaction-reverting statement in two matched functions
'''
def compare_stat_diff(func_1, func_2, cus_patterns):
        require_list_1 = func_1.require_list
        # assert_list_1 = func_1.assert_list     # change to revert stats
        require_list_2 = func_2.require_list
        # assert_list_2 = func_2.assert_list     # change to revert stats

        # first delete the same part
        for i in range(len(require_list_1)):
            for r in require_list_1:
                if r in require_list_2:
                    require_list_1.remove(r)
                    require_list_2.remove(r)
        # for i in range(len(assert_list_1)):
        #     for r in assert_list_1:
        #         if r in assert_list_2:
        #             assert_list_1.remove(r)
        #             assert_list_2.remove(r)

        # then compare the diff part
        # Print diff require stat
        # print("================After remove diff")
        # print("Require statement: ")
        # if len(require_list_1) > 0 or len(require_list_2) > 0:
        #     if len(require_list_1) > 0:
        #         print(require_list_1)
        #         print("-----------------")
        #     if len(require_list_2) > 0:
        #         print(require_list_2)
        #         print("-----------------")
        # else:
        #     print("No diff in require statement.")
        # # Print diff assert stat
        # print("Assert statement: ")
        # if len(assert_list_1) > 0 or len(assert_list_2) > 0:
        #     if len(assert_list_1) > 0:
        #         print(assert_list_1)
        #         print("-----------------")
        #     if len(assert_list_2) > 0:
        #         print(assert_list_2)
        #         print("-----------------")
        # else:
        #     print("No diff in assert statement.")
        # print("======================================================")


        # print("Require Statements: ")
        # print(require_list_1)
        # print(require_list_2)
        if len(require_list_1) == len(require_list_2):
            for i in range(len(require_list_1)):
                stat_1 = require_list_1[i][0]
                stat_2 = require_list_2[i][0]
                print(stat_1)
                print(stat_2)

                # find different value for the same key
                same_keys = stat_1.keys() & stat_2
                # print("Print diff")
                # print(same_keys)
                diff_vals = [(k, stat_1[k], stat_2[k]) for k in same_keys if stat_1[k] != stat_2[k]]
                print("Print diff_vals for len(require_list_1) == len(require_list_2)")
                for val in diff_vals:
                    print(val)
                print("========================================")

        elif len(require_list_1) > len(require_list_2):
            for i in range(len(require_list_2)):
                stat_1 = require_list_1[i][0]
                stat_2 = require_list_2[i][0]
                # if stat_1 is equal to stat_2, move to next stat comparison
                if stat_1 == stat_2:
                    continue
                print(stat_1)
                print(stat_2)
                clause_list_1 = []
                clause_list_2 = []
                clause_list_1 = get_clauses(stat_1, clause_list_1)
                clause_list_2 = get_clauses(stat_2, clause_list_2)
                print("----------------------------------------")
                print("Clause_list_1:")
                print(clause_list_1)
                print("Clause_list_2:")
                print(clause_list_2)
                print("----------------------------------------")

                same_clauses = Utils.extract_same_elem(clause_list_1, clause_list_2)
                for c in same_clauses:
                    clause_list_1.remove(c)
                    clause_list_2.remove(c)

                # for the remaining different clauses
                if len(clause_list_1) == 0:   # add clause
                    cus_patterns["add_clause"] += len(clause_list_2)
                elif len(clause_list_2) == 0: # delete clause
                    cus_patterns["delete_clause"] += len(clause_list_1)
                else:
                    for c_1 in clause_list_1:
                        for c_2 in clause_list_2:
                            # if 'type' and 'name' in left&right is the same, seem as "modify clause"
                            # else, seem as "add var" or "delete var"
                            if c_1['left']['type'] == c_2['left']['type'] and c_1['left']['name'] == c_2['left']['name'] and c_1['right']['type'] == c_2['right']['type'] and c_1['right']['name'] == c_2['right']['name']:
                                cus_patterns['modify_clause'] += 1
                                clause_list_1.remove(c_1)
                                clause_list_2.remove(c_2)
                    # the remaining part is added to "add var" or "delete var"
                    if len(clause_list_1) >= len(clause_list_2):
                        cus_patterns["delete_var"] += len(clause_list_1) - len(clause_list_2)
                    else:
                        cus_patterns["add_var"] += len(clause_list_2) - len(clause_list_1)

                # # find different value for the same key
                # same_keys = stat_1.keys() & stat_2
                # # print("Print diff")
                # # print(same_keys)
                # diff_vals = [(k, stat_1[k], stat_2[k]) for k in same_keys if stat_1[k] != stat_2[k]]
                # print("Print diff_vals for len(require_list_1) > len(require_list_2)")
                # for val in diff_vals:
                #     print(val)
                # print("========================================")

            print("Other stats in require_list_1: ")  # which should be added to "Del stat"
            for j in range(len(require_list_2), len(require_list_1)):
                cus_patterns["delete_stat"] += 1
                # print(require_list_1[j][0])
        elif len(require_list_1) < len(require_list_2):
            for i in range(len(require_list_1)):
                stat_1 = require_list_1[i][0]
                stat_2 = require_list_2[i][0]
                print(stat_1)
                print(stat_2)
                print("----------------------------------------")

                # find different value for the same key
                same_keys = stat_1.keys() & stat_2
                # print("Print diff")
                # print(same_keys)
                diff_vals = [(k, stat_1[k], stat_2[k]) for k in same_keys if stat_1[k] != stat_2[k]]
                print("Print diff_vals for len(require_list_1) < len(require_list_2)")
                for val in diff_vals:
                    print(val)
                print("========================================")

            print("Other stats in require_list_2: ")  # which should be added to "Add stat"
            for j in range(len(require_list_1), len(require_list_2)):
                cus_patterns["add_stat"] += 1
                # print(require_list_2[j][0])
        # for s1 in require_list_1:
        #     for s2 in require_list_2:
        #         # 怎么将两条相似的statement对应起来比较？怎么找到相似的statement？
        #         # 就按照时间顺序来比较
        #         stat_1 = s1[0]
        #         stat_2 = s2[0]
        #         print(stat_1)
        #         print(stat_2)
        #         print("----------------------------------------")
        #
        #         # find different value for the same key
        #         same_keys = stat_1.keys() & stat_2
        #         # print("Print diff")
        #         # print(same_keys)
        #         diff_vals = [(k, stat_1[k], stat_2[k]) for k in same_keys if stat_1[k] != stat_2[k]]
        #         print("Print diff_vals")
        #         for val in diff_vals:
        #             print(val)
        #         print("========================================")


'''
Input: require_list_1 and require_list_2 or assert_list_1 and assert_list_2
Note that stat_list_1 is from template contracts while stat_list_2 is from custom contacts.
'''
def detect_frequent_patterns(stat_list_1, stat_list_2):
    frequent_patterns = {
        "Add clause": 0,
        "Add new var": 0,
        "Add stat": 0,
        "Del clause": 0,
        "Del var": 0,
        "Del stat": 0,
        "Change stat": 0,
        "Modify clause": 0,
        "Other": 0,
    }

    if len(stat_list_1) == 0 and len(stat_list_2) != 0:
        # No diff in two stat_list
        return
    if len(stat_list_1) == 0 and len(stat_list_2) != 0:
        count = len(stat_list_2)
        frequent_patterns["Add stat"] += count
    if len(stat_list_1) != 0 and len(stat_list_2) == 0:
        count = len(stat_list_1)
        frequent_patterns["Del stat"] += count
    # 分情况讨论（template contract 和 custom contract 的require statement数量 相同， template多， custom多）
    if len(stat_list_1) == len(stat_list_2):
        for i in range(len(stat_list_1)):
            stat_1 = stat_list_1[i][0]
            stat_2 = stat_list_2[i][0]
            pprint.pprint(stat_1)
            pprint.pprint(stat_2)
            print("----------------------------------------")

            # find different value for the same key
            same_keys = stat_1.keys() & stat_2
            # print("Print diff")
            # print(same_keys)
            diff_vals = [(k, stat_1[k], stat_2[k]) for k in same_keys if stat_1[k] != stat_2[k]]
            print("Print diff_vals")
            for val in diff_vals:
                print(val)
            print("========================================")

    elif len(stat_list_1) > len(stat_list_2):
        for i in range(len(stat_list_2)):
            stat_1 = stat_list_1[i][0]
            stat_2 = stat_list_2[i][0]
            print(stat_1)
            print(stat_2)
            print("----------------------------------------")

            # find different value for the same key
            same_keys = stat_1.keys() & stat_2
            # print("Print diff")
            # print(same_keys)
            diff_vals = [(k, stat_1[k], stat_2[k]) for k in same_keys if stat_1[k] != stat_2[k]]
            print("Print diff_vals")
            for val in diff_vals:
                print(val)
            print("========================================")

        # print("Other stats in require_list_1: ")  # which should be added to "Del stat"
        count = len(stat_list_1) - len(stat_list_2)
        frequent_patterns["Del stat"] += count
    elif len(stat_list_1) < len(stat_list_2):
        for i in range(len(stat_list_1)):
            stat_1 = stat_list_1[i][0]
            stat_2 = stat_list_2[i][0]
            print(stat_1)
            print(stat_2)
            print("----------------------------------------")

            # find different value for the same key
            same_keys = stat_1.keys() & stat_2
            # print("Print diff")
            # print(same_keys)
            diff_vals = [(k, stat_1[k], stat_2[k]) for k in same_keys if stat_1[k] != stat_2[k]]
            print("Print diff_vals")
            for val in diff_vals:
                print(val)
            print("========================================")

        # print("Other stats in require_list_2: ")  # which should be added to "Add stat"
        count = len(stat_list_2) - len(stat_list_1)
        frequent_patterns["Add stat"] += count


''''
Get all clauses for a transaction-reverting statement using BFS
input: a transaction-reverting statement 
retrun: a claus list
'''
def get_clauses(tv_stat, clause_list):
    # print(tv_stat)
    origin_stat = tv_stat
    if tv_stat['operator'] == '&&':
        get_clauses(tv_stat['left'], clause_list)
        get_clauses(tv_stat['right'], clause_list)
    else:
        clause_list.append(tv_stat)
    return clause_list


# remove the origin stat for those stat which contains multiple clauses
def preprocess_clause_list(clause_list):
    if len(clause_list) > 1:
        origin_stat = max(clause_list, key=len, default='')
        clause_list.remove(origin_stat)
    return clause_list


def init():
    f = solidity_parser("/Users/luliu/PycharmProjects/solidity-parser-python/samples/simple.sol")
    f2 = solidity_parser("/Users/luliu/PycharmProjects/solidity-parser-python/samples/simple1.sol")
    cus_patterns = {
        "add_clause": 0,
        "add_var": 0,
        "add_stat": 0,
        "delete_clause": 0,
        "delete_var": 0,
        "delete_stat": 0,
        "modify_clause": 0,
        "cosmetic_change": 0,
    }

    get_same_func(f, f2, cus_patterns)


if __name__ == '__main__':
    init()