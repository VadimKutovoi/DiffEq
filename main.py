import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import new

from tkinter import *
from math import sin
from math import cos
from math import pi

Fi_a = 3.5
Fi_b = 1
Fi_c = 1

B_a = 0
B_b = 0.25
B_c = -0.25
B_d = -0.5
B_e = -0.5


def FuncFi(x, l):
	return Fi_a * 1 + Fi_b * cos(pi * x / l) + Fi_c * cos(2 * pi * x / l)


def FuncB(x, l):
	return B_a * 1 + B_b * cos(pi * x / l) + B_c * sin(pi * x / l) \
        + B_d * cos(2 * pi * x / l) + B_e * sin(2 * pi * x / l)


def RightConst(y, l, tau):
    x = np.zeros(len(y))
    simpson = 0.0

    simpson += (1 / 3) * ( FuncB(0, l) * y[0] + FuncB(l-2, l) * y[l-2] )

    for i in range(2, l-1, 2):
        simpson += (2 / 3) * (FuncB(i, l) * y[i])

    for i in range(1, l-1, 2):
        simpson += (4 / 3) * (FuncB(i, l) * y[i])

    for i in range(1, len(x)):
        x[i] = y[i] * ((1 / tau) + FuncB(i, l) - simpson)
	
    return x


def main(args):
    print(args)

    global T
    global l
    global a
    global h
    global tau
    global Fi_a
    global Fi_b
    global Fi_c
    global B_a
    global B_b
    global B_c
    global B_d
    global B_e

    T = args[0] ; l = args[1] ; a = args[2] ; h = args[3] ; tau = args[4]
    Fi_a = args[5] ; Fi_b = args[6] ; Fi_c = args[7]
    B_a = args[8] ; B_b = args[9] ; B_c = args[10] ; B_d = args[11] ; B_e = args[12]

    y = np.zeros(l - 1)
    b = np.zeros(l + 1)
    y0 = np.zeros(l + 1)
    B = np.zeros(shape=(l + 1, l + 1))
    yb = np.zeros(l + 1)

    for i in range(len(y)):
        y[i] = FuncFi(i + 1, l)

    for i in range(len(y0)):
        y0[i] = FuncFi(i, l)
        b[i] = FuncB(i, l)

    coef1 = (-1) * (a * a) / (h * h)
    coef2 = ((2 * a * a) / (h * h)) + (1 / tau)

    for i in range(1, l):
        B[i][i - 1] = coef1
        B[i][i] = coef2
        B[i][i + 1] = coef1

    B[0][0] = 1
    B[0][1] = -1
    B[1][0] = 0
    B[l - 1][l] = 0
    B[l][l - 1] = -1
    B[l][l] = 1

    for i in range(len(y)):
        yb[i + 1] = y[i]

    yb[0] = 0
    yb[l] = 0

    for i in range(1, T + 1):
        tmp_y = RightConst(yb, l, tau)
        yb = np.linalg.solve(B, tmp_y)

    print(y)
    print(y0)
    print(yb)

    x = [i for i in range(0, l + 1)]
    plt.style.use('fivethirtyeight')
    #plt.rcParams['figure.figsize']=(16,9)
    mng = plt.get_current_fig_manager()
    mng.resize(width=1600, height=900)
    plt.minorticks_on()
    plt.grid(which='both', color='gray')
    plt.show()

class form:
    def __init__(self, master):

        frame = Frame(master, bg="lightblue")
        frame.pack(anchor = W, expand=True)

        self.labelT = Label(frame, text = "T : ", bg="lightblue")
        self.labelT.pack(padx = 3, pady = 7, side = LEFT)
        self.T = Entry(frame, width = 5)
        self.T.pack(side = LEFT)
        self.T.insert(0, "1")
        self.labelL = Label(frame, text = "l : ", bg="lightblue")
        self.labelL.pack(side = LEFT)
        self.l = Entry(frame, width = 5)
        self.l.pack(side = LEFT)
        self.l.insert(0, "42")
        self.labelA = Label(frame, text = "a : ", bg="lightblue")
        self.labelA.pack(side = LEFT)
        self.a = Entry(frame, width = 5)
        self.a.pack(side = LEFT)
        self.a.insert(0, "2")
        self.labelH = Label(frame, text = "h : ", bg="lightblue")
        self.labelH.pack(side = LEFT)
        self.h = Entry(frame, width = 5)
        self.h.pack(side = LEFT)
        self.h.insert(0, "1")
        self.labelTau = Label(frame, text = "tau : ", bg="lightblue")
        self.labelTau.pack(side = LEFT)
        self.tau = Entry(frame, width = 5)
        self.tau.pack(padx = 3, pady = 7, side = LEFT)
        self.tau.insert(0, "1")

        self.coefFi = []
        self.labelFi = []
        self.coefB = []
        self.labelB = []

        frameFi = Frame(master, bg="lightblue")
        frameFi.pack(anchor=W, expand=True)

        for i in range(3):
            self.coefFi.append(Entry(frameFi,  width = 5))
            self.coefFi[i].pack(padx = 3, pady = 7, side = LEFT)
            self.labelFi.append(Label(frameFi, bg="lightblue"))
            self.labelFi[i].pack(side = LEFT)
        self.labelFi[0].config(text = " + ")
        self.labelFi[1].config(text = " cos(pi * x / l) + ")
        self.labelFi[2].config(text = " cos(2 * pi * x / l) ")

        self.coefFi[0].insert(0, "3")
        self.coefFi[1].insert(0, "1")
        self.coefFi[2].insert(0, "1")
        
        frameB = Frame(master, bg="lightblue")
        frameB.pack(anchor=W, expand=True)


        for i in range(5):
            self.coefB.append(Entry(frameB,  width = 5))
            self.coefB[i].pack(padx = 3, pady = 7, side = LEFT)
            self.labelB.append(Label(frameB, bg="lightblue"))
            self.labelB[i].pack(side = LEFT)
        self.labelB[0].config(text = " + ")
        self.labelB[1].config(text = " cos(pi * x / l) + ")
        self.labelB[2].config(text = " sin(pi * x / l) + ")
        self.labelB[3].config(text = " cos(2 * pi * x / l) + ")
        self.labelB[4].config(text = " sin(2 * pi * x / l) ")

        self.coefB[0].insert(0, "0")
        self.coefB[1].insert(0, "0.25")
        self.coefB[2].insert(0, "-0.25")
        self.coefB[3].insert(0, "-0.5")
        self.coefB[4].insert(0, "-0.5")

        ButtonFrame = Frame(master, bg="lightblue")
        ButtonFrame.pack(anchor=W, padx = 3, pady = 3)
        self.CalcButton = Button(ButtonFrame, text = "Вычислить", command= lambda: self.Calculate(master))
        self.CalcButton.pack(side = TOP)

    def Calculate(self, master):
            self.args = []
            self.args.append(int(self.T.get()))
            self.args.append(int(self.l.get()))
            self.args.append(float(self.a.get()))
            self.args.append(float(self.h.get()))
            self.args.append(float(self.tau.get()))

            self.args.append(float(self.coefFi[0].get()))
            self.args.append(float(self.coefFi[1].get()))
            self.args.append(float(self.coefFi[2].get()))


            self.args.append(float(self.coefB[0].get()))
            self.args.append(float(self.coefB[1].get()))
            self.args.append(float(self.coefB[2].get()))
            self.args.append(float(self.coefB[3].get()))
            self.args.append(float(self.coefB[4].get()))

            #main(self.args)
            new.main(self.args)


if __name__ == '__main__':
    root = Tk()
    root.configure(background='lightblue')
    fb = form(root)
    root.title("Вычислительные методы")
    root.geometry("600x150")
    root.mainloop()
