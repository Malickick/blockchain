import hashlib
import random
import string

# TODO :
#   Donner un avantage au noeud qui à trouvé pour le round suivant (il commence à chercher avant les
#   autres)
#   Mettre en place pondération de noeuds
#   Créer une classe Chain pour représenter les Forks



random.seed(random.SystemRandom())

class Block:
    def __init__(self, bid, previousHash, hash):
        self.bid = bid
        self.previousHash = previousHash
        self.hash = hash
        self.fork_id = -1 # Initialement le bloc n'appartient à aucune fork

class Node:
    def __init__(self, nid, chain):
        global nb_node
        self.nid   = nid
        self.chain = chain
        self.found = False # Vrai si le noeud à trouvé un bloc ce round

    def whoAmI(self):
        print("I'm node %d"%self.nid)

    # Renvoie le hash d'une tentative de minage du bloc
    def computeProof(self, block):
        global proof_size
        sha = hashlib.sha256()
        nonce = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                             string.digits +
                             string.ascii_lowercase)  for _ in range(proof_size))

        toHash = block.previousHash + nonce
        sha.update(toHash.encode('utf-8'))
        return sha.hexdigest()

    # Verifie si le hash trouvé est une solution
    def checkHash(self, hash):
        if (hash.startswith(difficulty)):
            return True
        else:
            return False

    # Met à jour la chaine actuelle du noeuds en choisissant une fork au hasard
    def chooseFork(self):
        global forks
        randomIndex = random.randint(0,len(forks)-1)
        self.chain = forks[randomIndex]
        #print('Le noeud %d adopte la fork %d'%(self.nid, randomIndex))


# Renvoie la taille de la/les plus grande(s) forks
def longestFork(forks):
    m = 0
    for fork in forks:
        if fork.bid > m:
            m = fork.bid
    return m

# Fonction qui renvoie une liste forks mise à jour (ne contenant que les plus longues)
def updateForks(m):
    res = []
    for fork in forks:
        if fork.bid == m:
            res.append(fork)
    return res


# Main




# Variables globles:
# Le premier bloc :
genSha = hashlib.sha256()
genSha.update("000".encode('utf-8'))
genesisBlock = Block(0, "0", genSha.hexdigest())
# Taille des preuves
proof_size = 32
# Nombre de noeuds connectés
nb_node = 100
# Difficulté du PoW
difficulty = "0"
# Liste des forks
#forks = []
forks = [Block(10, genesisBlock.hash, genesisBlock.hash) for _ in range(100) ]
# Création des noeuds du réseau
nodes = [Node(i, genesisBlock) for i in range(nb_node)]
#
maxForkSize = 0

def distributeFork(forks, nodes):
    for node in nodes:
        # node.chain.bid < forks[0].bid
        if (len(forks)>=1 and  node.found != True):
            # Dans ce cas le noeud ne travaille pas sur la bonne chaine
            node.chooseFork()

# Remet à false les booléen found des noeuds avant le prochain round
def resetFoundNodes(nodes):
    for node in nodes:
        node.found = False

# Une étape de la simulation
def step():
    global nodes
    global forks

    for node in nodes:
        # L'index du bloc actuel
        previousBid = node.chain.bid
        # Le noeud calcul le hash du dernier block de la chaine
        nodeHash = node.computeProof(node.chain)
        # Si le hash est une réponse au problème
        if (node.checkHash(nodeHash)):
            # On passe le booléen found à Vrai
            node.found = True
            #print("Le noeud %d a trouve une solution"%node.nid)
            newBid = previousBid + 1
            newPreviousHash = node.chain.hash
            newBlock = Block(newBid, node.chain.hash, nodeHash)
            print("Le noeud %d a trouve une solution bid = %d"%(node.nid,newBlock.bid))
            # On ajoute le bloc à la chaine courante sur laquel travail le noeud
            node.chain = newBlock
            if node.chain not in forks:
                print('Nouvelle fork cree !')
                forks.append(node.chain)
                print('Nombre de forks : %d'%len(forks))
    m = longestFork(forks)
    forks = updateForks(m)
    distributeFork(forks, nodes)
    resetFoundNodes(nodes)
            #print("Nouveau bloc bid : %d ajoute a la chaine"%newBlock.bid)
            # if (node.chain.fork_id == -1):
            #     forks.append([newBlock])
            #     newBlock.fork_id = len(forks) - 1
            # else:
            #     forks[node.chain.fork_id] = newBlock
            #print('Fork %d cree/modifiee'%newBlock.fork_id)





max_find = 10
i = 0
while i < max_find:
    #previous_lenFork = len(forks)
    #while (len(forks) == previous_lenFork):
    step()
    i += 1
    c = 0

print('Nombre de forks final: %d'%len(forks))


# print('Taille avant update : %d'%len(forks))
# l = longestFork(forks)
# print("Taille maximum : %d"%l)
# forks = updateForks(l)
# print("Taille apres update : %d"%len(forks))
