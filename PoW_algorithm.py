import hashlib as hlb
import string
import random
import time

# Fonction PoW qui prend en entrée la preuve précédente et qui résout le problème de la file de zéros avec incrément de difficulté

def pow(proof_old, fileZ_maxsize):
    
    fz_maxsize = fileZ_maxsize # Nombre max de zéros à trouver
    p_size = len(proof_old)  # taille de la preuve
    sha2 = hlb.sha256()
    file_zeros = "0"
    
    while (len(file_zeros) <= fz_maxsize ):

        start = time.time()
        while not (sha2.hexdigest().startswith(file_zeros)): 
            mes =  proof_old + (''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                                       string.digits +
                                                       string.ascii_lowercase)  for _ in range(p_size))) 
                                                        
                
            sha2.update(mes.encode("UTF-8"))

        time_took = time.time() - start
        proof = mes[p_size:]
        print("preuve : ", proof)
        print(sha2.hexdigest())
        print("temps de résolution :", str(time_took)[:4], "secs\n")
        file_zeros += "0"

psize = 5
fzsize = 7
pow("000000", fzsize)
