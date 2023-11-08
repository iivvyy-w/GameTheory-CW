import itertools
import numpy as np
import pandas as pd


class Minon:
    def __init__(self, current_attack: int, current_health: int):
        self.attack = current_attack
        self.health = current_health

        self.current_attack = current_attack
        self.current_health = current_health
        self.death = False
        self.reborn = False

    def set_death(self):
        self.current_attack = 0
        self.current_health = 0
        self.death = True

    def battle(self, other):
        if self.death or other.death:
            return False
        self.current_health -= other.current_attack
        other.current_health -= self.current_attack

        for minon in [self, other]:
            if minon.current_health <= 0:
                if minon.reborn:
                    minon.current_health = 1
                    minon.reborn = False
                else:
                    minon.set_death()
        return True

    def restart(self):
        self.current_attack = self.attack
        self.current_health = self.health
        self.death = False
        self.reborn = 0

    def __repr__(self) -> str:
        return f"({self.current_attack},{self.current_health})"


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
            power += minon.current_health + minon.current_attack
            power += minon.current_attack
        for minon in self.minons_B:
            power -= minon.current_health + minon.current_attack
            power -= minon.current_attack
        return power

    def restart(self):
        for m in self.minons_A + self.minons_B:
            m.restart()

    def __repr__(self) -> str:
        return f"Player A: {self.minons_A} \n Player B: {self.minons_B}"

    def generate_strats(self):
        m = len(self.minons_A)
        n = len(self.minons_B)
        A_strats = []
        for A_idx in itertools.permutations(list(range(m))):
            for B_idx in itertools.product(
                 *tuple([list(range(-1, n)) for _ in range(m)])):
                A_strats.append(list(zip(A_idx, B_idx)))

        B_strats = [_ for _ in range(n)]
        return A_strats, B_strats

    def payoff(self, A_strat: list, B_strat: int) -> int:
        self.restart()
        self.minons_B[B_strat].reborn = True
        for a in A_strat:
            if a[1] != -1:
                minon_A = self.minons_A[a[0]]
                minon_B = self.minons_B[a[1]]
                if not minon_A.battle(minon_B):
                    return -100
        power = self.get_power()
        return power

    def payoff_table(self):
        As, Bs = self.generate_strats()
        data = np.zeros((len(As), len(Bs)))
        for i in range(len(As)):
            for j in range(len(Bs)):
                data[i][j] = self.payoff(As[i], Bs[j])
        df = pd.DataFrame(data, index=[str(A) for A in As])
        return df


G = Game()
G.set_minons_A([(1, 4), (2, 3)])
G.set_minons_B([(2, 1), (2, 3)])

print(G.payoff_table())
