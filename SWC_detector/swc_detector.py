from z3 import *
import sys
import os
import pprint

from solidity_parser import parser

# Check Assert Violation
def check_assert_violation():
    pass


# Check Requirement Violation
def check_requirement_violation(condition_list):
    # TODO: Use SMT solver to check whether the condition of a require statement is too strong or too weak.
    s = Solver()
    s.add(condition_list)
    result = s.check()
    print(result)


# Check code with no effects
def check_no_effect_code():
    pass


def run(file_path):
    sourceUnit = parser.parse_file(file_path)
    pprint.pprint(sourceUnit)


if __name__ == '__main__':
    file_dir = sys.argv[1]
    files = os.listdir(file_dir)
    for file in files:
        if not os.path.isdir(file):
            continue
        run(file)