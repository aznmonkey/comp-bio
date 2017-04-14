import scipy.io as sio
import numpy as np
import glob 


def generateAverageMatrices(threshold, flag):
    '''
        Args: 
            threshold(float): sets the threshold the data will be filtered to
            flag (Boolean): determine whether or not the values across the diagonal will be zeroed out
    '''
    ##intialize counters
    keys = ['DZ_M','DZ_N', 'DZ_R', 'HC_M', 'HC_N', 'HC_R']
    count = {}
     
    ##intialize average arrays
    average_DZ_M = np.zeros((34,34,))
    average_DZ_N = np.zeros((34,34,))
    average_DZ_R = np.zeros((34,34,))
    average_HC_M = np.zeros((34,34,))
    average_HC_N = np.zeros((34,34,))
    average_HC_R = np.zeros((34,34,))

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
                if key == 'DZ_M':
                    average_DZ_M = average_DZ_M + data_array
                elif key == 'DZ_N':
                    average_DZ_N = average_DZ_N + data_array
                elif key == 'DZ_R':
                    average_DZ_R = average_DZ_R + data_array
                elif key == 'HC_M':
                    average_HC_M = average_HC_M + data_array
                elif key == 'HC_N':
                    average_HC_N = average_HC_N + data_array
                else:
                    average_HC_R = average_HC_R + data_array

    ## calculate averages
    for key in keys:
        average_array = eval('average_' + key)
        average_array = average_array/count[key]
        ##print(average_array)
        low_values_indices = average_array < threshold  # find low value indices
        ## print(low_values_indices)
        average_array[low_values_indices] = 0
        
        ## flag to zero out number opposite the diagonal since it's an undirected graph
        if flag == True:
            row = average_array.shape[0]
            col = average_array.shape[1]
            for i in range(0, row):
                for j in range(0, col):
                    if j < i:
                        average_array[i,j] = 0
        ## normalize array
        normalized = average_array/np.amin(average_array[np.nonzero(average_array)])*10
        trun = np.trunc(normalized)
        ## save to file 
        np.savetxt('average_json/' + key + '.json', trun, fmt='%i', delimiter=',')

if __name__ == "__main__":
    threshold = 0.02341644
    generateAverageMatrices(threshold, False)
