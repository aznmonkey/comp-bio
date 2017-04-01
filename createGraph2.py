#This file computes most of the graph properties we said we were going to investigate.

#The only thing missing is that it does not yet generate the output files for the global properties, and the path-related properties.
#THIS IS LEFT TO BE DONE.
#Once this is generated, statistical tests also need to be done on the rest of the global properties.

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

    channels = ["FCz", "Fz", "T7", "T8", "FC2", "FC6", "Iz", "P7"]

    outframes = [pandas.DataFrame() for k in range(0, len(channels))]

    lst = ["N", "M", "R"]
    
    for i in lst:
        tup1 = createGraph("DZ_" + i)
        tup2 = createGraph("HC_" + i)

        for j in range(0, len(channels)):
            outframes[j] = pandas.DataFrame({"DZ": tup1[j], "HC":tup2[j]})
            outframes[j].to_csv(i + channels[j] +'.csv')
    
def createGraph(path):
    G =[] # list of graphs for each file
    G_inv = []
    n = 0
    arr = np.ndarray(34)
    dirs = "C:/Anaconda3/Connect_"

    lstFCzDegs = []
    lstFzDegs = []
    lstT7Degs = []
    lstT8Degs = []
    lstFC2Degs = []
    lstFC6Degs = []
    lstIzDegs = []
    lstP7Degs = []

    global labelToIndexMap
    
    # http://stackoverflow.com/questions/14262405/loop-through-all-csv-files-in-a-folder
    for filename in glob.glob(dirs + path + "*.mat"):
        dictionary = sio.loadmat(filename) # this makes  call to open()

        for key in dictionary: #there is only one k-v pair, so this is just 1 iteration
            arr = dictionary[key]
        G.append(nx.Graph())
        G_inv.append(nx.Graph())

        G[n].add_nodes_from(range(0, 33))
        G_inv[n].add_nodes_from(range(0,33))

        for i in range(0,34):
            for j in range(i +1, 34):
                if arr[i][j] >= threshold:
                    G[n].add_edge(i, j, weight = arr[i][j])
                    #convert weights to a second, inverse version
                    G_inv[n].add_edge(i,j,weight=1/(arr[i][j]))

        #Average Clustering Coefficient
        avg = nx.average_clustering(G[n])

        for g in nx.connected_component_subgraphs(G_inv[n]):
            if len(g.nodes()) > 1:
            print(nx.average_shortest_path_length(g))
            
        deg_cent_dict = nx.degree_centrality(G[n])
                # returns a dictionary

        lstFCzDegs.append(deg_cent_dict[labelToIndexMap["'FCz'"]])
        lstFzDegs.append(deg_cent_dict[labelToIndexMap["'Fz'"]])
        lstT7Degs.append(deg_cent_dict[labelToIndexMap["'T7'"]])
        lstT8Degs.append(deg_cent_dict[labelToIndexMap["'T8'"]])
        lstFC2Degs.append(deg_cent_dict[labelToIndexMap["'FC2'"]])
        lstFC6Degs.append(deg_cent_dict[labelToIndexMap["'FC6'"]])
        if labelToIndexMap["'Iz'"] in deg_cent_dict:
            lstIzDegs.append(deg_cent_dict[labelToIndexMap["'Iz'"]])
        else:
            lstIzDegs.append(0)
        lstP7Degs.append(deg_cent_dict[labelToIndexMap["'P7'"]])
        
        #LEFT TO BE DONE: extract properties for select nodes from above from the below dictionaries
        bet_cent_dict = nx.betweenness_centrality(G_inv[n])
        close = nx.closeness_centrality(G_inv[n])


        n+=1

    lst = (lstFCzDegs, lstFzDegs, lstT7Degs, lstT8Degs, lstFC2Degs,lstFC6Degs, lstIzDegs, lstP7Degs)
    return lst
