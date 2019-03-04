import os

from dataClass import Data, batchImport

# Calculate dominate probability
# data1: [prob, [location]]
# data2: [prob, [location]]
# ps: bossible prob count
def dominateProbability(data1, data2):
    sump = float(0)
    ps = data1.getPCount
    print(ps)
    for i in range(ps):
        l1 = data1.getLocation(i)
        for j in range(ps):
            l2 = data2.getLocation(j)
            print(l1[1])
            print(l2[1])
            if dominateStat(l1[1], l2[1]) == True:
                sump += l1[0]*l2[0]
    return sump

# Show dominate status
# True: loc1 dominate loc2
# False: loc2 dominate loc1
# None: No dominate relation occure
def dominateStat(loc1, loc2):
    axis = len(loc1)
    l1doml2 = 0
    l1eql2 = 0
    l2doml1 = 0
    for i in range(axis):
        if loc1[i] < loc2[i]:
            l1doml2 += 1
        elif loc1[i] > loc2[i]:
            l2doml1 += 1
        else:
            l1eql2 += 1
    if l1doml2 == 0 and l2doml1 != 0:
        return False
    elif l2doml1 == 0 and l1doml2 != 0:
        return True
    else:
        return None
        