export const environment = {
  production: true,
  apiUrl: 'http://localhost:8000/graphql/',
  bc_contract_address: '0x8CdaF0CD259887258Bc13a92C0a6dA92698644C0', // Ganache
  //bc_contract_address: '0x5fbdb2315678afecb367f032d93f642f64180aa3', // Hardhat
  bc_abi_contract: [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "string",
          "name": "deviceId",
          "type": "string"
        },
        {
          "indexed": false,
          "internalType": "bytes32",
          "name": "recordId",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "dataHash",
          "type": "string"
        },
        {
          "indexed": false,
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
};