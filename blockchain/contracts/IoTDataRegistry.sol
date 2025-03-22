// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract IoTDataRegistry {
    address private immutable owner;

    struct DataRecord {
        bytes32 recordId;
        string dataHash;
        uint256 timestamp;
    }

    mapping(string => DataRecord[]) private deviceData;

    mapping(string => mapping(bytes32 => DataRecord)) private deviceRecordLookup;

    event DataStored(string indexed deviceId, bytes32 recordId, string dataHash, uint256 timestamp);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function storeData(string calldata deviceId, string calldata dataHash) external onlyOwner returns (bytes32) {
        uint256 currentTimestamp = block.timestamp;
        bytes32 recordId = keccak256(abi.encodePacked(deviceId, dataHash, currentTimestamp, msg.sender));

        DataRecord memory dataToSave = DataRecord({
            recordId: recordId,
            dataHash: dataHash,
            timestamp: currentTimestamp
        });

        deviceData[deviceId].push(dataToSave); // For easy retrieval by deviceId
        deviceRecordLookup[deviceId][recordId] = dataToSave; // For direct access by deviceId and recordId
 
        emit DataStored(deviceId, recordId, dataHash, currentTimestamp);
        return recordId;
    }

    function getData(string calldata deviceId) external view returns (DataRecord[] memory) {
        return deviceData[deviceId];
    }

    function getDataWithRecordId(string calldata deviceId, bytes32 recordId) external view returns (bytes32, string memory, uint256) {
        DataRecord memory record = deviceRecordLookup[deviceId][recordId];
        require(record.timestamp != 0, "Record not found for given deviceId and recordId");
        return (record.recordId, record.dataHash, record.timestamp);
    }

    function getOwner() external view returns (address) {
        return owner;
    }
}