from obtain_data import generate_points
from model_connections import connect_points
from result_analysis import present_results

alpha = 0.3

N, M, CC = generate_points()

lr, er, lr_len, er_len, graph = connect_points(N, M, CC, alpha)

present_results(graph)


