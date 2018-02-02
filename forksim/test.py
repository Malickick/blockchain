import hashlib


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

# Main

genSha = hashlib.sha256()
genSha.update("0".encode('utf-8'))
genesisBlock = Block(0, "0", genSha.hexdigest())

nb_node = 0 # Nombre de noeuds
initial_chain = []
difficulty = "00"
proof_size = 32
forks = [] # Contient la liste des fork
nodes = [Node(nb_node, genesisBlock) for _ in range(10)]


def step():
    global nodes
    global forks

    for node in nodes:
        nodeHash = node.computeProof(node.chain)
        if (node.checkHash(nodeHash)):
            print("Le noeud %d à trouvé !"%node.nid)
            newBid = node.chain.bid + 1
            newPreviousHash = node.chain.hash
            newBlock = Block(node.chain.bid + 1, node.chain.hash, nodeHash)
            forks.append(newBlock)

step()

# while (len(forks) < 1):
#     step()
# print(forks)
