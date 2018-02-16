# Main

# Variables globles:
# Le premier bloc :
genSha = hashlib.sha256()
genSha.update("000".encode('utf-8'))
genesisBlock = Block(0, "0", genSha.hexdigest())

# Taille des preuves
proof_size = 32
# Nombre de noeuds connectés
nb_node = 4000
# Difficulté du PoW
difficulty = "0"
# Liste des forks
#firstChain = Block(10, genesisBlock.hash, genesisBlock.hash)
forks = []
# b = [Block(10, genesisBlock.hash, genesisBlock.hash) for _ in range(100)]
#forks = [Chain(createdChain, b) for _ in range(nb_node)]
# Création des noeuds du réseau
#nodes = [Node(i, forks[i]) for i in range(nb_node)]
nodes = [Node(i, Chain(0, [genesisBlock])) for i in range(nb_node)]

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
