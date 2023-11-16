import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from shapely.geometry import LineString


class PayoffMatrix:  # for two players game
    def __init__(self, payoff):
        self.a = payoff.index  # dataframe's index of A's strategies
        self.b = payoff.columns  # dataframe's columns of B's strategies 0,1
        self.matrix = payoff  # payoff matrix expressed as dataframe

    def findpayoff(self, a, b):
        return self.matrix.loc[a][b]

    def equilibrium(self, display=False):

        # initialization
        m = len(self.a)
        q = sp.Symbol('q')  # for two players only
        qvals = np.arange(0, 1.001, 0.001)
        lines = []  # store each Linestrings
        plt.figure()
        maxg = np.full(shape=len(qvals), fill_value=-100.0)  # store upper envelope
        nash_equi = -100  # final equi value
        coord = (-100, -100)  # coordinates of min-max
        involved_line = []  # the list stores the lines that intersects at equilibrium for b
        xcoord = []
        ycoord = []  # coordinates of intersections
        all_line = []  # the list stores all intersected line pairs at every intersection
        xerror = 100
        yerror = 100
        index_a = []  # A's strategies' index that involved in the equilibrium

        for i in range(m):
            a = self.a[i]
            g = self.findpayoff(a, 0)*q + self.findpayoff(a, 1)*(1-q)
            lam_g = sp.lambdify(q, g, modules=['numpy'])
            gvals = lam_g(qvals)
            if isinstance(gvals, float):
                gvals = np.full(shape=len(qvals), fill_value=g)
            plt.plot(qvals, gvals, label=g)  # plot g(a_i, beta)
            for r in range(len(gvals)):
                if gvals[r] > maxg[r]:
                    maxg[r] = gvals[r]

            line = LineString(np.column_stack((qvals, gvals)))
            if lines == []:
                lines.append(line)
            else:  # find intersections
                for line2 in lines:
                    intersection = line.intersection(line2)
                    x, y = intersection.xy
                    if len(y) > 0:
                        xcoord.append(x[0])
                        ycoord.append(y[0])
                        all_line.append([line2, line])
                lines.append(line)

        nash_e = min(maxg)
        ecoord = (qvals[maxg.argmin()], nash_e)  # min-max of upper envelope plotted

        for i in range(len(xcoord)):  # the closest exact value to plotted min-max
            x = xcoord[i]
            y = ycoord[i]
            if abs(y-nash_e) < yerror or abs(x - ecoord[0]) < xerror:
                yerror = abs(y-nash_e)
                xerror = abs(x-ecoord[0])
                coord = (x, y)
                nash_equi = y
                involved_line = all_line[i]

        for l in involved_line:
            index_a.append(lines.index(l))

        if display:  # showing the lines, maximum of each q and equilibrium
            plt.plot(*(coord), 'ro', label=coord)
            plt.plot(qvals, maxg, 'k:', label='maximum')
            plt.xlabel('q')
            plt.ylabel('g')
            # plt.title('The upper envelope diagram of the example.')
            plt.grid()
            plt.legend()
            plt.show()
            # plt.savefig("E1.jpg", dpi=300, bbox_inches='tight')

        return nash_equi, coord, index_a

    def equilibrium_a(self):
        """
        Use sympy to calculate the mixed strategies for A after min-max is found.
        """
        nash_equi, coord, index_a = self.equilibrium()

        if len(index_a) == 2:
            strat1 = index_a[0]
            strat2 = index_a[1]
            p = sp.Symbol('p')
            g1 = self.matrix[0][strat1]*p + self.matrix[0][strat2]*(1-p)
            g2 = self.matrix[1][strat1]*p + self.matrix[1][strat2]*(1-p)
            equi_p = float(sp.solve(g1 - g2, p)[0])

        return (equi_p, 1-equi_p)

    def equilibrium_b(self):
        nash, coord, index_a = self.equilibrium()
        q = coord[0]
        return (q, 1-q)
