from obtain_data import generate_points
from model_connections import connect_points
import result_analysis as resan

"""
This program receives the locations of houses, malls and one city center and 
builds a network of roads that optimizes the cost connects all the houses. 
There are two types of roads, local and high-speed, and each one has a 
different cost, depending on the value of alpha. 

The program first creates a random distribution of houses, malls and city 
center (generate_points). Then it creates a graph where the connections 
between the points are optimized depending on the cost (connect_points). 
Finally it send the results to a function that plots the graph 
(present_results).

alpha = is the parameter controling the cost of the road. It's range is 
        between 0 and 1 but not uincluding 0 and 1. 
seed = seed of the random generator of the points.
size_houses = amount of houses to create.
size_malls = amount of malls to create.

houses, malls and city_center = coordinates in 2D of all the houses, malls and
                                city center, respectively.
                                
lr = array showing the local roads where for every road, the first number is 
     the starting point and the second the ending point of the road.
er = array showing the high-speed (express) roads. The concept is the same as
     in lr.
lr_len = total length of the local roads.
er_len = total length of the high-speed roads.

the cost is calculated following the equation:
    cost = alpha*lr_len + (1-alpha)*er_len
"""


alpha = 0.9
seed = 0
size_houses = 15
size_malls = 10


houses, malls, city_center = generate_points(size_houses, size_malls, seed)
resan.simple_plot(houses, malls, city_center, [], 'Town_Layout')
lr, er, lr_len, er_len = connect_points(houses, malls, city_center, alpha)
resan.present_results(houses, malls, city_center, lr, er, lr_len, er_len, alpha, seed)

# O(n log n) time and O(n) space