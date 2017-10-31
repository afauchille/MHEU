from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from numpy import power, sin, floor

def Michalewicz(X):
    res = 0
    for i, x in enumerate(X):
        res += sin(x) * power(sin((i + 1) * x * x / np.pi), 20)
    return res

# f([0, 0, 0]) = 0
def DeJongF1(X):
    return np.dot(X, X)

# D = 2
# f([1, 1, 1]) = 0
def DeJongF2(X):
    return 100 * (X[1] * X[1] - X[0]) + 1 - X[0]

def DeJongF3(X):
    res = 0
    for x in X:
        res += floor(x)
    return res

#TODO
# D = 2
#f([-1, 0]) = 3
def GP(X):
    f1 = (1 + power(X[0] + X[1] + 1, 2) * (19 - 14 * X[0] + 13 * X[0] * X[0] - 14 * X[1] + 6 * X[0] * X[1] + 3 * X[1] * X[1]))
    f2 = (30 + power(2 * X[0] - 3 * X[1], 2) * (18 - 32 * X[0] + 12 * X[0] * X[0] - 48 * X[1] - 36 * X[0] * X[1] + 27 * X[1] * X[1]))
    return f1 * f2

def Rosenbrock(X):
    res = 0
    for i in range(len(X) - 1):
        x = X[i]
        xp = X[i + 1]
        res += 100 * power(x * x - xp, 2) + x - 1
    return res

def Zakharov(X):
    tmp = np.dot(np.arange(1, X.shape[0] + 1), X) * 0.5
    res = np.dot(X, X) + tmp ** 2 + tmp ** 4
    return res

def Schwefel1(X):
    return -np.sum(X * np.sin(np.sqrt(np.abs(X))))

def plot3D(f, low_pos, high_pos):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = y = np.linspace(low_pos, high_pos, 100)
    X, Y = np.meshgrid(x, y)
    zs = np.array([f(np.array([x,y])) for x,y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel("{}(X, Y)".format(f.__name__))

    plt.show()


funs = [Michalewicz, DeJongF1, DeJongF2, DeJongF3, GP, Rosenbrock, Zakharov, Schwefel1]
bounds = [(0, np.pi), (-5.12, 5.12), (-2.048, 2.048), (-5.12, 5.12), (-2, 2), (-2.048, 2.048), (-5, 10), (-500, 500)]

def fun_test():
    for f, bound in zip(funs, bounds):
        plot3D(f, bound[0], bound[1])
#print(Zakharov(np.array([421, 421, 421])))

#fun_test()
