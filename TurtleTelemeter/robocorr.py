'''
Created on 29 sept. 2014

@author: chevaleyre
'''
import numpy as np
import scipy.signal
import scipy.optimize
import numpy.fft
import matplotlib.pyplot as plt
from math import *

def multiples(x,s):
    return [-x*i for i in range(s)[::-1]] + [x*i for i in range(1,s)]


X = [pow(sin(2*x),1) for x in np.arange(0,10,0.2)]

#plt.plot(X)
#plt.show()


X = (X - np.mean(X)) / np.std(X)

C = scipy.signal.fftconvolve(X, X[::-1])
M = scipy.signal.argrelextrema(C, np.greater)[0]
print "argrelextrema = ",M

M = M  - (len(C)-1)/2
s = (len(M)+1)/2
print M

print [sum(np.abs(M-  multiples(i,s))) for  i in range(1,max(M))]
periode = np.argmin([sum(np.abs(M-  multiples(i,s))) for  i in range(1,max(M))])
print "periode =",periode

def objectiv(X,M):
    return sum(np.abs(M-  multiples(X[0], (len(M)+1)/2 )))

res = scipy.optimize.minimize(lambda X: objectiv(X,M),[0.0])
print "resultat= ",res

plt.plot(C)
plt.show()
