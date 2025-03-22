// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "hardhat/console.sol";

contract IoTDataRegistry {
    address private owner;
    struct DataRecord {
        string dataHash;
        uint256 timestamp;
    }

    // Map device ID to data records
    mapping(string => DataRecord[]) private deviceData;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    event DataStored(string indexed deviceId, string dataHash, uint256 timestamp);

    function storeData(string memory deviceId, string memory dataHash) public onlyOwner {
        uint256 currentTimestamp = block.timestamp;
        deviceData[deviceId].push(DataRecord(dataHash, currentTimestamp));
        emit DataStored(deviceId, dataHash, currentTimestamp);
    }

    function getData(string memory deviceId) public view returns (DataRecord[] memory) {
        return deviceData[deviceId];
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    // * receive function
    receive() external payable {
        console.log("Receive function triggered");
        console.log("Sender:", msg.sender);
        console.log("Value:", msg.value);
    }

    // * fallback function
    fallback() external payable {
        console.log("Fallback function triggered");
        console.log("Sender:", msg.sender);
        console.log("Value:", msg.value);
        console.logBytes(msg.data);
    }

}