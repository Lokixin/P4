from docopt import docopt


def bestValues(filename):
    f = open(filename)
    ff = f.readlines()
    err = []
    cost = []
    ncoefs = []
    for line in ff:
        err.append(float(line.split()[0]))
        cost.append(float(line.split()[1]))
        ncoefs.append(float(line.split()[2]))
        minerr = min(err)
        mincost = min(cost)
        coeferr = int(ncoefs[err.index(minerr)])
        coefcost = int(ncoefs[cost.index(mincost)])
    return minerr, mincost, coeferr, coefcost

USAGE='''
Finds the most optimum values for speaker recognition

Usage:
    enjambre [--help|-h] <file> 

Options:
    --help, -h                        Shows this message
'''

if __name__ == '__main__':
    args = docopt(USAGE)
    filename = args['<file>']
    err,cost,coeferr,coefcost = bestValues(filename)
    print(coefcost)