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


def plot3D(f, low_pos, high_pos):
    x = np.linspace(low_pos, high_pos, 100)
    y = np.linspace(low_pos, high_pos, 100)
    z = [f([xi, yi]) for xi, yi in zip(x, y)]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z)
    plt.show()

#print(Rosenbrock([0, 1, 2, 3, 4, 5]))
plot3D(DeJongF1, -5.12, 5.12)