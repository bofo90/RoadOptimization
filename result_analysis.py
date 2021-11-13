import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matl


def present_results(houses, malls, city_center, lr, er, lr_len, er_len, alpha, seed):
    """
    Creates a plot showing the houses, malls and city center and their 
    optimized road connection.
    """
    
    # Obtains all the points to plot them
    all_points = np.concatenate((houses, malls, [city_center]), axis = 0)

    # Creates figure
    plt.close('all')
    fig1 = plt.figure()
    ax1 = plt.subplot(111)
    ax1.set_axis_off()

    # Plots first the edges with colors depending if they are local or high-speed
    for e in lr:
        ax1.plot(all_points[e,0], all_points[e,1], c='#264653', zorder=0, linewidth=3)
    for e in er:
        ax1.plot(all_points[e,0], all_points[e,1], c='#2A9D8F', zorder=0, linewidth=3)
    
    # Plots the houses, malls and city center with different colors
    ax1.scatter(houses[:,0],houses[:,1], s=100, zorder=10, c='#E9C46A')
    ax1.scatter(malls[:,0], malls[:,1], s=200, zorder=10, c='#F4A261')
    ax1.scatter(city_center[0], city_center[1], s=150, zorder=10, c='#E76F51')
    
    # The title is the cost of the road network
    ax1.set_title(f'Cost: {lr_len*alpha+er_len*(1-alpha):.2f}')

    plt.tight_layout()
    
    # Saves figure with all parameters
    fig1.savefig(f'Results/Graph_{np.shape(all_points)[0]}points_{alpha}alpha_{seed}seed.png', transparent = True)
    
    
    return

def simple_plot(houses, malls, city_center, roads, title):
    """
    Creates a plot showing the houses, malls and city center and their 
    road connection. This graph is used to plot intermediate steps.
    """
    
    # Obtains all the points to plot them
    if np.shape(city_center)[0]>0:
        all_points = np.concatenate((houses, malls, [city_center]), axis = 0)
    else:
        all_points = np.concatenate((houses, malls), axis = 0)
        
    # Creates figure
    plt.close('all')
    fig1 = plt.figure()
    ax1 = plt.subplot(111)
    ax1.set_axis_off()

    # If given roads, plot them
    if np.shape(roads)[0]>0:
        size_houses = np.shape(houses)[0]
        local_roads_ind = (roads<size_houses).any(axis=1)
        
        # Obtain local and high-speed roads
        lr = roads[local_roads_ind,:]
        er = roads[~local_roads_ind,:]
    
        # Plots first the edges with colors depending if they are local or high-speed
        for e in lr:
            ax1.plot(all_points[e,0], all_points[e,1], c='#264653', zorder=0, linewidth=3)
        for e in er:
            ax1.plot(all_points[e,0], all_points[e,1], c='#2A9D8F', zorder=0, linewidth=3)
    
    # Plots the houses, malls and city center with different colors
    ax1.scatter(houses[:,0],houses[:,1], s=100, zorder=10, c='#E9C46A', label='houses')
    ax1.scatter(malls[:,0], malls[:,1], s=200, zorder=10, c='#F4A261', label='malls')
    if np.shape(city_center)[0]>0:
        ax1.scatter(city_center[0], city_center[1], s=150, zorder=10, c='#E76F51', label='city center')
    
    ax1.legend()
    
    plt.tight_layout()
    
    # Saves figure with all parameters
    fig1.savefig(f'Results/{title}.png')
    
    return
