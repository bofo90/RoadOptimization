import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial import distance


def connect_points(houses, malls, city_center, alpha):
    
    
    houses_and_malls = np.concatenate((houses,malls), axis=0)
    size_houses = np.shape(houses)[0]
    size_malls = np.shape(malls)[0]
    tot_size = size_houses + size_malls
    
    edges = obtain_Delaunay(houses_and_malls)
    weights = get_weigths_edges(houses_and_malls, edges, alpha, size_houses)
    graph_w_weights = edges_to_matrix(tot_size, edges, weights)   
    opt_edges, opt_weights = obtain_MST(graph_w_weights)
    compl_edges, compl_weights = add_city_center(houses_and_malls, city_center, 
                                                 size_houses, opt_edges, opt_weights)
    red_edges, red_weights = remove_unnec_malls(compl_edges, compl_weights, size_houses)

    lr, er, lr_len, er_len = divide_lr_er(red_edges, red_weights, size_houses, alpha)
    
    return lr, er, lr_len, er_len

def obtain_Delaunay(houses_and_malls, plot=False):
    
    delaunay = Delaunay(houses_and_malls, qhull_options='Qc')
    
    if plot:
        plt.triplot(houses_and_malls[:,0], houses_and_malls[:,1], delaunay.simplices)
        plt.plot(houses_and_malls[:,0], houses_and_malls[:,1], 'o')
        plt.show()
    
    triangles = delaunay.simplices
    edges = np.concatenate((triangles[:,0:2], triangles[:,1:3], triangles[:,[0,2]]), axis = 0)
    ord_edges = np.sort(edges, axis=1)
    unique_edges = np.unique(ord_edges, axis=0)
    return unique_edges

def get_weigths_edges(houses_and_malls, edges, alpha, size_houses):
    
    len_edges = np.sqrt((houses_and_malls[edges[:,0],0]-
                         houses_and_malls[edges[:,1],0])**2+
                        (houses_and_malls[edges[:,0],1]-
                         houses_and_malls[edges[:,1],1])**2)
    
    local_road = (edges<size_houses).any(axis = 1)
    weights = np.zeros(np.shape(len_edges))
    weights[local_road] = len_edges[local_road]*alpha
    weights[~local_road] = len_edges[~local_road]*(1-alpha)     
    
    return weights

def edges_to_matrix(tot_size, edges, weights):
    
    graph_w_weights = np.zeros((tot_size,tot_size))
    
    graph_w_weights[edges[:,0], edges[:,1]] = weights

    return graph_w_weights

def obtain_MST(graph_w_weights):
    
    matrix = csr_matrix(graph_w_weights)
    mst = minimum_spanning_tree(matrix)
    
    opt_edges = np.array([[i, j] for i, j in zip(*mst.nonzero())])
    opt_weights = np.array([mst[i,j] for i, j in zip(*mst.nonzero())])
    
    return opt_edges, opt_weights

def add_city_center(houses_and_malls, city_center, size_houses, opt_edges, opt_weights):
    
    city_center_dis = distance.cdist([city_center], houses_and_malls)
    closest_points = city_center_dis.argsort()
    pos = np.argmax(closest_points>=size_houses)
    closest_mall = closest_points[0,pos]
        
    compl_edges = np.concatenate((opt_edges, [[closest_mall, np.shape(houses_and_malls)[0]]]), axis=0)    
    compl_weights = np.concatenate((opt_weights, [city_center_dis[0,pos]]), axis=0)
    
    return compl_edges, compl_weights

def remove_unnec_malls(compl_edges, compl_weights, size_houses):
    
    pos, counts = np.unique(compl_edges, return_counts=True)
    
    single_conn_malls = (pos[:-1]>=size_houses) & (counts[:-1]==1)
    
    red_edges = compl_edges
    red_weights = compl_weights
    for i in pos[:-1][single_conn_malls]:
        edge, _ = np.where(red_edges == i)
        red_edges = np.delete(red_edges, edge, axis = 0)
        red_weights = np.delete(red_weights, edge, axis = 0)
    
    return red_edges, red_weights

def divide_lr_er(red_edges, red_weights, size_houses, alpha):
    
    local_road = (red_edges<size_houses).any(axis = 1)
    
    lr = red_edges[local_road,:]
    er = red_edges[~local_road,:]
    
    lr_len = np.sum(red_weights[local_road])/alpha
    er_len = np.sum(red_weights[~local_road])/(1-alpha)
    
    return lr, er, lr_len, er_len


