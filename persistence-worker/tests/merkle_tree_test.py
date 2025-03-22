import pytest

from persistence_worker.utils.hashing import generate_hash
from persistence_worker.utils.merkle_tree import generate_merkle_proof, generate_merkle_root, verify_merkle_proof


def test_generate_merkle_root():
    data = [
        {"timestamp": "2021-01-01T00:00:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:01:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:02:00", "temp": "27"},
    ]
    root = generate_merkle_root(data)

    assert isinstance(root, str)
    assert len(root) == 64  # SHA-256 hex digest length


def test_generate_merkle_root_empty_data():
    with pytest.raises(ValueError, match="Empty data array"):
        generate_merkle_root([])


def test_verify_merkle_root_valid():
    index_to_verify = 0
    data = [
        {"timestamp": "2021-01-01T00:00:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:01:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:02:00", "temp": "27"},
    ]
    leaf_hash = generate_hash(data[index_to_verify])
    expected_root = generate_merkle_root(data)
    proof = generate_merkle_proof(data, index_to_verify)
    assert verify_merkle_proof(leaf_hash, proof, expected_root) is True


def test_verify_merkle_root_invalid_root():
    data = [
        {"timestamp": "2021-01-01T00:00:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:01:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:02:00", "temp": "27"},
    ]
    generate_merkle_root(data)
    invalid_root = "0" * 64
    leaf_hash = generate_hash(data[0])
    proof = generate_merkle_proof(data, 0)
    assert verify_merkle_proof(leaf_hash, proof, invalid_root) is False


def test_verify_if_item_belongs_to_merkle_tree():
    index_to_verify = 0
    data = [
        {"timestamp": "2021-01-01T00:00:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:01:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:02:00", "temp": "27"},
    ]
    root = generate_merkle_root(data)
    item = data[index_to_verify]
    leaf_hash = generate_hash(item)
    proof = generate_merkle_proof(data, index_to_verify)
    assert verify_merkle_proof(leaf_hash, proof, root) is True


def test_verify_if_item_does_not_belong_to_merkle_tree():
    index_to_verify = 0
    data = [
        {"timestamp": "2021-01-01T00:00:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:01:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:02:00", "temp": "27"},
    ]
    root = generate_merkle_root(data)
    item = {"timestamp": "2021-01-01T00:03:00", "temp": "28"}
    leaf_hash = generate_hash(item)
    proof = generate_merkle_proof(data, index_to_verify)
    assert verify_merkle_proof(leaf_hash, proof, root) is False


def test_verify_if_item_belongs_to_merkle_tree_loot_items():
    index_to_verify = 8
    data = [
        {"timestamp": "2021-01-01T00:00:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:01:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:02:00", "temp": "27"},
        {"timestamp": "2021-01-01T00:03:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:04:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:05:00", "temp": "27"},
        {"timestamp": "2021-01-01T00:06:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:07:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:08:00", "temp": "27"},
        {"timestamp": "2021-01-01T00:09:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:10:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:11:00", "temp": "27"},
        {"timestamp": "2021-01-01T00:12:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:13:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:14:00", "temp": "27"},
        {"timestamp": "2021-01-01T00:15:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:16:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:17:00", "temp": "27"},
        {"timestamp": "2021-01-01T00:18:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:19:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:20:00", "temp": "27"},
        {"timestamp": "2021-01-01T00:21:00", "temp": "25"},
        {"timestamp": "2021-01-01T00:22:00", "temp": "26"},
        {"timestamp": "2021-01-01T00:23:00", "temp": "27"},
    ]
    root = generate_merkle_root(data)
    item = data[index_to_verify]
    leaf_hash = generate_hash(item)
    proof = generate_merkle_proof(data, index_to_verify)
    assert verify_merkle_proof(leaf_hash, proof, root) is True
