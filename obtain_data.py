import numpy as np


def generate_points(size_houses, size_malls, seed=0):
    
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