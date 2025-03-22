const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();  

  const MiContrato = await hre.ethers.getContractFactory("IoTDataRegistry");
  const miContrato = await MiContrato.connect(deployer).deploy();
  await miContrato.waitForDeployment();

  console.log("Contrato desplegado en:", await miContrato.getAddress());
  console.log("Propietario del contrato:", deployer.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });