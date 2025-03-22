const { ethers } = require("hardhat");
const { expect } = require("chai");

describe("IoTDataRegistry", function () {
  let oTDataRegistryContract, instancia, owner, addr1;
  const iotDeviceId = "1234567890";
  const dataHash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef";

  beforeEach(async function () {
    oTDataRegistryContract = await ethers.getContractFactory("IoTDataRegistry");
    [owner, addr1] = await ethers.getSigners(); // owner = deployer, addr1 = first test account
    instancia = await oTDataRegistryContract.deploy();
  });

  it("should set the right owner", async function () {
    expect(await instancia.getOwner()).to.equal(owner.address);
  });

  it("should set to the owner the right data", async function () {
    await instancia.storeData(iotDeviceId, dataHash);
    const data = await instancia.getData(iotDeviceId);
    expect(data).to.be.an("array");
    expect(data[0][0]).to.equal(dataHash);
  });

  it("should emit an event when data is stored", async function () {
    await expect(instancia.storeData(iotDeviceId, dataHash))
      .to.emit(instancia, "DataStored")
      .withArgs(iotDeviceId, dataHash,(amount) => { 
        expect(amount).to.be.closeTo(Math.round(Date.now()/1000), 1000); 
        return true; 
      }
    );
  });

  it("should not allow to store data if not the owner", async function () {
    await expect(instancia.connect(addr1).storeData(iotDeviceId, dataHash))
      .to.be.revertedWith("Only owner can call this function");
  });
});