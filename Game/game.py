import itertools
import numpy as np
import pandas as pd
from scipy.optimize import linprog
from Equi import PayoffMatrix

class Minion:
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
        self.minons_A = [Minion(m[0], m[1]) for m in minons]
        self.nA = len(self.minons_A)

    def set_minons_B(self, minons: list):
        self.minons_B = [Minion(m[0], m[1]) for m in minons]
        self.nB = len(self.minons_B)

    def get_power(self):
        power = 0
        for minon in self.minons_A:
            # power += minon.current_health + minon.current_attack
            power += minon.current_attack
        for minon in self.minons_B:
            # power -= minon.current_health + minon.current_attack
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
                    return -1000
        power = self.get_power()
        return power

    def full_payoff_table(self):
        As, Bs = self.generate_strats()
        d = np.zeros((len(As), len(Bs)))
        for i in range(len(As)):
            for j in range(len(Bs)):
                d[i][j] = self.payoff(As[i], Bs[j])
        d = pd.DataFrame(d, index=[str(A) for A in As])
        return d

    def reduced_payoff_table(self):
        d = {}
        for index, row in self.full_payoff_table().iterrows():
            row = tuple(row)
            if row in d:
                d[row] += str(index) + ', '
            else:
                d[row] = str(index) + ', '
        data = list(d.keys())
        index = list(d.values())
        return pd.DataFrame(data, index=index)

    def no_dominated_payoff_table(self):
        d = self.reduced_payoff_table()
        A = d.to_numpy()
        row = list(d.index)
        col = list(d.columns)

        del_row = []
        for i in range(len(A)):
            for j in range(len(A)):
                if (A[i] < A[j]).all():
                    del_row.append(i)
                    break

        if del_row != []:
            A = np.delete(A, del_row, axis=0)
            row = np.delete(row, del_row, axis=0)

        del_col = []
        for i in range(len(A[0])):
            for j in range(len(A[0])):
                if (A[:, i] > A[:, j]).all():
                    del_col.append(i)

        if del_col != []:
            A = np.delete(A, del_col, axis=1)
            col = np.delete(col, del_col, axis=1)
        return pd.DataFrame(A, index=row, columns=col)

    def get_eq(self):
        A = self.no_dominated_payoff_table()
        A = np.c_[A, -1*np.ones(len(A)), np.ones(len(A))]
        A = np.r_[A, [[1]*(len(A[0])-2) + [0, 0]], [[-1]*(len(A[0])-2) + [0, 0]]]
        b = np.array([0]*(len(A) - 2) + [1, -1])
        c = np.array([0]*(len(A[0]) - 2) + [1, -1])
        lpA = linprog(b, -1*A.transpose(), c, method='simplex')
        lpB = linprog(c, A, b, method='simplex')
        alpha = np.around(lpA.x[:len(A)-2], decimals=4)
        beta = np.around(lpB.x[:len(A[0])-2], decimals=4)
        value = np.around(lpB.fun, decimals=4)
        return list(alpha), list(beta), value

    def solution(self):
        m = len(self.minons_A)
        n = len(self.minons_B)
        print('****============The Solution of the Game============****')
        print("Player A has ", np.math.factorial(m)*(n+1)**m, " strategies,") # Noqa
        print("Player B has ", n, " strategies.")
        print('========================================================')
        print("The  payoffs table for this game is: ")
        d = self.no_dominated_payoff_table()
        print(d)
        print('========================================================')
        print("The Nash equilibrium of this game is: ")

        alpha, beta, value = self.get_eq()
        As = []
        pa = []
        Bs = []
        pb = []
        for i in range(len(alpha)):
            if alpha[i] != 0:
                As.append(d.index[i])
                pa.append(alpha[i])
                print(
                    "Player A plays: ",
                    d.index[i],  "\nwith the probability:",
                    alpha[i])
                print('--------------')
        print('----------------------------')
        for i in range(len(beta)):
            if beta[i] != 0:
                Bs.append(d.columns[i])
                pb.append(beta[i])
                print(
                    "Player B plays: ",
                    d.columns[i],  "\nwith the probability:",
                    beta[i])
        print("The value of the game is: ", value, '.')
        print('****================================================****')
        return As, pa, Bs, pb


G = Game()
G.set_minons_A([(2, 3), (4, 1)])
G.set_minons_B([(3, 2), (2, 3)])
G.solution()
