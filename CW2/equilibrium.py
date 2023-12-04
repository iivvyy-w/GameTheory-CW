import numpy as np


def f1(x):
    if x == 0:
        return 0
    elif x <= 4:
        return 10*x+50
    else:
        return 90
def f2(x):
    if x == 0:
        return 0
    else:
        return 50
def f3(x):
    if x == 0:
        return 0
    elif x == 1:
        return 10
    elif x == 2:
        return 40
    else:
        return 100
def g11(x):
    if x == 0:
        return 0
    else:
        return 100-90
def g12(x):
    if x == 0:
        return 0
    return 100-55
def g13(x):
    if x == 0:
        return 0
    return 100-75
def g14(x):
    if x == 0:
        return 0
    return 100-30
def g21(x):
    if x == 0:
        return 0
    return 100-40
def g22(x):
    if x == 0:
        return 0
    return 100-80
def g23(x):
    if x == 0:
        return 0
    return 100-70
def g24(x):
    if x == 0:
        return 0
    return 100-20
def g31(x):
    if x == 0:
        return 0
    return 100-0
def g32(x):
    if x == 0:
        return 0
    return 100-85
def g33(x):
    if x == 0:
        return 0
    return 100-10
def g34(x):
    if x == 0:
        return 0
    return 100-100
def h1(x):
    if x == 0:
        return 0
    elif x == 1:
        return 0
    elif x == 2:
        return 20
    elif x == 3:
        return 60
    else:
        return 100
def h2(x):
    if x == 0:
        return 0
    elif x == 1:
        return 20
    elif x == 2:
        return 30
    elif x == 3:
        return 40
    else:
        return 100
def h3(x):
    if x == 0:
        return 0
    elif x == 1:
        return 30
    elif x == 2:
        return 80
    else:
        return 100
def h4(x):
    if x == 0:
        return 0
    elif x == 1:
        return 60
    elif x == 2:
        return 70
    elif x == 3:
        return 80
    else:
        return 100


f = [f1, f2, f3]
g = np.array([[g11, g12, g13, g14],
              [g21, g22, g23, g24],
              [g31, g32, g33, g34]
              ])
h = [h1, h2, h3, h4]

def potential_f(x):
    res = 0
    for i in range(3):
        for j in range(1, x[i]+1):
            res += f[i](j)
    return res

def potential_g(y):
    res = 0
    for i in range(3):
        for j in range(4):
            for k in range(1, y[i][j]+1):
                res += g[i][j](k)

    return res

def potential_h(z):
    res = 0
    for i in range(4):
        for j in range(1, z[i]+1):
            res += h[i](j)
    return res

def potential(x, y, z):
    return potential_f(x) + potential_g(y) + potential_h(z)


OPT = 1e6
xeq = None
yeq = None
zeq = None

for x1 in range(0, 8+1):
    for x2 in range(0, 8-x1+1):
        x3 = 8-x1-x2

        for y11 in range(0, x1+1):
            for y12 in range(0, x1-y11+1):
                for y13 in range(0, x1-y11-y12+1):
                    y14 = x1 - y11 - y12 - y13

                    for y21 in range(0, x2+1):
                        for y22 in range(0, x2-y21+1):
                            for y23 in range(0, x2-y21-y22+1):
                                y24 = x2 - y21 - y22 - y23

                                for y31 in range(0, x3+1):
                                    for y32 in range(0, x3-y31+1):
                                        for y33 in range(0, x3-y31-y32+1):
                                            y34 = x3 - y31 - y32 - y33

                                            x = [x1, x2, x3]
                                            y = np.array(
                                                [[y11, y12, y13, y14],
                                                 [y21, y22, y23, y24],
                                                 [y31, y32, y33, y34]])
                                            z = [y11+y21+y31, y12+y22+y32, y13+y23+y33, y14+y24+y34]
                                            p = potential(x, y, z)
                                            if p < OPT:
                                                OPT = p
                                                xeq = x
                                                yeq = y
                                                zeq = z
                                            elif p==OPT:
                                                print('eq: p= ', p, ', OPT= ', OPT) 
print(OPT)
print(xeq)
print(yeq)
print(zeq)