import hashlib

nb_node = 0
initial_chain = []
difficulty = "00";
proof_size = 32;

class Block:
    def __init__(self, bid, previousHash, hash):
        self.bid = 0 # NYI
        self.previousHash = previousHash
        self.hash = hash

class Node:
    def __init__(self, nid, chain):
        global nb_node
        self.nid   = nid
        self.chain = chain
        nb_node += 1

    def whoAmI(self):
        print("I'm node %d"%self.nid)

    # Renvoie vrai si la preuve permet de miner le bloc
    def checkHash(hash, block):
        if (hash.startswith(difficulty)):
            return True
        else:
            return False

    # Renvoie le hash d'une tentative de minage du bloc block
    def computeProof(block):
        global proof_size
        sha = hashlib.sha256()
        nonce = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                             string.digits +
                             string.ascii_lowercase)  for _ in range(proof_size))

        toHash = block.previousHash + nonce
        sha.update(toHash)
        return sha.hexdigest()


nodes = [Node(nb_node, initial_chain) for _ in range(10)]

for node in nodes:
    node.whoAmI()
