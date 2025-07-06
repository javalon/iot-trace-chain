# import hashlib
from pymerkle import InmemoryTree as MerkleTree
from pymerkle import verify_inclusion
from persistence_worker.utils.hashing import get_data_string
from pymerkle.hasher import MerkleHasher

# from persistence_worker.utils.hashing import generate_hash


# def compute_level(hashes):
#     if len(hashes) == 1:
#         return hashes[0]
#     next_level = []
#     for i in range(0, len(hashes), 2):
#         left = hashes[i]
#         right = hashes[i + 1] if i + 1 < len(hashes) else left
#         combined = bytes.fromhex(left) + bytes.fromhex(right)
#         next_level.append(hashlib.sha256(combined).hexdigest())
#     return compute_level(next_level)


# def generate_merkle_root(data):
#     if not data:
#         raise ValueError("Empty data array")

#     # Compute leaf hashes
#     leaf_hashes = []
#     for item in data:
#         leaf_hash = generate_hash(item)
#         item["hash"] = leaf_hash
#         leaf_hashes.append(leaf_hash)

#     return compute_level(leaf_hashes)


# def verify_merkle_proof(leaf_hash, proof, root):
#     current_hash = bytes.fromhex(leaf_hash)
#     for step in proof:
#         sibling_hash = bytes.fromhex(step["hash"])
#         if step["position"] == "left":
#             combined = sibling_hash + current_hash
#         else:
#             combined = current_hash + sibling_hash
#         current_hash = hashlib.sha256(combined).digest()
#     return current_hash.hex() == root


# def generate_merkle_proof(data_list, target_value):
#     data_list = data_list.copy()

#     if len(data_list) % 2 != 0:
#         data_list.append("{'__DUMMY__':'__DUMMY__'}")

#     leaf_hashes = [generate_hash(val) for val in data_list]

#     audit_log = []
#     current_level = leaf_hashes
#     current_indices = list(range(len(leaf_hashes)))
#     levels = [current_level.copy()]
#     index_map = [current_indices.copy()]
#     level_num = 0

#     while len(current_level) > 1:
#         next_level = []
#         next_indices = []
#         for i in range(0, len(current_level), 2):
#             left = current_level[i]
#             right = current_level[i + 1] if i + 1 < len(current_level) else left
#             left_index = current_indices[i]
#             right_index = current_indices[i + 1] if i + 1 < len(current_level) else left_index
#             combined = hashlib.sha256(bytes.fromhex(left) + bytes.fromhex(right)).hexdigest()
#             next_level.append(combined)
#             next_indices.append(left_index)

#             audit_log.append({
#                 "level": level_num,
#                 "left_index": left_index,
#                 "right_index": right_index,
#                 "left_hash": left,
#                 "right_hash": right,
#                 "combined_hash": combined
#             })

#         current_level = next_level
#         current_indices = next_indices
#         levels.append(current_level.copy())
#         index_map.append(current_indices.copy())
#         level_num += 1

#     merkle_root = current_level[0]
#     target_index = data_list.index(target_value)
#     current_index = target_index
#     proof = []

#     for entry in audit_log:
#         if entry["left_index"] == current_index:
#             proof.append({
#                 "position": "right",
#                 "hash": entry["right_hash"],
#                 "level": entry["level"]
#             })
#             current_index = entry["left_index"]
#         elif entry["right_index"] == current_index:
#             proof.append({
#                 "position": "left",
#                 "hash": entry["left_hash"],
#                 "level": entry["level"]
#             })
#             current_index = entry["left_index"]

#     return {
#         "leaf_hash": leaf_hashes[target_index],
#         "merkle_root": merkle_root,
#         "proof": proof,
#         "valid": verify_merkle_proof(leaf_hashes[target_index], proof, merkle_root)
#     }

def verify_merkle_proof(leaf_hash, proof, root):
    try:
        verify_inclusion(bytes.fromhex(leaf_hash), bytes.fromhex(root), proof)
    except Exception as e:
        print(f"Merkle proof verification failed: {e}")
        return False
    return True # if verify_inclusion returns without exception, the proof is valid

def generate_merkle_tree(data):
    if not data:
        raise ValueError("Empty data array")
    tree = MerkleTree(algorithm='sha256')
    for item in data:
        index = tree.append_entry(get_data_string(item).encode("utf-8"))
        item["hash"] = tree.get_leaf(index).hex()
    return [
        tree,
        tree.get_state().hex()
    ]

def generate_hash(tree, data):
    hasher = MerkleHasher(tree.algorithm, tree.security)
    return hasher.hash_buff(get_data_string(data).encode("utf-8")).hex()
