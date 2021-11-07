import numpy as np


def generate_points(size_houses, size_malls, seed=0):
    """
    From a size_area of 10x10, it creates random houses, malls and a city 
    center from a uniform disribution in the area. 
    
    Parameters
    ----------
    size_houses : int, >1
        Defines the number of houses to create.
    size_malls : int, >1
        Defines the number of mall to create.
    seed : int
        Seed of the random generrator. The default is 0.

    Returns
    -------
    houses : array of coordinates (floats)
        Positions of the houses in 2D plane.
    malls : array of coordinates (floats)
        Positions of the malls in 2D plane.
    city_center : coordinates (float)
        Position of the city center.

    """
    
    if (size_houses+size_malls < 4):
        raise ValueError('The number of points should be bigger than 3.')
    if size_malls<1:
        raise ValueError('There should be at least one mall.')
    
    np.random.seed(seed)
    
    size_area = 10
    
    houses = np.random.random((size_houses,2))*size_area
    malls = np.random.random((size_malls,2))*size_area
    
    city_center = np.random.random(2)*size_area
    
    return houses, malls, city_center