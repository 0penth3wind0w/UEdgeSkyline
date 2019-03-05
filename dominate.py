import os

from dataClass import Data, batchImport

# Calculate the probability that data1 dominate data2
# data1: [prob, [location]]
# data2: [prob, [location]]
# ps: bossible prob count
def dominateProbability(data1, data2):
    sump = float(0)
    ps = data1.getPCount()
    for i in range(ps):
        l1 = data1.getLocation(i)
        for j in range(ps):
            l2 = data2.getLocation(j)
            if dominateStat(l1, l2) == True:
                sump += data1.getProb(i)*data2.getProb(j)
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

if __name__ == '__main__':
    data = batchImport('test_rec10_dim2_pos3_rad2.csv', 3)
    lbl = str(input('input the lable of data point: '))
    index = -1
    data1 = Data('tmp',2)
    for i,d in enumerate(data):
        if d.getLabel() == lbl:
            data1 = d
            index = i
            break
    del data[index]

    for d in data:
        print('Probability that '+ lbl + ' dominates ' + d.getLabel() + ' is: ' + str(dominateProbability(data1, d)))
