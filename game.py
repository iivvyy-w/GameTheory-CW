import itertools
import numpy as np
import pandas as pd


class Minon:
    def __init__(self, attack: int, health: int):
        self._attack = attack
        self._health = health

        self.attack = attack
        self.health = health
        self.death = False
        self.reborn = 0

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

    def restart(self):
        self.attack = self._attack
        self.health = self._health
        self.death = False
        self.reborn = 0

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
            power += minon.health + minon.attack
            power += minon.attack
        for minon in self.minons_B:
            power -= minon.health + minon.attack
            power -= minon.attack
        return power

    def restart(self):
        for m in self.minons_A + self.minons_B:
            m.restart()

    def __repr__(self) -> str:
        return f"Player A: {self.minons_A} \n Player B: {self.minons_B}"


def generate_strats(G: Game):
    m = len(G.minons_A)
    n = len(G.minons_B)
    A_strats = []
    for A_idx in itertools.permutations(list(range(m))):
        for B_idx in itertools.product(
             *tuple([list(range(-1, n)) for _ in range(m)])):
            A_strats.append(list(zip(A_idx, B_idx)))

    B_strats = [_ for _ in range(n)]
    return A_strats, B_strats


def payoff(G: Game, A_strat: list, B_strat: int):
    G.restart()
    G.minons_B[B_strat].reborn = 1
    for a in A_strat:
        if a[1] != -1:
            minon_A = G.minons_A[a[0]]
            minon_B = G.minons_B[a[1]]
            if not minon_A.battle(minon_B):
                return -100
    power = G.get_power()
    return power


def payoff_table(G):
    As, Bs = generate_strats(G)
    data = np.zeros((len(As), len(Bs)))
    for i in range(len(As)):
        for j in range(len(Bs)):
            data[i][j] = payoff(G, As[i], Bs[j])
    df = pd.DataFrame(data, index=[str(A) for A in As])
    return df


G = Game()
G.set_minons_A([(2, 3), (2, 3)])
G.set_minons_B([(2, 3), (2, 3)])

print(payoff_table(G))
