import hashlib

nb_node = 0
initial_chain = []
difficulty = "00";

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

    def checkProof(proof, block):
        global difficulty
        return 0

    def computeProof(block):

        while not (sha2.hexdigest().startswith(file_zeros)):
            mes =  proof_old + (''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                                       string.digits +
                                                   string.ascii_lowercase)  for _ in range(p_size))


nodes = [Node(nb_node, initial_chain) for _ in range(10)]
