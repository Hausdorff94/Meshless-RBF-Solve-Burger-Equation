import numpy as np
from scipy.linalg import lu_factor, lu_solve

from expressions import *


class Onestepmethod(object):
    def __init__(self, f, y0, t0, te, N, tol):
        self.f = f
        self.y0 = y0.astype('float')
        self.t0 = t0
        self.interval = [t0, te]
        self.grid = np.linspace(t0, te, N+2)
        self.h = (te-t0)/(N+1)
        self.N = N
        self.tol = tol
        self.dm = y0.ndim
        self.s = 2#len(self.b)

    def step(self):
        ti, yi = self.grid[0], self.y0
        t_i = ti
        yield np.array([ti]), yi
            
        for ti in self.grid[1:]:
            yi = yi + self.h*self.phi(t_i, yi)
            t_i = ti
            yield np.array([ti]), yi

    def solve(self):
        #print(np.array(list(self.step()))[:,:,0])
        self.solution = np.array(list(self.step()))


class RungeKutta_implicit(Onestepmethod):
    def phi(self, ti, yi):
        '''
        Calculates the sum of b_j*Y_j in one step of the Runge-Kutta method with y_{n+1}= y_n + h*sum_{j=1}^s b_j *Y
        where j=1,2,...,s and s is the number of stages, b the notes and Y the stages values.

        Parameters:
        ----------------
        t0 = float, current timestep
        y0 = 1xm vector, the last solution y_n. Where m is the lenght of the IC y_0 of IVP.

        '''
        M = 10
        stageDer = np.array(self.s*[self.f(ti, yi)])  # Initial value Y'_0
        print(stageDer)
        #J = nd.Jacobian(self.f)([t0, y0[0]])
        # J = nd.Jacobian(self.f, t0, y0)

        J = np.array([-5])
        #J = np.array([[0, 1], [-1, 0]])
        #J = np.array([[0, 1], [-9.8*np.cos(yi[0]), 0]])
        stageVal = self.phi_solve(ti, yi, stageDer, J, M)
        return np.dot(self.b, stageVal.reshape(self.s, self.dm))
        # -|-return np.array([np.dot(self.b, stageVal.reshape(self.s, self.dm)[:, j]) for j in range(self.dm)])

    def phi_solve(self, t0, y0, initVal, J, M):
        '''
        This function solves the sm x sm system
        F(Y_i)=0 by Newton method with initial guess initVal.

        Parameters:
        ______________
        t0 = float, current timestep.
        y0 = 1 x m vector, the last solution y_n.
            Where m is the length on the initial condition
            y_0 of the IVP.
        initVal = Initial guess for the Newton iteration.
        J = m x m matrix, the Jacobian matrix of f()
            evaluated in y_i
        M = Maximal number of Newton iterations

        Returns:
        ______________
        The stage derivative Y'_i               
        '''
        print(initVal)
        JJ = np.eye(self.s * self.dm) - self.h * np.kron(self.A, J)
        luFactor = lu_factor(JJ)

        for i in range(M):
            initVal, norm_d = self.phi_newtonstep(t0, y0, initVal, luFactor)
            if norm_d < self.tol:
                print('Newton converged in {} steps'.format(i))
            elif i == M-1:
                raise ValueError('The Newton iteration did not converge.')

        return initVal

    def phi_newtonstep(self, t0, y0, initVal, luFactor):
        '''
        Takes one Newton step by solving
            G'(Y_i)(Y^{n+1}_{i} - Y^{n}_{i}) = -G(Y_i)

        where,
            G(Y_i) = Y_i - y_n - h * sum(a_{ij} * Y'_j)
                for j = 1,...,s

        Parameters:
        ______________
        t0 = 
        y0 =
        '''

        d = lu_solve(luFactor, -self.F(initVal.flatten(), t0, y0))

        return initVal.flatten() + d, np.linalg.norm(d)

    def F(self, stageDer, t_n, y_i):
        '''
        Returns the substraction Y'_i-
        '''
        stageDer_new = np.empty((self.s, self.dm))
        # print(stageDer.shape)

        for i in range(self.s):

            stageVal = y_i + self.h * np.dot(
                self.A[i, :], stageDer.reshape(self.s, self.dm))
            # -|-stageVal = y_i + np.array([self.h * np.dot(
            #     self.A[i, :], stageDer.reshape(self.s, self.dm)[:, j]) for j in range(self.dm)])

            stageDer_new[i, :] = self.f(t_n + self.c[i] * self.h, stageVal)

        return stageDer - stageDer_new.reshape(-1)


class SDIRK(RungeKutta_implicit):
    def phi_solve(self, t0, y0, initVal, J, M):
        '''
        This function solves F(Y_i)=0
        '''
        print('phi_solve')
        alpha = self.A[0, 0]

        JJ = np.eye(self.dm) - self.h * alpha * J

        luFactor = lu_factor(JJ)

        for i in range(M):
            initVal, norm_d = self.phi_newtonstep(
                t0, y0, initVal, J, luFactor)
            if norm_d < self.tol:
                print('Newton converged in {} steps'.format(i))
                break
            elif i == M-1:
                raise ValueError('The Newton iteration did not converge.')

        return initVal

    def phi_newtonstep(self, t0, y0, initVal, J, luFactor):
        '''
        Takes on Newton step by solving
        '''
        print('phi_newtonstep')
        x = []
        for i in range(self.s):
            rhs = -self.F(initVal.flatten(), t0, y0)[i * self.dm:(i+1) * self.dm] + np.sum(
                [self.h * self.A[i, j] * np.dot(J, x[j]) for j in range(i)], axis=0)
            d = lu_solve(luFactor, rhs)
            x.append(d)

        return initVal + x, np.linalg.norm(x)


class Gauss(RungeKutta_implicit):
    A = np. array([
        [5/36, 2/9 - np.sqrt(15)/15, 5/36 - np.sqrt(15)/30],
        [5/36 + np.sqrt(15)/24, 2/9, 5/36 - np.sqrt(15)/24],
        [5/36 + np.sqrt(15)/30, 2/9 + np.sqrt(15)/15, 5/36]
    ])
    b = np.array([5/18, 4/9, 5/18])
    c = np.array([1/2-np.sqrt(15)/10, 1/2, 1/2 + np.sqrt(15)/10])


class SDIRK_tableau2s(SDIRK):
    p = (3 - np.sqrt(3))/6
    A = np.array([[p, 0], [1 - 2*p, p]])
    b = np.array([1/2, 1/2])
    c = np.array([p, 1-p])


class SDIRK_tableau5s(SDIRK):
    A = np.array([
        [1/4, 0, 0, 0, 0],
        [1/2, 1/4, 0, 0, 0],
        [17/50, -1/25, 1/4, 0, 0],
        [371/1360, -137/2720, 15/544, 1/4, 0],
        [25/24, -49/48, 125/16, -85/12, 1/4]
    ])
    b = np.array([25/24, -49/48, 125/16, -85/12, 1/4])
    c = np.array([1/4, 3/4, 11/20, 1/2, 1])
