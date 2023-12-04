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

def costf(x):
    return np.sum([x[i]*f[i](x[i]) for i in range(len(x))])

def costg(y):
    m, n = np.shape(y)
    res = 0
    for i in range(m):
        for j in range(n):
            res += y[i][j]*g[i][j](y[i][j])
    return res

def costh(z):
    return np.sum([z[i]*h[i](z[i]) for i in range(len(z))])

def cost(x, y, z):
    return (costf(x) + costg(y) + costh(z))

opt = 10000
optx = [0, 0, 0]
opty = [0]*12
optz = [0]*4

t = 0
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
                                            t+=1
                                            x = [x1, x2, x3]
                                            y = np.array(
                                                [[y11, y12, y13, y14],
                                                 [y21, y22, y23, y24],
                                                 [y31, y32, y33, y34]])
                                            z = [y11+y21+y31, y12+y22+y32, y13+y23+y33, y14+y24+y34]
                                            c = cost(x, y, z)/8
                                            if c < opt:
                                                opt = c
                                                optx = x
                                                opty = y
                                                optz = z
print(t)                                          
print(opt)
print(optx)
print(opty)
print(optz)

x = [2, 4, 2]
y = [[2, 0, 0, 0],
     [0, 3, 1, 0],
     [0, 0, 0, 2]]
z = [2, 3, 1, 2]

print(f3(2)+g34(2)+h4(2))
