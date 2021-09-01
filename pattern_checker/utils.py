from pattern_checker.variable import Variable
from pattern_checker.comment import Comment

# stat1 is the custom contract, stat2 is the template contract
def find_cus_patterns(stat1, stat2, comm1, comm2, cus_patterns):
    vars_1 = []
    vars_2 = []
    vars_1 = extract_var(stat1, vars_1)
    vars_2 = extract_var(stat2, vars_2)

    # Identify and Compare comment field
    comment_1 = None
    comment_2 = None
    if comm1 != "":
        comment_1 = identify_comment_field(comm1)
    if comm2 != "":
        comment_2 = identify_comment_field(comm2)
    if comm1 != comm2 or comment_1 != comment_2:
        cus_patterns["cosmetic_change"] += 1

    # if is_same_var_list(vars_1, vars_2) and len(stat1) == len(stat2):
    clause_num_1 = get_clause_num(stat1, 0)
    clause_num_2 = get_clause_num(stat2, 0)

    if is_same_var_list(vars_1, vars_2) is False and clause_num_1 == clause_num_2:
        cus_patterns = compare_vars(vars_1, vars_2, clause_num_1, clause_num_2, cus_patterns)
    elif is_same_var_list(vars_1, vars_2) and clause_num_1 > clause_num_2:
        cus_patterns["add_clause"] += 1
    elif is_same_var_list(vars_1, vars_2) is False and clause_num_1 > clause_num_2:
        cus_patterns = compare_vars(vars_1, vars_2, clause_num_1, clause_num_2, cus_patterns)
    elif is_same_var_list(vars_1, vars_2) and clause_num_1 < clause_num_2:
        cus_patterns["delete_clause"] += 1
    elif is_same_var_list(vars_1, vars_2) is False and clause_num_1 < clause_num_2:
        cus_patterns = compare_vars(vars_1, vars_2, clause_num_1, clause_num_2, cus_patterns)

    return cus_patterns


# Calculate the number of clauses for each stat
def get_clause_num(stat, num):
    if stat['type'] == 'BinaryOperation' and stat['operator'] == '&&':
        num = get_clause_num(stat['left'], num)
        num = get_clause_num(stat['right'], num)
    else:
        num += 1
    return num


# Compare vars
def compare_vars(vars_1, vars_2, clause_num_1, clause_num_2, cus_patterns):
    if is_same_var_list(vars_1, vars_2):
        return cus_patterns


    if clause_num_1 >= clause_num_2:
        count = 0
        for v in vars_2:
            for v_1 in vars_1:
                if v.var_type != v_1.var_type or v.name != v_1.name:
                    cus_patterns["delete_var"] += 1
                    count += 1
        cus_patterns["add_var"] += clause_num_1 - clause_num_2 + count
    elif clause_num_1 < clause_num_2:
        count = 0
        for v in vars_1:
            for v_1 in vars_2:
                if v.var_type != v_1.var_type or v.name != v_1.name:
                    cus_patterns["add_var"] += 1
                    count += 1
        cus_patterns["delete_var"] += clause_num_2 - clause_num_1 + count

    return cus_patterns


# Identify the comment field within a statement
def identify_comment_field(comm):
    comment_type = comm['type']
    comment_value = comm['value']
    comment = Comment(comment_type, comment_value)
    return comment


# Extract vars for a given statement
def extract_var(stat, vars):
    if stat['type'] == 'BinaryOperation' and stat['operator'] == '&&':
        vars = extract_var(stat['left'], vars)
        vars = extract_var(stat['right'], vars)
    else:
        var_name = ""
        if 'name' in stat['left'].keys():
            var_name = stat['left']['name']
        elif 'base' in stat['left'].keys():
            var_name = stat['left']['base']
        var = Variable(stat['left']['type'], var_name)
        vars.append(var)

    return vars


def extract_same_elem(list1, list2):
    # set1 = set(list1)
    # set2 = set(list2)
    ilist = list1.intersection(list2)
    # iset = set1.intersection(set2)
    return ilist


# Check whether elements in two var lists are the same
def is_same_var_list(vas_1, vas_2):
    if len(vas_1) != len(vas_2):
        return False
    else:
        for i in range(len(vas_1)):
            if vas_1[i].var_type != vas_2[i].var_type or vas_1[i].name != vas_2[i].name :
                return False
    return True
