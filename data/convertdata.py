import scipy.io as sio
import numpy as np

## set the threshold
threshold = 0.01

data = sio.loadmat('Connect_DZ_M1.mat')
## print(np.min(np.nonzero(data['DZ_M'])))
data_array = data['DZ_M']
low_values_indices = data_array < threshold  # find low value indices
print(low_values_indices)
data_array[low_values_indices] = 0

#normalize array
normalized = data_array/np.amin(data_array[np.nonzero(data_array)])
trun = np.trunc(normalized)
print(trun)
np.savetxt('test.json', trun, fmt='%i', delimiter=',')
