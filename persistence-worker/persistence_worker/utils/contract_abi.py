contract_abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "string",
          "name": "deviceId",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "bytes32",
          "name": "recordId",
          "type": "bytes32"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "dataHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "DataStored",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "deviceId",
          "type": "string"
        }
      ],
      "name": "getData",
      "outputs": [
        {
          "components": [
            {
              "internalType": "bytes32",
              "name": "recordId",
              "type": "bytes32"
            },
            {
              "internalType": "string",
              "name": "dataHash",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "timestamp",
              "type": "uint256"
            }
          ],
          "internalType": "struct IoTDataRegistry.DataRecord[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "deviceId",
          "type": "string"
        },
        {
          "internalType": "bytes32",
          "name": "recordId",
          "type": "bytes32"
        }
      ],
      "name": "getDataWithRecordId",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getOwner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "deviceId",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "dataHash",
          "type": "string"
        }
      ],
      "name": "storeData",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]