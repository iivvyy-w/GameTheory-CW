import matplotlib.pyplot as plt

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
    if x==0:
        return 0
    else:
        return 100-90

def g12(x):
    if x==0:
        return 0
    return 100-55

def g13(x):
    if x==0:
        return 0
    return 100-75

def g14(x):
    if x==0:
        return 0
    return 100-30

def g21(x):
    if x==0:
        return 0
    return 100-40

def g22(x):
    if x==0:
        return 0
    return 100-80

def g23(x):
    if x==0:
        return 0
    return 100-70

def g24(x):
    if x==0:
        return 0
    return 100-20

def g31(x):
    if x==0:
        return 0
    return 100-0

def g32(x):
    if x==0:
        return 0
    return 100-85

def g33(x):
    if x==0:
        return 0
    return 100-10

def g34(x):
    if x==0:
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
    if x==0:
        return 0
    elif x==1:
        return 20
    elif x==2:
        return 30
    elif x==3:
        return 40
    else:
        return 100

def h3(x):
    if x==0:
        return 0
    elif x==1:
        return 30
    elif x==2:
        return 80
    else:
        return 100

def h4(x):
    if x==0:
        return 0
    elif x==1:
        return 60
    elif x==2:
        return 70
    elif x==3:
        return 80
    else:
        return 100

x = [0, 1, 2, 3, 4, 5, 6, 7, 8]

y1 = [f1(i) for i in range(9)]
y2 = [f2(i) for i in range(9)]
y3 = [f3(i) for i in range(9)]

plt.plot(x, y1, '.-r', label='$c^u_1(x)$, win-streak', c='r')
plt.plot(x, y2, '.-r', label='$c^u_2(x)$, no-streak', c='b')
plt.plot(x, y3, '.-r', label='$c^u_3(x)$, lose-streak', c='g')
plt.xlabel('$x$')
plt.ylabel('$c^u_i(x)$')
plt.legend()
plt.grid()
plt.show()

y1 = [h1(i) for i in range(9)]
y2 = [h2(i) for i in range(9)]
y3 = [h3(i) for i in range(9)]
y4 = [h4(i) for i in range(9)]

plt.plot(x, y1, '.-r', label='$c^v_1(x)$, scaling', c='r')
plt.plot(x, y2, '.-r', label='$c^v_2(x)$, mid-speed', c='b')
plt.plot(x, y3, '.-r', label='$c^v_3(x)$, tempo', c='g')
plt.plot(x, y4, '.-r', label='$c^v_4(x)$, burst', c='y')
plt.xlabel('$x$')
plt.ylabel('$c^v_j(x)$')
plt.legend()
plt.grid()
plt.show()
