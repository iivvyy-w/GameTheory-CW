import numpy as np
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
from shapely.geometry import LineString


class PayoffMatrix:  # for two players game 
    def __init__(self, index, columns, payoff):
        self.a = index  # dataframe's index of A's strategies
        self.b = columns  # dataframe's columns of B's strategies 0,1
        self.payoff = payoff  # payoff matrix as a list of lists
        self.matrix = pd.DataFrame(payoff, index=self.a, columns=self.b) # payoff matrix expressed as dataframe

    def findpayoff(self, a, b):
        return self.matrix.loc[a][b]

    def equilibrium(self, display=False):

        #initialization
        m = len(self.a)
        q = sp.Symbol('q')  # for two players only
        qvals = np.arange(0, 1.001, 0.001)
        lines = []
        plt.figure()
        maxg = np.full(shape=len(qvals), fill_value=-100.0)
        nash_equi = -100
        coord = (-100, -100)
        #error = 100

        for i in range(m):
            a = self.a[i]
            g = self.findpayoff(a, 0)*q + self.findpayoff(a, 1)*(1-q)
            lam_g = sp.lambdify(q, g, modules=['numpy'])
            gvals = lam_g(qvals)
            if isinstance(gvals, int):
                gvals = np.full(shape=len(qvals), fill_value=g)
            plt.plot(qvals, gvals, label=g)
            for r in range(len(gvals)):
                if gvals[r] > maxg[r]:
                    maxg[r] = gvals[r]

            line = LineString(np.column_stack((qvals, gvals)))
            if lines == []:
                lines.append(line)
            else:
                for line2 in lines:
                    intersection = line.intersection(line2)
                    #print(intersection)
                    x, y = intersection.xy
                    if len(y) > 0:
                        if y[0] > nash_equi:
                        #if abs(y[0]-nash_e) < error:
                            nash_equi = y[0]
                            coord = (x[0], y[0])
                            #error = abs(y[0]-nash_e)
                lines.append(line)
            
            #nash_e = min(maxg)
            #ecoord = (qvals[maxg.argmin()], maxg[maxg.argmin()])

        if display:
            plt.plot(*(coord), 'ro')
            plt.plot(qvals, maxg, 'k:', label='maximum')
            plt.grid()
            plt.legend()
            plt.show()
        
        return nash_equi, coord


index = [0, 1, 2]
columns = [0, 1]
payoff = [[-2, 6], [3, 1], [4, -1]]
pm = PayoffMatrix(index, columns, payoff)
print(pm.matrix)
print(pm.findpayoff(0, 0))
print(pm.equilibrium(display=True))
nash, coord = pm.equilibrium()
print(nash)
