import random

class Experiment:
    def __init__(self, q, z, nb_iter, n):
        self.value = nb_iter
        self.q = q
        self.z = z
        self.nb_iter = nb_iter
        self.n = n
        self.results = [0, 0, 0]
        #self.global_results = []

    def step(self, verbose=True):
        if random.random() < self.q:
            self.value += 1
        else:
            self.value -= 1
        #print("Debug : Value = %d"%self.value)

    def start(self):
        for _ in range(self.n):
            while(True):
                self.step()
                if self.value <= 0:
                    self.results[1] += 1 # L'attaquant perd, il n'a plus de ressources
                    #print("Perdu !")
                    self.value = self.nb_iter # On réinitialise avant le prochain lancement
                    break
                if self.value >= self.z + self.nb_iter:
                    self.results[0] += 1 # L'attaquant gagne
                    self.value = self.nb_iter # On réinitialise avant le prochain lancement
                    #print("Gagné")
                    break

        self.results[2] = self.results[0] / (self.results[0] + self.results[1])
        return self.results[2]

def main():
    #e = Experiment(0.4, 1, 36, 1000)
    #r = e.start()
    #print(r)
    z = [3, 6, 12]
    for zz in z:
        x = [0.1, 0.2, 0.3, 0.4, 0.49]
        r = []

        for xx in x:
            e = Experiment(xx, zz - 1, zz - 1 + 35, 100000)
            r.append(e.start())

        print(r)

# Main
main()
