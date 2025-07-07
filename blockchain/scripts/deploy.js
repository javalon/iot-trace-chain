const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const networkName = hre.network.name;
  const DEPLOY_INFO_PATH = path.join(__dirname, `../deploy-info.${networkName}.json`);

  if (fs.existsSync(DEPLOY_INFO_PATH)) {
    const info = JSON.parse(fs.readFileSync(DEPLOY_INFO_PATH, "utf8"));
    console.warn(
      `⚠️  The contract has already been deployed at address: ${info.contractAddress}\n` +
      `    Deployer: ${info.deployer}\n` +
      `    Network: ${info.network}\n` +
      `    If you need to redeploy, delete the file ${path.basename(DEPLOY_INFO_PATH)}, and execute again.`
    );
    return;
  }

  const [deployer] = await hre.ethers.getSigners();

  const IotChainContract = await hre.ethers.getContractFactory("IoTDataRegistry");
  const iotChainContract = await IotChainContract.connect(deployer).deploy();
  await iotChainContract.waitForDeployment();

  const contractAddress = await iotChainContract.getAddress();

  // Get the ABI from the contract factory
  const artifact = require("../artifacts/contracts/IoTDataRegistry.sol/IoTDataRegistry.json");
  const abi = artifact.abi;

  const deployInfo = {
    contractAddress,
    deployer: deployer.address,
    network: networkName,
    timestamp: new Date().toISOString(),
    abi: abi,
  };

  fs.writeFileSync(DEPLOY_INFO_PATH, JSON.stringify(deployInfo, null, 2));
  console.log("Contract deployed at:", contractAddress);
  console.log("Contract owner:", deployer.address);
  console.log(`Information saved in ${DEPLOY_INFO_PATH}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });