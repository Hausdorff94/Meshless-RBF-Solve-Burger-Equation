import numpy as np

from explicit_RK import *
from expressions import *
from halton_points import HaltonPoints


def Fm(t, X0, uh):
    F = []
    for xn in uh.Mi:
        uh.x = xn
        # yield uh.F_m(X0)[0], uh.J()[0]
        F.append(uh.F_m(X0)[0])
    return np.vstack(F)


Mb = np.array([
    #[0., 0.],
    [0., 0.5],
    #[0., 1.],
    [0.5, 1.],
    #[1., 1.],
    [1., 0.5],
    #[1., 0.],
    [0.5, 0.]
])
nf = 20
r = HaltonPoints(2, nf).haltonPoints()
fxl = r
fxl[:,0] = 0
fxr = r
fxr[:,1] = 1
fyu = r
fyu[0,:] = 0
fyd = r
fyd[1,:] = 1

Mb = np.vstack((fxl, fxr, fyu, fyd))

poly_b = np.array([[-1, -1, 1], [1/2, 3/2, -1], [3/2, 1/8, -3/8]])
npnts = 2
t0, te = 0, 1.
N = 15

uh = assembled_matrix(Mb, npnts, 2, 1, poly_b=poly_b)
X0 = uh.X_0()

#system = explicit_RungeKutta(Fm, X0, t0, te, N, uh)
#system.solve()
#S = system.solution
#print(uh.Mi)
m= uh.M()
q2 = uh.Q2()
k1 = uh.K1()
q1 = uh.Q1()
k2 = uh.K2()
q2 = uh.Q2()
o2 = uh.O2()

K = np.vstack((np.hstack((k1, m, q1)), np.hstack((m.T, k2, q2)), np.hstack((q1.T, q2.T, o2))))

A = np.vstack((np.hstack((k2, q2)), np.hstack((q2.T, o2))))
_, s, __ = np.linalg.svd(A)
print('Condition Number: {:,.2f}'.format(max(s)/min(s)))
#print(S[:, 0])
# # t = S[:, 0]
# # y = S[:, 1]
# a = np.vstack(tuple(exact_sol(timegrid)))
# print(a)
# error = np.linalg.norm(np.vstack(y)-a, axis=-1)
# plt.plot(np.vstack(t), error)
# plt.show()
