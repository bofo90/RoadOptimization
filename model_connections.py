import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial import distance


def connect_points(houses, malls, city_center, alpha):
    """
    Creates the connections of the houses, malls and city_center following
    the cost of the roads. The connections are made in steps. First, I create
    a big array with all the houses and malls. These are considered points in
    a 2D space from which I can create a graph. The graph that I create is a
    Delaunay graph or triangulated graph, since all single connected graphs 
    are a sub-group from this graph. After obtaining the graph, I calculate 
    the weights of each connection and transform it to connection matrix. From
    this matrix, I obtain the minimum expanding tree that minimizes the edges
    according to their weight. Afterwards, I connect the city center to the
    closest mall and remove all the malls that are single connected to the 
    road network. Finally I obtain the total length of the local and high-
    speed roads.
    """
    
    # Creation of big array of houses and malls
    houses_and_malls = np.concatenate((houses,malls), axis=0)
    size_houses = np.shape(houses)[0]
    size_malls = np.shape(malls)[0]
    tot_size = size_houses + size_malls
    
    edges = obtain_Delaunay(houses_and_malls)
    weights = get_weights_edges(houses_and_malls, edges, alpha, size_houses)
    graph_w_weights = edges_to_matrix(tot_size, edges, weights)   
    opt_edges, opt_weights = obtain_MST(graph_w_weights)
    compl_edges, compl_weights = add_city_center(houses_and_malls, city_center, 
                                                 size_houses, opt_edges, opt_weights)
    red_edges, red_weights = remove_unnec_malls(compl_edges, compl_weights, size_houses)

    # Obtain the total length of the two types of roads
    lr, er, lr_len, er_len = divide_lr_er(red_edges, red_weights, size_houses, alpha)
    
    return lr, er, lr_len, er_len

def obtain_Delaunay(houses_and_malls, plot=False):
    """
    Creates the Delaunay graph given the coordinates of the houses and malls.
    It checks if the graph is fully connected. Then obtains all the 
    triangulations of the graphs and creates an array of edges. It returns
    all the edges of the graph.
    """
    
    delaunay = Delaunay(houses_and_malls, qhull_options='Qc')
    
    # Check if there are points not connected to the graph due to coplanarity issues
    if delaunay.coplanar.size != 0:
        raise UserWarning('The Delaunay graph gave non-connected points. Please check coplanarity of points.')
    
    if plot:
        plt.triplot(houses_and_malls[:,0], houses_and_malls[:,1], delaunay.simplices)
        plt.plot(houses_and_malls[:,0], houses_and_malls[:,1], 'o')
        plt.show()
    
    # Create array of edges instead of triangluations of the graph
    triangles = delaunay.simplices
    edges = np.concatenate((triangles[:,0:2], triangles[:,1:3], triangles[:,[0,2]]), axis = 0)
    ord_edges = np.sort(edges, axis=1)
    unique_edges = np.unique(ord_edges, axis=0)
    return unique_edges

def get_weights_edges(houses_and_malls, edges, alpha, size_houses):
    """
    Takes all the edges of the graphs and calculates their length in 2D space.
    After it calculates the cost of each edges in order to obtain the weight.
    Returns the weight of all edges
    """
    
    # Calculate the distance between points
    len_edges = np.sqrt((houses_and_malls[edges[:,0],0]-
                         houses_and_malls[edges[:,1],0])**2+
                        (houses_and_malls[edges[:,0],1]-
                         houses_and_malls[edges[:,1],1])**2)
    
    # Obtain cost of the roads (edges) as weights
    local_road = (edges<size_houses).any(axis = 1)
    weights = np.zeros(np.shape(len_edges))
    weights[local_road] = len_edges[local_road]*alpha
    weights[~local_road] = len_edges[~local_road]*(1-alpha)     
    
    return weights

def edges_to_matrix(tot_size, edges, weights):
    """
    Transforms from the edge notation, each row is an edge defined by the 
    begining and end point, to a connectivity matrix, where each row  and 
    column represents a point and if the value is non-zero, it means it has
    an edge with the described weight.
    """
    
    graph_w_weights = np.zeros((tot_size,tot_size))
    
    graph_w_weights[edges[:,0], edges[:,1]] = weights

    return graph_w_weights

def obtain_MST(graph_w_weights):
    """
    From the connectivity matrix, I obtain a minimum spanning tree. This is a
    fully connected graph that minimizes the total sum of the weights of their
    edges. It returns an array of edges and their corresponding weights.
    """
    # Obtaining the minimum spanning tree (mst)
    matrix = csr_matrix(graph_w_weights)
    mst = minimum_spanning_tree(matrix)
    
    # Creating array of edges from the mst
    opt_edges = np.array([[i, j] for i, j in zip(*mst.nonzero())])
    opt_weights = np.array([mst[i,j] for i, j in zip(*mst.nonzero())])
    
    return opt_edges, opt_weights

def add_city_center(houses_and_malls, city_center, size_houses, opt_edges, opt_weights):
    """
    It calculates the distance from the city center to all points and sort 
    these distances to obtain the closest connected mall. Then adds and edge
    from this mall to the city center. Returns the complete edge list.
    """
    
    # Calculate distances from city center to all points
    city_center_dis = distance.cdist([city_center], houses_and_malls)
    
    # Order points according to distance
    closest_points = city_center_dis.argsort()
    
    # Obtain the closes mall
    pos = np.argmax(closest_points>=size_houses)
    closest_mall = closest_points[0,pos]
        
    # Add edge to city center
    compl_edges = np.concatenate((opt_edges, [[closest_mall, np.shape(houses_and_malls)[0]]]), axis=0)    
    compl_weights = np.concatenate((opt_weights, [city_center_dis[0,pos]]), axis=0)
    
    return compl_edges, compl_weights

def remove_unnec_malls(compl_edges, compl_weights, size_houses):
    """
    Check how many connections does each point has, and removes all the malls
    with only one connection. It repeats this until there is no mall to remove.
    Returns a reduced edge list.
    """
    
    # Obtain points and the amount of connections it has
    pos, counts = np.unique(compl_edges, return_counts=True)
    single_conn_malls = (pos[:-1]>=size_houses) & (counts[:-1]==1)
    
    red_edges = compl_edges
    red_weights = compl_weights
    # Repeats as long as there are malls with only one connection
    while single_conn_malls.any():
        # Loops through all malls with one connection to remove that edge
        for i in pos[:-1][single_conn_malls]:
            edge, _ = np.where(red_edges == i)
            red_edges = np.delete(red_edges, edge, axis = 0)
            red_weights = np.delete(red_weights, edge, axis = 0)
        
        pos, counts = np.unique(red_edges, return_counts=True)
        single_conn_malls = (pos[:-1]>=size_houses) & (counts[:-1]==1)
        
    
    return red_edges, red_weights

def divide_lr_er(red_edges, red_weights, size_houses, alpha):
    """
    Obtains the total local and high-speed road length from their cost.
    """
    
    # If and edge connects to a house is local, if not is high-speed
    local_road = (red_edges<size_houses).any(axis = 1)
    
    lr = red_edges[local_road,:]
    er = red_edges[~local_road,:]
    
    lr_len = np.sum(red_weights[local_road])/alpha
    er_len = np.sum(red_weights[~local_road])/(1-alpha)
    
    return lr, er, lr_len, er_len


