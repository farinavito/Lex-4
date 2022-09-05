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

    /// @notice Storing the Transaction's id 
    //mapping(uint256 => uint256) queue;

    /// @notice Storign the contract's owner
    address internal owner;

    /// @notice storing if we will have a waiting period of 1 week before transfering Transaction to the queue
    bool internal waitingPeriod = false;

    /// @notice storing the id of the Transaction, which will be picked up i a week
    uint256[] internal waitingQueue;

    /// @notice storing the Transaction's id in the queue
    uint256[] internal queue;

    /// @notice Increasing the id of the Transaction id
    uint256 public queueNum = 0;

    constructor(){
        owner = msg.sender;
    }

    modifier onlyOwner{
        require(owner == msg.sender);
        _;
    }

    /// @notice 
    function initialize(uint256 _id) external {
        //increase the queue's number
        queueNum++;
        //creating a new instance
        Transaction storage newTransaction = exactTransaction[queueNum];
        //storing the id
        newTransaction.id = _id;
        //storing the time
        newTransaction.time = block.timestamp;
        //check if the waiting period is on
        if(waitingPeriod == false){
            queue.push(newTransaction.id);
        } else {
            waitingPeriod.push(newTransaction.id);
        }

    }

    /// @notice set the waiting period to false
    function setWaitingPeriodFalse() onlyOwner {
        waitingPeriod = false;
    }


}