// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

contract LoadBalancer {

    
    struct Transaction{
        //saving the id of the transaction
        uint256 id;
        //saving the time of the transaction
        uint256 time;
    }

    /// @notice A unique identifier for the Transaction
    mapping(uint256 => Transaction) public exactTransaction;

    /// @notice storing the Transaction's id 
    mapping(uint256 => uint256) queue;
}