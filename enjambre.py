import numpy as np 
import random
from docopt import docopt
## Funciones para actualizar los valores 

def updateVelocity(V, X, BestCols, Best):
    rp = np.random.rand(1,1)
    rg = np.random.rand(1,1)
    V = np.round(V + rp*(BestCols - X) + rg*(Best-X))
    return V

def updateValues(X,V):
    r = X+V 
    r = np.where(r > 0, r, abs(r) +1)
    return r

def newSource(maxVal, minVal, nelem):
    X = np.round(minVal + np.random.rand(1,nelem)*(maxVal-minVal))
    return X

def computeChance(allresults):
    return allresults/sum(np.sum(allresults))

def computeScore(error, coste):
    return 2*(10*error+coste)/(100*error+coste)

def computeCost(fichero):
    file_in = open(fichero,'r')
    errCost = file_in.readlines()
    err = []
    cost = []
    for line in errCost:
        err.append(float(line.split()[0]))
        cost.append(float(line.split()[1]))
    err = np.array(err)
    cost = np.array(cost)
    return computeScore(err,cost)




########################################################################################################
# Main Program
########################################################################################################

USAGE='''
Finds the most optimum values for speaker recognition

Usage:
    enjambre [--help|-h] <iteracion> <iteracionnum> <downbound> <upbound>

Options:
    --help, -h                        Shows this message
'''

if __name__ == '__main__':
    args = docopt(USAGE)
    it = int(args['<iteracion>'])
    itnum = int(args['<iteracionnum>'])
    Cup = int(args['<upbound>'])
    Cdown = int(args['<downbound>'])
    bestPos = 0
    results = 'results/prueba2.txt'
    values = 'scripts/values.npy'
    costs = 'scripts/costs.npy'
    speed = 'scripts/speed.npy'

    if it == 0: 
        Cinit = np.random.randint(Cdown, high=Cup,size=itnum)
        Vinit = np.random.randint(-(Cup-Cdown), high=(Cup-Cdown), size=itnum)
        Xnew = updateValues(Cinit, Vinit)
        Xtotal = Cinit.copy()
        allcosts = 255*np.ones((itnum,itnum),float)
        np.save(values,Xtotal)
        np.save(costs,allcosts)
        np.save(speed,Vinit)
        output = np.array2string(Cinit).replace("[","").replace("]","").replace(".","")
        print(output)

    else:
        Coefs = np.load(values)
        Vel = np.load(speed)
        Cost = np.load(costs)
        costeTotal = computeCost(results)  
        posx,posy = np.argwhere(Cost == 255)[0]
        Cost[posx] = costeTotal
        bestPosx,bestPosy = np.unravel_index(np.argmin(Cost),Cost.shape)
        if len(Coefs.shape) > 1:
            N,M = Coefs.shape
            lastCoefs = Coefs[N-1,:]
            bestValGroup = Coefs[bestPosx,bestPosy]
            bestValCols = Coefs[np.argmin(Cost, axis = 0),np.arange(itnum)]
        else:
            N = len(Coefs)
            lastCoefs = Coefs[N-1]
            bestValGroup = Coefs[bestPosy]
            bestValCols = Coefs[np.argmin(Cost, axis = 0)]  
        Vnew = updateVelocity(Vel, lastCoefs, bestValCols, bestValGroup)
        Xnew = updateValues(lastCoefs,Vnew)    
        Xtotal = np.vstack([Coefs, Xnew])
        np.save(values,Xtotal)
        np.save(costs,Cost)
        np.save(speed, Vnew)
        output = np.array2string(Xnew).replace("[","").replace("]","").replace(".","")
        print(output)

