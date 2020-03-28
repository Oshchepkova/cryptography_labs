from hashlib import sha256


def compute_hash(data):
    return sha256(data.encode()).hexdigest()


class Node:
    def __init__(self, hash):
        self.hash = hash
        self.parent = None
        self.left_child = None
        self.right_child = None


class MerkleTree:
    def __init__(self, data):
        leaves = []

        for chunk in data:
            node = Node(compute_hash(chunk))
            leaves.append(node)

        self.leaves = leaves
        self.root = self.build_merkle_tree(leaves)

    def build_merkle_tree(self, leaves):
        num_leaves = len(leaves)
        if num_leaves == 1:
            return leaves[0]

        parents = []

        i = 0
        while i < num_leaves:
            left_child = leaves[i]
            right_child = leaves[i + 1] if i + 1 < num_leaves else left_child
            parents.append(self.create_parent(left_child, right_child))
            i += 2
        return self.build_merkle_tree(parents)

    def create_parent(self, left_child, right_child):
        parent = Node(compute_hash(left_child.hash + right_child.hash))
        parent.left_child, parent.right_child = left_child, right_child
        left_child.parent, right_child.parent = parent, parent
        print("Left child: {},\nRight child: {},\nParent: {}\n".format(left_child.hash, right_child.hash, parent.hash))
        return parent

    def get_audit_leaf_path(self, chunk_hash):
        for leaf in self.leaves:
            if leaf.hash == chunk_hash:
                print("Leaf exists")
                return self.generate_audit_leaf_path(leaf)
        return False

    def generate_audit_leaf_path(self, merkle_node, leaf_path=[]):
        if merkle_node == self.root:
            leaf_path.append(merkle_node.hash)
            return leaf_path

        is_left = merkle_node.parent.left_child == merkle_node
        if is_left:
            leaf_path.append((merkle_node.parent.right_child.hash, not is_left))
            return self.generate_audit_leaf_path(merkle_node.parent, leaf_path)
        else:
            leaf_path.append((merkle_node.parent.left_child.hash, is_left))
            return self.generate_audit_leaf_path(merkle_node.parent, leaf_path)


if __name__ == '__main__':
    input_message = input("your message:")
    chunks = list(input_message)
    merkle_tree = MerkleTree(chunks)
    print("main root:", merkle_tree.root.hash)
    leaf = input("leaf for check:")
    chunk_hash = compute_hash(leaf)
    print("leaf hash is:", chunk_hash)
    merkle_tree.get_audit_leaf_path(chunk_hash)



