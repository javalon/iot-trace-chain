contract_abi = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "string", "name": "deviceId", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "dataHash", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "name": "DataStored",
        "type": "event",
    },
    {"stateMutability": "payable", "type": "fallback"},
    {
        "inputs": [{"internalType": "string", "name": "deviceId", "type": "string"}],
        "name": "getData",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "dataHash", "type": "string"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                ],
                "internalType": "struct IoTDataRegistry.DataRecord[]",
                "name": "",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "deviceId", "type": "string"},
            {"internalType": "string", "name": "dataHash", "type": "string"},
        ],
        "name": "storeData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {"stateMutability": "payable", "type": "receive"},
]  # ABI del contrato
