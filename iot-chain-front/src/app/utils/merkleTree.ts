import * as CryptoJS from "crypto-js";

export class InvalidProof extends Error {
  constructor(message: string) {
    super(message);
    this.name = "InvalidProof";
  }
}

// Utilidades para conversión hex <-> Uint8Array
export function uint8ArrayToHex(arr: Uint8Array): string {
  return Array.from(arr)
    .map(b => b.toString(16).padStart(2, "0"))
    .join("");
}

export function hexToUint8Array(hex: string): Uint8Array {
  if (hex.length % 2 !== 0) throw new Error("Invalid hex string");
  const arr = new Uint8Array(hex.length / 2);
  for (let i = 0; i < arr.length; i++) {
    arr[i] = parseInt(hex.substr(i * 2, 2), 16);
  }
  return arr;
}

export function hexStringToUint8Array(hexString: string): Uint8Array {
    if (!hexString) return new Uint8Array();
    const cleanHex = hexString.startsWith('0x') ? hexString.slice(2) : hexString;
    const matches = cleanHex.match(/.{1,2}/g);
    if (!matches) return new Uint8Array();
    return new Uint8Array(matches.map(byte => parseInt(byte, 16)));
  }

// Necesitas implementar o importar una función de hash y de comparación segura
function compareDigest(a: Uint8Array, b: Uint8Array): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a[i] ^ b[i];
  }
  return result === 0;
}

export class MerkleHasher {
  algorithm: string;
  security: boolean;
  prefx00: Uint8Array;
  prefx01: Uint8Array;

  constructor(algorithm: string, security: boolean = true) {
    this.algorithm = algorithm;
    this.security = security;
    this.prefx00 = security ? new Uint8Array([0x00]) : new Uint8Array([]);
    this.prefx01 = security ? new Uint8Array([0x01]) : new Uint8Array([]);
  }

  private hash(data: Uint8Array): Uint8Array {
    // Solo SHA-256 aquí, pero puedes adaptar para otros algoritmos soportados por crypto-js
    const wordArray = CryptoJS.lib.WordArray.create(data as any);
    const hash = CryptoJS.SHA256(wordArray);

    return hexToUint8Array(hash.toString(CryptoJS.enc.Hex));
  }

  hash_empty(): Uint8Array {
    return this.hash(new Uint8Array([]));
  }

  hash_raw(buff: Uint8Array): Uint8Array {
    return this.hash(buff);
  }

  hash_buff(data: Uint8Array): Uint8Array {
    const combined = new Uint8Array(this.prefx00.length + data.length);
    combined.set(this.prefx00, 0);
    combined.set(data, this.prefx00.length);
    return this.hash(combined);
  }

  hash_pair(buff1: Uint8Array, buff2: Uint8Array): Uint8Array {
    const combined = new Uint8Array(this.prefx01.length + buff1.length + buff2.length);
    combined.set(this.prefx01, 0);
    combined.set(buff1, this.prefx01.length);
    combined.set(buff2, this.prefx01.length + buff1.length);
    return this.hash(combined);
  }
}

export class MerkleProof {
  algorithm: string;
  security: boolean;
  size: number;
  rule: number[];
  subset: number[];
  path: Uint8Array[];
  hasher: MerkleHasher;

  constructor(
    algorithm: string,
    security: boolean,
    size: number,
    rule: number[],
    subset: number[],
    path: Uint8Array[]
  ) {
    this.algorithm = algorithm;
    this.security = security;
    this.size = size;
    this.rule = rule;
    this.subset = subset;
    this.path = path;
    this.hasher = new MerkleHasher(algorithm, security);
  }

  get_metadata() {
    return {
      algorithm: this.algorithm,
      security: this.security,
      size: this.size,
    };
  }

  serialize() {
    return {
      metadata: this.get_metadata(),
      rule: this.rule,
      subset: this.subset,
      path: this.path.map((digest) => uint8ArrayToHex(digest)),
    };
  }

  static deserialize(data: any): MerkleProof {
    const metadata = data.metadata;
    const rule = data.rule;
    const subset = data.subset;
    const path = data.path.map((hex: string) => hexToUint8Array(hex));
    return new MerkleProof(metadata.algorithm, metadata.security, metadata.size, rule, subset, path);
  }

  retrieve_prior_state(): Uint8Array {
    const subpath = this.path.filter((_, i) => this.subset[i]);
    if (subpath.length === 0) {
      return this.hasher.hash_empty();
    }
    let result = subpath[0];
    let index = 0;
    while (index < subpath.length - 1) {
      result = this.hasher.hash_pair(subpath[index + 1], result);
      index += 1;
    }
    return result;
  }


  resolve(): Uint8Array {
    const path = this.rule.map((bit, i) => [bit, this.path[i]] as [number, Uint8Array]);
    if (path.length === 0) {
      return this.hasher.hash_empty();
    }
    let [bit, result] = path[0];
    let index = 0;
    while (index < path.length - 1) {
      const [next_bit, digest] = path[index + 1];
      if (bit === 0) {
        result = this.hasher.hash_pair(result, digest);
      } else if (bit === 1) {
        result = this.hasher.hash_pair(digest, result);
      } else {
        throw new Error("Invalid bit found");
      }
      bit = next_bit;
      index += 1;
    }
    return result;
  }
}

// Funciones de verificación

export function verify_inclusion(base: Uint8Array, root: Uint8Array, proof: MerkleProof) {
  if (!compareDigest(proof.path[0], base)) {
    throw new InvalidProof("Base hash does not match");
  }
  if (!compareDigest(proof.resolve(), root)) {
    throw new InvalidProof("State does not match");
  }
}

export function verify_consistency(state1: Uint8Array, state2: Uint8Array, proof: MerkleProof) {
  if (!compareDigest(proof.retrieve_prior_state(), state1)) {
    throw new InvalidProof("Prior state does not match");
  }
  if (!compareDigest(proof.resolve(), state2)) {
    throw new InvalidProof("Later state does not match");
  }
}