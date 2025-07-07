

import { Injectable } from '@angular/core';
import Web3 from 'web3';
import { Contract } from 'web3';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class Web3Service {
  private web3: Web3;
  private contract: Contract<any>;
  private merkleRootCache = new Map<string, string>();

  // Replace these with your actual contract ABI and address
  private contractABI = environment.bc_abi_contract;
  private contractAddress = environment.bc_contract_address;

  constructor() {
    if ((window as any).ethereum) {
      this.web3 = new Web3((window as any).ethereum);
      this.contract = new this.web3.eth.Contract(this.contractABI, this.contractAddress);
    } else {
      throw new Error('Ethereum provider not found');
    }
  }

  async getMerkleRoot(deviceId: string, recordId: string): Promise<string> {
    const cacheKey = `${deviceId}:${recordId}`;

    if (this.merkleRootCache.has(cacheKey)) {
      console.log('Cache hit for Merkle root:', cacheKey);
      return this.merkleRootCache.get(cacheKey) as string;
    }

    try {
      console.log('Cache miss for Merkle root:', cacheKey);
      // recordId should be a bytes32 type, so we convert it to bytes32 format
      const recordIdBytes32 = recordId.startsWith('0x') ? recordId : '0x' + recordId;
      type GetDataWithRecordIdResult = [string, string, string];
      const result = await this.contract.methods['getDataWithRecordId'](deviceId, recordIdBytes32).call() as GetDataWithRecordIdResult;
      const merkleRoot = result[1]; // result[1] corresponds to merkle root hash

      this.merkleRootCache.set(cacheKey, merkleRoot);
      
      return merkleRoot;
    } catch (error) {
      console.error('Error calling getDataWithRecordId:', error);
      throw error;
    }
  }
}