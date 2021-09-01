# Customization Pattern Checker
A static pattern checker built on top of a [python solidity parser](https://github.com/ConsenSys/python-solidity-parser) to identify customization patterns
for transaction-reverting statements in smart contracts. 

The checker is based on **python3**. 

## HowTo
Given the filepath for one custom contract and one template contract: 
```
#> pip install -r requirement.txt
#> python init.py custom_contract_path template_contract_path
```
Then the checker output the result of the occurrences of each customization pattern in the following format:
```
{"add_clause": 0,
 "add_var": 0,
 "add_stat": 0,
 "delete_clause": 0,
 "delete_var": 0,
 "delete_stat": 0,
 "modify_clause": 0,
 "modify_stat_type": 0,
 "cosmetic_change": 0}
```

Due to the complex conditions within transaction-reverting statements, the checker may 
induce imprecise categorization results. To reduce the false alerts, we manually categorized
the transaction-reverting statement dataset to verify the categorization result. 

The below figure shows the final categorization result of customization patterns of transaction-reverting statements
 which can also be found in our paper:
![avatar](/checker_result.png)

