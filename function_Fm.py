import numpy as np

#from explicit_RK import *
#from expressions import *


def Fm(t, X0, uh):
    F = []
    for i, xn in enumerate(uh.Mi):
        uh.x = xn
        F.append(uh.F_m(X0, t, i)[0])
    return np.vstack(F)


def FDM_time(timegrid, Xi, uh):
    solution = dict()
    for dt in timegrid:
        solution[dt] = Xi
        Xi = Xi + dt*Fm(dt, Xi, uh)
    return solution

# Mb = np.array([
#     #[0., 0.],
#     [0., 0.5],
#     [0.5, 1.],
#     #[1., 1.],
#     [1., 0.5],
#     [0.5, 0.],
#     #[0.75, 0.],
#     #[0.75,1.],
#     #[1, 0.75],
#     #[0, 0.75],
#     #Zero
#     #[0., 1.],
#     #[1., 0.],
#     #[1, 1/3],
#     #[0, 2/3],
#     #[1/6, 1],
#     #[1/4, 0]
# ])


# print('X0')
# print(X0)
# X0 = X0 + 0.01*Fm(X0, uh)
# print('X1')
# print(X0)
# X0 = X0 + 0.02*Fm(X0, uh)
# print('X2')
# print(X0)
# X0 = X0 + 0.03*Fm(X0, uh)
# print('X3')
# print(X0)
# X0 = X0 + 0.04*Fm(X0, uh)
# print('X4')
# print(X0)
# uh.x = [0.5, 0.333333333]
# Fm(X0, uh)

# df = pd.DataFrame(np.hstack((uh.Mi, X0)), columns=['x', 'y', 'u', 'v'])

# cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
# sns.scatterplot(x='x', y='y', data=df, hue='u', palette=cmap)
# plt.show()
#system = explicit_RungeKutta(Fm, X0, t0, te, N, uh)
# system.solve()
#S = system.solution
# print(uh.Mi)
# m= uh.M()
# q2 = uh.Q2()
# k1 = uh.K1()
# q1 = uh.Q1()
# mq=np.hstack((m, q1))
# mqt=np.vstack((m.T, q1.T))
# mult1 = np.matmul()

# k2 = uh.K2()
# q2 = uh.Q2()
# o2 = uh.O2()

# q = uh.q
# qm_1 = q(Mb[:,0].reshape(-1,1), Mb[:,1].reshape(-1,1), 1)
# qm_2 = q(Mb[:,0].reshape(-1,1), Mb[:,1].reshape(-1,1), 2)
# qm_3 = q(Mb[:,0].reshape(-1,1), Mb[:,1].reshape(-1,1), 3)
#print(np.hstack((qm_1, qm_2, qm_3)))

# Mi = HaltonPoints(2, nf*4).haltonPoints()
# df_b = pd.DataFrame(Mb, columns=['x', 'y'])
# df_b['Type'] = 'Boundary'
# df_i = pd.DataFrame(Mi, columns=['x', 'y'])
# df_i['Type'] = 'Interior'
# df = pd.concat([df_i, df_b])
# sns.scatterplot(x='x', y='y', data=df, hue='Type')
# plt.legend(loc='upper left')
# #plt.show()
# K = np.vstack((np.hstack((k1, m, q1)), np.hstack((m.T, k2, q2)), np.hstack((q1.T, q2.T, o2))))

# A = np.vstack((np.hstack((k2, q2)), np.hstack((q2.T, o2))))
# _, s, __ = np.linalg.svd(K)
# print('Condition Number: {:,.2f}'.format(max(s)/min(s)))
# print('Determinant K: {:,.2f}'.format(np.linalg.det(K)))
# print('Determinant A: {:,.2f}'.format(np.linalg.det(A)))
#print(S[:, 0])
# # t = S[:, 0]
# # y = S[:, 1]
# a = np.vstack(tuple(exact_sol(timegrid)))
# print(a)
# error = np.linalg.norm(np.vstack(y)-a, axis=-1)
# plt.plot(np.vstack(t), error)
# plt.show()
