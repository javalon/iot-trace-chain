/** @type import('hardhat/config').HardhatUserConfig */

require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.28",
  networks: {
    hardhat: {}, // Red local de Hardhat
    localhost: {
      url: "http://127.0.0.1:8545"
    },
    'hardhat-node': {
      url: "http://hardhat-node:8545",
      chainId: 31337
    }
  }
};
