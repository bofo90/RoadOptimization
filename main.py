from obtain_data import generate_points
from model_connections import connect_points
from result_analysis import present_results

alpha = 0.999
seed = 1

houses, malls, city_center = generate_points(size_houses=20, size_malls=20, seed=seed)

lr, er, lr_len, er_len = connect_points(houses, malls, city_center, alpha)

present_results(houses, malls, city_center, lr, er, lr_len, er_len, alpha, seed)

# O(n log n) time and O(n) space
