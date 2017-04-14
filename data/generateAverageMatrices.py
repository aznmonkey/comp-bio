import scipy.io as sio
import numpy as np
import glob 
import csv
import pandas as pd

def generateAverageMatrices(threshold, flag):
    '''
        Args: 
            threshold(float): sets the threshold the data will be filtered to
            flag (Boolean): determine whether or not the values across the diagonal will be zeroed out
    '''
    ##intialize counters
    keys = ['DZ_M','DZ_N', 'DZ_R', 'HC_M', 'HC_N', 'HC_R']
    count = {}
    community_assignments = []
    df = pd.read_csv('CommunityAssignments.csv')
    for key in keys:
        community_assignments.append(df[key])


    ##intialize average arrays for each task-group
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
  
        count[file_key] += 1 #increment counter for that key

        data = sio.loadmat(files)
        
        # sum them up first
        for key in data: # access the matlab dictionary
            if key in keys: # list of keys initialized in the beginning
                data_array = data[key] # access the matrix
                if key == 'DZ_M':
                    average_DZ_M = average_DZ_M + data_array # add the matrices together
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
        average_array = eval('average_' + key) # concatenate variable names and evaluate as variable https://docs.python.org/2/library/functions.html#eval
        average_array = average_array/count[key] # find the average, based on number of examples for that task group
        low_values_indices = average_array < threshold  # find low value indices
        ## print(low_values_indices)
        average_array[low_values_indices] = 0
        
        ## map the rows to the correct communities
        communities = {}
        key_index = keys.index(key)
        community_mapping = community_assignments[key_index]
        max_community = max(community_mapping)
        for i in range(max_community+1):
            if i == 0:
                continue
            communities[i] = [j for j, x in enumerate(community_mapping) if x == i]
        
        ## rearrange the rows
        for i in range(max_community+1):
            if i == 0:
                continue
            for rows in communities[i]:
                if rows == 0:
                    rearranged_array = np.array(average_array[rows])
                else:
                    rearranged_array = np.vstack([rearranged_array, np.array(average_array[rows])])

        
        #average_array is a np array
        # comparing np array to a floating point type using the operator < returns a boolean array of which ones are true and false
        #indexing into this array will perform an operation on all the entries for the indices that are true in this nparray
        
        average_array[low_values_indices] = 0
        
        ## flag to zero out number opposite the diagonal since it's an undirected graph
        if flag == True:
            row = rearranged_array.shape[0]
            col = rearranged_array.shape[1]
            for i in range(0, row):
                for j in range(0, col):
                    if j < i:
                        rearranged_array[i,j] = 0
                        average_array[i,j] = 0
        ## normalize array
        normalized = rearranged_array/np.amin(rearranged_array[np.nonzero(rearranged_array)])*10
        trun = np.trunc(normalized)
        
        normalized_average = average_array/np.amin(average_array[np.nonzero(average_array)])*10
        trun_average = np.trunc(normalized_average)
        ## save to file  
        np.savetxt('average_json/' + key + '_rearranged' + '.json', trun, fmt='%i', delimiter=',')
        np.savetxt('average_json/' + key + '_average' + '.json', trun_average, fmt='%i', delimiter=',')

if __name__ == "__main__":
    threshold = 0.02341644
    generateAverageMatrices(threshold, False)
