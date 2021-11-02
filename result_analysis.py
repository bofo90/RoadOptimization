import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matl

def cm2inch(value):
    return value/2.54

def NiceGraph2D(axes, nameX, nameY, mincoord = [np.NaN, np.NaN], maxcoord = [np.NaN, np.NaN], divisions = [np.NaN, np.NaN],buffer = [0.0, 0.0, 0.0]):
    
    gray = '0.2'
    matl.rcParams.update({'font.size': 12})

    if ~np.isnan(mincoord[0]) and ~np.isnan(maxcoord[0]):
        axes.set_xlim([mincoord[0]-buffer[0], maxcoord[0]+buffer[0]])
        if isinstance(divisions[0], (list, tuple, np.ndarray)):
            if ~np.isnan(divisions[0]).any():
                axes.set_xticks(divisions[0])
        else:
            if ~np.isnan(divisions[0]):
                axes.set_xticks(np.linspace(mincoord[0],maxcoord[0],divisions[0]))
    axes.set_xlabel(nameX,labelpad=0, color = gray)
    
    if ~np.isnan(mincoord[1]) and ~np.isnan(maxcoord[1]):
        axes.set_ylim([mincoord[1]-buffer[1], maxcoord[1]+buffer[1]])
        if isinstance(divisions[1], (list, tuple, np.ndarray)):
            if ~np.isnan(divisions[1]).any():
                axes.set_yticks(divisions[1])
        else:
            if ~np.isnan(divisions[1]):
                axes.set_yticks(np.linspace(mincoord[1],maxcoord[1],divisions[1]))
    axes.set_ylabel(nameY,labelpad=0, color = gray)
   
    axes.xaxis.label.set_color(gray)
    axes.tick_params(axis='x', colors=gray, direction = 'in', width = 0.4)
    axes.yaxis.label.set_color(gray)
    axes.tick_params(axis='y', colors=gray, direction = 'in', width = 0.4)
    axes.tick_params(pad = 2)
    
    axes.tick_params(axis='y', which='minor', colors=gray, direction = 'in', width = 0.4)
    axes.tick_params(axis='x', which='minor', colors=gray, direction = 'in', width = 0.4)
    
    for axis in ['top','bottom','left','right']:
        axes.spines[axis].set_linewidth(0.4)
        axes.spines[axis].set_color(gray)
        
    return

def present_results(houses, malls, city_center, lr, er, lr_len, er_len, alpha, seed):
    
    all_points = np.concatenate((houses, malls, [city_center]), axis = 0)

    plt.close('all')
    fig1 = plt.figure()
    ax1 = plt.subplot(111)
    ax1.set_axis_off()

    for e in lr:
        ax1.plot(all_points[e,0], all_points[e,1], c='b', zorder=0)
    for e in er:
        ax1.plot(all_points[e,0], all_points[e,1], c='r', zorder=0)
    
    ax1.scatter(houses[:,0],houses[:,1], s=50, zorder=10)
    ax1.scatter(malls[:,0], malls[:,1], s=100, zorder=10)
    ax1.scatter(city_center[0], city_center[1], s=70, zorder=10)
    
    ax1.set_title(f'Cost: {lr_len*alpha+er_len*(1-alpha):.2f}')

    plt.tight_layout()
    
    fig1.savefig(f'Results/Graph_{np.shape(all_points)[0]}points_{alpha}alpha_{seed}seed.pdf', transparent = True)
    
    
    return
