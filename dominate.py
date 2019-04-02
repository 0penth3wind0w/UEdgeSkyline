import os

from data.dataClass import Data, batchImport

# 
def dominateProbability(data1, data2):
    """
    Calculate the probability that data1 dominate data2
    
    :param data1: [float, list(int)]
        The [prob, [location]] set of first data
    :param data2: [float, list(int)]
        The [prob, [location]] set of second data
    """
    sump = float(0)
    ps = data1.getPCount()
    for i in range(ps):
        l1 = data1.getLocation(i)
        for j in range(ps):
            l2 = data2.getLocation(j)
            if dominateStat(l1, l2) == True:
                sump += data1.getProb(i)*data2.getProb(j)
    return sump

def dominateStat(loc1, loc2):
    """
    Show dominate status.
    Return status:
        True: loc1 dominate loc2
        False: loc2 dominate loc1
        None: No dominate relation occure

    :param loc1: list()
    :param loc2: list()
    """
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
    data = batchImport('test_30_dim2_pos3_rad2_0100.csv', 3)
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
