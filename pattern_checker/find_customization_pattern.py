from pattern_checker.variable import Variable


def find_cus_patterns(stat1, stat2, cus_patterns):
    if len(stat1) == len(stat2):
        cus_patterns["modify_clause"] += 1
    elif len(stat1) > len(stat2):
        # Extract vars for stat1 and stat2(Note that we only extract the left var for a expression)
        vars_1 = []
        vars_2 = []
        extract_var(stat1, vars_1)
        extract_var(stat2, vars_2)
        if vars_1 == vars_2:
            cus_patterns["add_clause"] += 1
        else:
            cus_patterns["add_var"] += 1
    elif len(stat1) < len(stat2):
        # Extract vars for stat1 and stat2(Note that we only extract the left var for a expression)
        vars_1 = []
        vars_2 = []
        extract_var(stat1, vars_1)
        extract_var(stat2, vars_2)
        if vars_1 == vars_2:
            cus_patterns["delete_clause"] += 1
        else:
            cus_patterns["delete_var"] += 1


# Extract vars for a given statement
def extract_var(stat, vars):
    if stat['type'] == 'BinaryOperation' and stat['operator'] == '&&':
        extract_var(stat['left'])
        extract_var(stat['right'])

    var = Variable(stat['left']['type'], stat['left']['name'])
    vars.append(var)