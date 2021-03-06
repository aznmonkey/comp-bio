import scipy.io as sio
import numpy as np
import glob 


def convertData(threshold, flag):
    '''
        Args: 
            threshold(float): sets the threshold the data will be filtered to
            flag (Boolean): determine whether or not the values across the diagonal will be zeroed out
    '''
    ##intialize counters
    keys = ['DZ_M','DZ_N', 'DZ_R', 'HC_M', 'HC_N', 'HC_R']
    count = {}
    for key in keys:
        count[key] = 0

    for files in glob.glob("./Connect_*"):
        file_key = ''
        for key in keys:
            if files.find(key) > 0:
                file_key = key
  
        count[file_key] += 1

        data = sio.loadmat(files)
        for key in data:
            if key in keys:
                data_array = data[key]
        ##print(data_array)
        low_values_indices = data_array < threshold  # find low value indices
        #print(low_values_indices)
        data_array[low_values_indices] = 0
        
        #flag to zero out number opposite the diagonal since it's an undirected graph
        if flag == True:
            row = data_array.shape[0]
            col = data_array.shape[1]
            for i in range(0, row):
                for j in range(0, col):
                    if j < i:
                        data_array[i,j] = 0
        #normalize array
        normalized = data_array/np.amin(data_array[np.nonzero(data_array)])*10
        trun = np.trunc(normalized)
        np.savetxt('json/' + files[2:14] + str(count[file_key]) +'.json', trun, fmt='%i', delimiter=',')

if __name__ == "__main__":
    threshold = 0.02341644
    convertData(threshold, False)
