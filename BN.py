import numpy as np
from itertools import permutations

def computeProbAux(parents, prob, evid):
    if len(parents) == 0:
        return prob[0]   
    if len(parents) == 1:
        return prob[evid[parents[0]]]
    else:
        return computeProbAux(parents[1:],prob[evid[parents[0]]],evid)
    
    
class Node():
    def __init__(self, prob, parents):
        self.parents = parents
        self.prob = prob
    
    def computeProb(self, evid):
        return [1-computeProbAux(self.parents, self.prob, evid),computeProbAux(self.parents, self.prob, evid)]
        
            
    
class BN():
    def __init__(self, gra, prob):
        self.gra = gra
        self.prob = prob
       
    def computeJointProb(self, evid):
        product = 1
        for e in range(len(self.prob)):
            product = product * self.prob[e].computeProb(evid)[evid[e]]  
        return product
    

    def computePostProb(self, evid):
        product = 1
        count = 0 
        n = 1
        ev0 = []
        ev1 = []
        l = []
        index = []
        pa = 0
        pna = 0
        for j in range(len(evid)):
            if evid[j] == -1:
                ev0.append(0)
                ev1.append(1)
            elif evid[j] == []:
                ev0.append([])
                ev1.append([])
                index.append(j)
                count += 1
            else:
                ev0.append(evid[j])
                ev1.append(evid[j])
        n = 2**count
        for e in range(0,n):
            l1 = []
            for d in bin(e)[2:]:
                l1.append(int(d))
            while len(l1) < count:
                l1 = [0] + l1
            l.append(l1)
        if count > 0:
            for m in l:
                for k in range(len(m)):
                    ev0[index[k]] = m[k]
                    ev1[index[k]] = m[k]
                pa += self.computeJointProb(ev1)
                pna += self.computeJointProb(ev0)
        else:
            pa = self.computeJointProb(ev1)
            pna = self.computeJointProb(ev0)
        if (pa + pna) == 0:
            return 0
        return (pa / (pa+pna))
        
     