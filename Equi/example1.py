from Equi import PayoffMatrix
from Game import Game

G = Game()
G.set_minons_A([(2, 3), (1, 2)])
G.set_minons_B([(1, 3), (3, 2)])
pm = PayoffMatrix(G.no_dominated_payoff_table())
print(pm.matrix)