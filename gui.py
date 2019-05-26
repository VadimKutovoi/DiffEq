import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

import math

Fi_a = 3.5
Fi_b = 1
Fi_c = 1
B_a = 0
B_b = 0.25
B_c = -0.25
B_d = -0.5
B_e = -0.5
l = 0
h = 0
tau = 0
a = 0
T = 0

def FuncFi(x, l):
    return Fi_a * 1 + Fi_b * math.cos(math.pi * x / l) + Fi_c * math.cos(2 * math.pi * x / l)


def FuncB(x, l):
    return B_a * 1 + B_b * math.cos(math.pi * x / l) + B_c * math.sin(math.pi * x / l) + \
        B_d * math.cos(2 * math.pi * x / l) + B_e * math.sin(2 * math.pi * x / l)


def RightConst(y, size, tau):
    global l
    x = np.zeros(len(y))
    simpson = 0
    simpson += (1 / 3) * ( FuncB(0, l) * y[0] + FuncB((size - 1)*h, l) * y[size - 1] )

    for i in range(2, size, 2):
        simpson += (2 / 3) * (FuncB(i * h, l) * y[i])

    for i in range(1, size, 2):
        simpson += (4 / 3) * (FuncB(i * h, l) * y[i])

    for i in range(1, len(x) - 1):
        x[i] = y[i] * ((1 / tau) + FuncB(i * h, l) - simpson)

    return x

def main(args):
    print(args)
    global T ; global a ; global l ; global tau ; global h ; global Fi_a 
    global Fi_b ; global Fi_c ; global B_a ; global B_b ; global B_d ; global B_c ; global B_e ;
    T = args[0] ; l = args[1] ; a = args[2] ; h = args[3] ; tau = args[4]
    Fi_a = args[5] ; Fi_b = args[6] ; Fi_c = args[7]
    B_a = args[8] ; B_b = args[9] ; B_c = args[10] ; B_d = args[11] ; B_e = args[12]


    size = int(l / h) + 1
    y = np.zeros(size)
    b = np.zeros(size)
    y0 = np.zeros(size)
    A = np.zeros((size, size))
    B = np.zeros((size, size))
    yb = np.zeros(size)

    for i in range(len(y)):
        y[i] = FuncFi(i * h, l)

    for i in range(len(y0)):
        y0[i] = FuncFi(i * h, l)
        b[i] = FuncB(i * h, l)

    coef1 = (-1) * (a * a) / (h * h)    
    coef2 = ((2 * a * a) / (h * h)) + (1 / tau)

    for i in range(1, size-1):
        A[i][i - 1] = coef1
        A[i][i] = coef2
        A[i][i + 1] = coef1

    A[0][0] = coef2
    A[0][1] = coef1
    A[size-1][size-2] = coef1
    A[size-1][size-1] = coef2

    for i in range(1, size-1):
        B[i][i - 1] = coef1
        B[i][i] = coef2
        B[i][i + 1] = coef1

    B[0][0] = 1
    B[0][1] = -1
    B[1][0] = 0
    B[size - 2][size-1] = 0
    B[size-1][size - 2] = -1
    B[size-1][size-1] = 1

    for i in range(size-1):
        yb[i + 1] = y[i]

    yb[0] = 0
    yb[size-1] = 0


    for i in range(1, T + 1):
        tmp_y = RightConst(yb, size, tau)
        yb = np.linalg.solve(B, tmp_y)

    x = [i * h for i in range(0, size)]

    print(b)
    print(y0)
    print(yb)

    plt.plot(x, yb, color='black')
    plt.plot(x, y0, color='blue')
    plt.plot(x, b, color='red')
    plt.style.use('fivethirtyeight')
    #plt.rcParams['figure.figsize']=(16,9)
    mng = plt.get_current_fig_manager()
    mng.resize(width=1600, height=900)
    plt.minorticks_on()
    plt.grid(which='both', color='gray')
    plt.show()
    