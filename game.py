import itertools
import numpy as np
import pandas as pd

class Minon:
    def __init__(self, attack: int, health: int):
        self.attack = attack
        self.health = health
        self.death = False
        self.reborn = False
    
    def set_death(self):
        self.attack = 0
        self.health = 0
        self.death = True
    
    def battle(self, other):
        if self.death or other.death:
            return False
        self.health -= other.attack
        other.health -= self.attack

        for minon in [self, other]:
            if minon.health <= 0:
                if minon.reborn:
                    minon.health = 1
                    minon.reborn = False
                else:
                    minon.set_death()
        return True

    def __repr__(self) -> str:
        return f"({self.attack},{self.health})"

class Game:
    def __init__(self):
        self.minons_A = []
        self.minons_B = []
    
    def set_minons_A(self, minons: list):
        self.minons_A = [Minon(m[0], m[1]) for m in minons]

    def set_minons_B(self, minons: list):
        self.minons_B = [Minon(m[0], m[1]) for m in minons]
    
    def get_power(self):
        power = 0
        for minon in self.minons_A:
            #power += minon.health + minon.attack
            power += minon.attack
        for minon in self.minons_B:
            #power -= minon.health + minon.attack
            power -= minon.attack
        return power

    def __repr__(self) -> str:
        return f"Player A: {self.minons_A} \n Player B: {self.minons_B}"


def payoff(G: Game, A_strat: list, B_strat: int):
    G.minons_B[B_strat].reborn = True
    for a in A_strat:
        if a[1] != -1:
            minon_A = G.minons_A[a[0]]
            minon_B = G.minons_B[a[1]]
            if not minon_A.battle(minon_B):
                return -100
    return G.get_power()


def generate_strats(m, n):
    A_strats = []
    for A_idx in itertools.permutations(list(range(m))):
        for B_idx in itertools.product(*tuple([list(range(-1, n)) for _ in range(m)])):
            A_strat = []
            for a in A_idx:
                for b in B_idx:
                    A_strat.append((a, b))
            A_strats.append(A_strat)

    B_strats = []
    for i in range(n):
        bs = [0 for _ in range(n)]
        bs[i] = 1
        B_strats.append(bs)
    return A_strats, B_strats


def payoff_table(G, As, Bs):
    data = np.zeros((len(As), len(Bs)))
    for i in range(len(As)):
        for j in range(len(Bs)):
            data[i][j] = payoff(G,As[i],Bs[j])
    return data




G = Game()
G.set_minons_A([(2, 3), (1, 4)])
G.set_minons_B([(2, 3), (1, 4)])

m = 2
n = 2


'''
df = pd.DataFrame(data=data, dtype=np.int8, index=[str(i) for i in a_strat_list])
print(df)
'''