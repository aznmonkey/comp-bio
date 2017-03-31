# This file was prepared by consulting the documentation for networkx online.

import scipy.io as sio
import networkx as nx
import glob
import numpy as np
import pandas

labelToIndexMap = {}

threshold = 0

# returns a histogram
def avgHist():
    #http://stackoverflow.com/questions/18449136/initialize-empty-matrix-in-python
    sumMatrix = np.zeros((34,34))
    n = 0

    # http://stackoverflow.com/questions/14262405/loop-through-all-csv-files-in-a-folder
    for filename in glob.glob("C:/Anaconda3/Connect_*.mat"):
        dictionary = sio.loadmat(filename) # this makes  call to open()

        arr = np.ndarray(34)

        for key in dictionary: #there is only one k-v pair, so this is just 1 iteration
            arr = dictionary[key]

        for i in range(0,34):
            for j in range(i +1, 34):
                sumMatrix[i][j] += arr[i][j]

        n+=1
    # end for

    meanMatrix = sumMatrix

    for i in range(0,34):
        for j in range(i +1, 34):
            meanMatrix[i][j] /= n

    hist = np.histogram(meanMatrix)

    return hist

def __init__():

    hist = avgHist()
    global threshold
    global labelToIndexMap
    threshold = hist[1][3]

    frame = pandas.read_csv("C:/Anaconda3/channel_info.csv")
    frame.dropna(inplace=True)

    it = 0
    
    for tup in frame.itertuples():
        labelToIndexMap[tup[1]] = it
        it+=1
    
    lst = ["N", "M", "R"]
    for i in lst:
        tup1 = createGraph("DZ_" + i)
        tup2 = createGraph("HC_" + i)

        outframe = pandas.DataFrame({"DZ": tup1[0], "HC": tup2[0]})
        outframe2 = pandas.DataFrame({"DZ": tup1[1], "HC": tup2[1]})
        outframe3 = pandas.DataFrame({"DZ": tup1[2], "HC": tup2[2]})
        outframe4 = pandas.DataFrame({"DZ": tup1[3], "HC": tup2[3]})

        
        outframe.to_csv(i + 'FCz.csv')
        outframe2.to_csv(i + 'Fz.csv')
        outframe3.to_csv(i + 'T7.csv',)
        outframe4.to_csv(i + 'T8.csv')

    
def createGraph(path):
    G =[] # list of graphs for each file
    n = 0
    arr = np.ndarray(34)
    dirs = "C:/Anaconda3/Connect_"

    lstFCzDegs = []
    lstFzDegs = []
    lstT7Degs = []
    lstT8Degs = []

    global labelToIndexMap
    
    # http://stackoverflow.com/questions/14262405/loop-through-all-csv-files-in-a-folder
    for filename in glob.glob(dirs + path + "*.mat"):
        dictionary = sio.loadmat(filename) # this makes  call to open()

        for key in dictionary: #there is only one k-v pair, so this is just 1 iteration
            arr = dictionary[key]
        G.append(nx.Graph())

        G[n].add_nodes_from(range(0, 33))

        for i in range(0,34):
            for j in range(i +1, 34):
                if arr[i][j] >= threshold:
                    G[n].add_edge(i, j, weight = arr[i][j])

        deg_cent_dict = nx.degree_centrality(G[n])
                # returns a dictionary

        lstFCzDegs.append(deg_cent_dict[labelToIndexMap["'FCz'"]])
        lstFzDegs.append(deg_cent_dict[labelToIndexMap["'Fz'"]])
        lstT7Degs.append(deg_cent_dict[labelToIndexMap["'T7'"]])
        lstT8Degs.append(deg_cent_dict[labelToIndexMap["'T8'"]])

        #have to convert weights to a second, inverse version to perform the next function call
        #bet_cent_dict = nx.betweenness_centrality(G[n])

        n+=1

    lst = (lstFCzDegs, lstFzDegs, lstT7Degs, lstT8Degs)
    return lst
