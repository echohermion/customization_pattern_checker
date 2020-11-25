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
        require(balances[msg.sender] >= _value);
        require(_to!=msg.sender&&_value>0);
        if(to==123434){
            return false;
        }
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        return true;
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        if(_owner!=_spender){
            throw;
        }
        require(_owner!=address(0)&&_spender!=address(0));
        return allowed[_owner][_spender];
    }
}
