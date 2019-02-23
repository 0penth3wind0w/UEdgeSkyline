import os
import numpy as np
import random

# generate one data location accouding to dimension and bond
def dimgen(dim, bond=[0,100]):
    result = [random.randint(bond[0],bond[1]) for x in range(dim)]
    return result

# generate csv file
def csvgen(path, records, dimension, possibility):
    with open(path+'/data_'+str(records)+'r'+str(dimension)+'d'+str(possibility)+'p'+'.csv', 'w') as data:
        for record in range(records):
            probs = np.random.dirichlet(np.ones(possibility),size=1).tolist()[0]
            data.write('d_'+str(record)+', ')
            last = len(probs) - 1
            for i,p in enumerate(probs):
                if i == last:
                    data.write(str(p)+', '+str(dimgen(dimension, bond=[0,100]))+'\n')
                else:
                    data.write(str(p)+', '+str(dimgen(dimension, bond=[0,100]))+', ')

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    records = int(input('How many data is needed: '))
    dimension = int(input('How many dimension of data: '))
    possibility = int(input('How many possible output of each data: '))
    csvgen(here,records,dimension,possibility)
    print("Done")
