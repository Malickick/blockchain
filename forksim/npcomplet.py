import hashlib
import random
import string

proof_size = 32
difficulty = "0"
base       = "aefFxZqz2891000"

def computeProof():
    global proof_size
    global base

    sha = hashlib.sha256()
    nonce = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                         string.digits +
                         string.ascii_lowercase)  for _ in range(proof_size))

    toHash = base + nonce
    sha.update(toHash.encode('utf-8'))
    return sha.hexdigest()

# Verifie si le hash trouvé est une solution
def checkHash(hash):
    global difficulty
    if (hash.startswith(difficulty)):
        return True
    else:
        return False


def main():
    global difficulty
    N = 10000


    results = [-1]

    for k in range(6):
        goodHash = 0.0
        attempts = 0.0
        for i in range(N):
            h = computeProof()
            #print(h)
            attempts += 1.0
            if checkHash(h):
                goodHash += 1
            #print('%d hash / %d '%(i,N))
        p = goodHash / attempts
        results.append(p)
        print('p(%d) = %f'%(k+1,p))
        difficulty += "0"
    print("Done")
    print(results)
main()
