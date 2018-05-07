# Simulation

import random
import time

# TODO : Implémenter z le nombre de bloc de confirmation
class Race:
    def __init__(self, q, z, nb_iter, n):
        self.p = 1.0 - q
        self.q = q
        self.z = z
        self.nb_iter = nb_iter
        self.n = n
        # Longeur de chaines de l'attaquant et de la partie honête de réseau
        self.attack_chain = 0
        self.honest_chain = 0
        self.results = [0, 0, 0] # Attack wins, Honest wins
        self.global_results = []

    def print_results(self, rr ,verbose=False):
        self.results[2] = self.results[0] / (self.results[0] + self.results[1])
        if verbose :
            print("Attaquant gagne %d fois."%self.results[0])
            print("Honêtes gagnent %d fois."%self.results[1])
            print("p = %f"%self.results[2])
        rr.append(self.results[2])


    # Lance la course
    def start(self):

        #print("Lancement de la simulation")
        #print("p = %f\tq = %f"%(self.p, self.q))
        for _ in range(self.n):
            #start = time.time()
            for _ in range(self.nb_iter):
                self.next_step()
                if self.attack_chain >= self.honest_chain + self.z:
                    break
            #print("A = %d\tH = %d"%(self.attack_chain, self.honest_chain))
            #end = time.time()


            if self.attack_chain >= self.honest_chain + self.z:
                #print("deja") # Déja fait au dessus
                self.results[0] += 1.0
            else:
                self.results[1] += 1.0

            # Réinitialisation des compteurs
            self.attack_chain = 0
            self.honest_chain = 0

        #print("Simulation terminée en %f s."%(end - start))
        #print("Taille de la chaine attaquant : %d"%self.attack_chain)
        #print("Taille de la chaine honête : %d"%self.honest_chain)


    # Simule la prochaine étape temporelle
    def next_step(self, verbose=False):
        random_1 = random.random()
        random_2 = random.random()

        # # # Hypothèse 1 dépendance des probabilités
        # if random_1 < self.q:
        #     if verbose : pass
        #         #print("L'attaquant mine un bloc. len(att) = %d"%self.attack_chain)
        #     self.attack_chain += 1
        # else:
        #     #print("Honete mine un bloc.")
        #     self.honest_chain += 1

        # Hypothèse 2 : Les deux probabilités sont indépendantes
        #Lancé de l'attaquant
        if random_1 < self.q:
            if verbose :
                print("L'attaquant mine un bloc. len(att) = %d"%self.attack_chain)
            self.attack_chain += 1
        # Lancé des noeuds honêtes
        if random_2 > self.q:
            if verbose :
                print("La chaine honête mine un bloc. len(att) = %d"%self.honest_chain)
            self.honest_chain += 1




def main():
    random.seed()
    z = 12
    rr = []
    r = []
    x = [((i)/10.0) for i in range(1,6)]
    x[4] = 0.4999

    for xx in x:
        race = Race(xx, z-1, 1000, 1000)
        race.start()
        race.print_results(rr)
        r.append(race.results)

        #print(r)
    print (x)
    print(rr)
# Main
main()
