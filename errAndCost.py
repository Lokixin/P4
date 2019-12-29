import matplotlib
from matplotlib import pyplot as plt
import numpy as np

file_in = open('/home/dimas/Documentos/Uni/3B/PAV/P4/results/prueba1.txt', 'r')
txt = file_in.readlines()
txt_sp = []
numcoef = []
claserror = []
threshold = []
cost = []
for line in txt:
    txt_sp.append(line.split())
for x in txt_sp:
    for y in range(len(x)):
        if (x[y] == 'CostDetection:'):
            cost.append((x[y+1]))
        elif (x[y].__contains__('error_rate=')):
            claserror.append(x[y])
cost = ''.join(cost)
claserror = ''.join(claserror) 
claserror = claserror.replace('=',' ').replace('%','').split()[1]
cost = cost.replace('[','').replace(']','')
print(claserror +" "+cost)