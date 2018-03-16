import hashlib
import random
import string
import sys
import copy

verbose = False

if sys.argv[1] == '-v':
    verbose = True

# TODO :
#   Donner un avantage au noeud qui à trouvé pour le round suivant (il commence à chercher avant les
#   autres)
#   Mettre en place pondération de noeuds

# BUG(s) :

random.seed(random.SystemRandom())

# Compteur de chaines pour l'id
createdChain = 0

class TxPool:
    def __init__(self, txList):
        self.txList = txList

class Tx:
    def __init__(self, tid):
        global tx_nb
        self.tid = tid
        tx_nb += 1

class Chain:
    def __init__(self, cid, blocks):
        global createdChain
        self.cid = cid
        self.lenght = len(blocks)
        self.blocks = blocks # Liste de blocs
        createdChain += 1

    # Renvoie le dernier bloc de la chaine
    def getLastBlock(self):
        return self.blocks[-1]

    def addBlock(self, block):
        self.blocks.append(block)
        self.lenght += 1
        #self.lenght = len(self.blocks)
        #print('Bloc ajoute a la chaine %d taille = %d'%(self.cid, self.lenght))

class Block:
    def __init__(self, bid, previousHash, hash):
        self.bid = bid
        self.previousHash = previousHash
        self.hash = hash
        self.fork_id = -1 # Initialement le bloc n'appartient à aucune fork
        self.txs = []

class Node:
    def __init__(self, nid, chain):
        self.nid   = nid
        self.chain = chain
        self.found = False # Vrai si le noeud à trouvé un bloc ce round

    def addTxToBlock(bloc, txPool):
        global tx_per_bloc
        bloc.txs = random.sample(txPool, tx_per_bloc)

    # Renvoie une txPool privée des tx minées dans le bloc
    def removeMyTx(bloc, txPool):
        res = [tx for tx in txPool if tx not in bloc.txs]
        return res

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
        return hash.startswith(difficulty)
        # if (hash.startswith(difficulty)):
        #     return True
        # else:
        #     return False


    # Met à jour la chaine actuelle du noeuds en choisissant une fork au hasard
    def chooseFork(self):
        global verbose
        global forks
        randomIndex = random.randint(0,len(forks)-1)
        self.chain = forks[randomIndex]
        if verbose:
            print('Le noeud %d adopte la fork %d'%(self.nid, randomIndex))


# Renvoie la taille de la/les plus grande(s) forks
def longestFork(forks):
    m = 0
    for fork in forks:

        #print('Debug : fork.lenght = %d'%fork.lenght)

        if fork.lenght > m:
            m = fork.lenght
            f = fork

    fork_lenghts = [fork.lenght for fork in forks]
    if verbose:
        print("Chaine la plus longue cid = %d, taille = %d"%(f.cid, m))
        print("Forks : ")
        print(fork_lenghts)
    return m

# Fonction qui renvoie une liste forks mise à jour (ne contenant que les plus longues)
def updateForks(m):
    res = []
    for fork in forks:
        if (fork.lenght >= m):
            res.append(fork)

    return res

maxForkSize = 0

def distributeFork(forks, nodes):
    for node in nodes:
        # node.chain.bid < forks[0].bid
        if (len(forks)>=1 and node.found != True):
            # Dans ce cas le noeud ne travaille pas sur la bonne chaine
            node.chooseFork()

# Remet à false les booléen found des noeuds avant le prochain round
def resetFoundNodes(nodes):
    for node in nodes:
        node.found = False

# Une étape de la simulation de convergence
def step():
    global nodes
    global forks
    global createdChain
    global verbose

    for node in nodes:
        # L'index du bloc actuel
        previousBid = node.chain.getLastBlock().bid
        # Le noeud calcul le hash du dernier block de la chaine
        nodeHash = node.computeProof(node.chain.getLastBlock())
        # Si le hash est une réponse au problème
        if (node.checkHash(nodeHash)):
            # On passe le booléen found à Vrai
            node.found = True
            #print("Le noeud %d a trouve une solution"%node.nid)
            newBid = previousBid + 1
            newPreviousHash = node.chain.getLastBlock().hash
            newBlock = Block(newBid, node.chain.getLastBlock().hash, nodeHash)
            if verbose:
                print("Le noeud %d a trouve une solution cid = %d"%(node.nid,node.chain.cid))
                print('Taille de sa chaine actuelle = %d'%len(node.chain.blocks))

            # On ajoute le bloc à la chaine courante sur laquelle travaille le noeud
            #print("Longueur avant = %d"%len(node.chain.blocks))
            newBlocks = copy.copy(node.chain.blocks)
            newBlocks.append(newBlock)
            #print("Longueur après = %d"%len(node.chain.blocks))

            #node.chain.addBlock(newBlock)
            newChain = Chain(createdChain, newBlocks)
            node.chain = newChain
            forks.append(newChain)
            if verbose:
                print('Taille de sa chaine après = %d'%len(node.chain.blocks))
            if verbose:
                print("Nombre de forks = %d"%len(forks))

            # print('Taille de sa nouvelle chaine = %d'%len(node.chain.blocks))

            # if node.chain not in forks:
            #     if verbose:
            #         print('Nouvelle fork cree !')
            #     forks.append(node.chain)
            #     if verbose:
            #         print('Nombre de forks : %d'%len(forks))

            # if node.chain not in forks:
            #     if verbose:
            #         print('Nouvelle fork cree !')
            #     forks.append(node.chain)
            #     if verbose:
            #         print('Nombre de forks : %d'%len(forks))
    m = longestFork(forks)

    #print('La chaine la plus longe = %d taille = %d'%(m, ))
    print('/// Nb FORKS AVANT UPDATE = %d'%len(forks))

    forks = updateForks(m)

    print('/// Nb FORKS APRES UPDATE = %d'%len(forks))

    distributeFork(forks, nodes)
    resetFoundNodes(nodes)

# # Main 2
#
# # Variables globles:
# # Le premier bloc :
# genSha = hashlib.sha256()
# genSha.update("000".encode('utf-8'))
# genesisBlock = Block(0, "0", genSha.hexdigest())
#
# # Transactions par bloc autrement dit taille des blocs
# tx_per_bloc = 10
# # Taille des preuves
# proof_size = 32
# # Nombre de noeuds connectés
# nb_node = 4000
# # Difficulté du PoW
# difficulty = "0"
# # Compteur de tx pour avoir un tid unique
# tx_nb = 0
#
# print("-- Scalability tests --")
#
# tx_pool = [Tx(tx_nb) for _ in range(20000)]
# print("Nombre de transactions initiales dans la pool : %d"%len(tx_pool))
#
# # Fin Main 2

# Main 1

# Variables globles:
# Le premier bloc :
genSha = hashlib.sha256()
genSha.update("000".encode('utf-8'))
genesisBlock = Block(0, "0", genSha.hexdigest())

# Taille des preuves
proof_size = 32
# Nombre de noeuds connectés
nb_node = 400
# Difficulté du PoW
difficulty = "00"

# Liste des forks

#fistBlock = Block(0, genesisBlock.hash, genesisBlock.hash)
firstChain = Chain(0, [genesisBlock])
forks = [firstChain]

#b = [Block(10, genesisBlock.hash, genesisBlock.hash) for _ in range(100)]
#forks = [Chain(createdChain, b) for _ in range(nb_node)]

# Création des noeuds du réseau
#nodes = [Node(i, forks[i]) for i in range(nb_node)]
nodes = [Node(i, firstChain) for i in range(nb_node)]

max_find = 10
i = 0
print('--- LANCEMENT DE LA SIMULATION --')
print('--- NOMBRE DE NOEUD = %d DIFFICULTE = %d NOMBRE DE FORKS INITIALES = %d ---'
%(nb_node, len(difficulty), len(forks)) )

while i < max_find:
    #previous_lenFork = len(forks)
    #while (len(forks) == previous_lenFork):
    step()
    print('--- PAS %d / %d - NOMBRE DE FORKS : %d ---'%(i+1,max_find,len(forks)))
    i += 1
    c = 0

print('Nombre de forks final: %d'%len(forks))

# print('Taille avant update : %d'%len(forks))
# l = longestFork(forks)
# print("Taille maximum : %d"%l)
# forks = updateForks(l)
# print("Taille apres update : %d"%len(forks))
