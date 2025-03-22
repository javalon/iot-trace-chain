import hashlib

from persistence_worker.utils.hashing import generate_hash


def compute_level(hashes):
    if len(hashes) == 1:
        return hashes[0]
    next_level = []
    for i in range(0, len(hashes), 2):
        left = hashes[i]
        right = hashes[i + 1] if i + 1 < len(hashes) else hashes[i]
        combined = left + right
        next_level.append(hashlib.sha256(combined.encode("utf-8")).hexdigest())
    return compute_level(next_level)


def generate_merkle_root(data):
    if not data:
        raise ValueError("Empty data array")

    # Compute leaf hashes
    leaf_hashes = []
    for item in data:
        leaf_hash = generate_hash(item)
        item["hash"] = leaf_hash
        leaf_hashes.append(leaf_hash)

    return compute_level(leaf_hashes)


def verify_merkle_proof(leaf_hash, proof, root):
    current_hash = leaf_hash
    for sibling in proof:
        if sibling["position"] == "left":
            combined = sibling["hash"] + current_hash
        else:
            combined = current_hash + sibling["hash"]
        current_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return current_hash == root


def generate_merkle_proof(data, target_index):
    if not data:
        raise ValueError("Empty data array")
    if target_index >= len(data):
        raise IndexError("target_index out of range")

    # Compute leaf hashes
    leaf_hashes = []
    for item in data:
        leaf_hash = generate_hash(item)
        leaf_hashes.append(leaf_hash)

    proof = []
    indexes = list(range(len(leaf_hashes)))
    current_level = leaf_hashes
    current_index = target_index

    while len(current_level) > 1:
        next_level = []
        next_indexes = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left

            left_index = indexes[i]
            right_index = indexes[i + 1] if i + 1 < len(current_level) else left_index

            combined = left + right
            parent_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
            next_level.append(parent_hash)
            next_indexes.append(left_index)  # Index of left used as parent ID

            if current_index == left_index:
                proof.append({"position": "right", "hash": right})
            elif current_index == right_index:
                proof.append({"position": "left", "hash": left})

        current_index = next_indexes[indexes.index(current_index) // 2]
        current_level = next_level
        indexes = next_indexes

    return proof
