contract EIP20 is EIP20Interface {

    uint256 constant private MAX_UINT256 = 2**256 - 1;
    mapping (address => uint256) public balances;

    function EIP20(
        uint256 _initialAmount,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol
    ) public {
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balances[msg.sender] > _value);
        require(msg.sender!=address(0));
        require(_to!=msg.sender);
        if(to==address(0)){
            return false;
        }
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        return true;
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        require(_owner!=_spender);
        require(_owner!=address(0));
        return allowed[_owner][_spender];
    }
}
