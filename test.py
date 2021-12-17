import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import TDA.VietorisRips_complex as vr
import TDA.Witness_complex as wc
from math import pi, cos, sin
import random

np.random.seed(7)
random.seed(7)


# Произвольное облако из 20 точек
# point_array = np.array([[5, 7], [4, 4], [8, 8], [8, 9], [9, 8],
#                         [7, 5], [3, 6], [1, 8], [7, 4], [6, 9],
#                         [5, 1], [1, 1], [8, 6], [12, 6], [2, 10],
#                         [10, 4], [2, 4], [0, 5], [10, 0], [12, 3]])


# "Окружность"
# point_array = np.array([[1, 4], [2, 2], [2, 6], [4, 1], [4, 7],
#                         [6, 2], [6, 6], [7, 4], [1.5, 3], [1.5, 5],
#                         [3, 1.5], [3, 6.5], [5, 1.5], [5, 6.5], [6.5, 3],
#                         [6.5, 5]])

# Облако из 4 точек
# point_array = np.array([[1, 1], [2, 4], [4, 1], [5, 4]])


# point_data = pd.DataFrame(point_array, columns=['x', 'y'])
#
# px.scatter(point_data, x="x", y="y").show()

# Первоначальная фильтрация(r=0), состоящая из 0-мерных симплексов
# n = len(point_array)
# detailed_filtering = [[], []]
# for i in range(n):
#     lst = [i]
#     detailed_filtering[0].append(lst)
#     detailed_filtering[1].append(0)
#
#
# distance_matrix = vr.get_distance_matrix(point_array, n)


# Максимальное значение радиуса(конец фильтрации) задается как
# максимальное растояние между точками облака
# list_max = []
# for i in distance_matrix:
#     list_max.append(max(i))
# c = math.ceil(max(list_max))

# c = 4 # Максимальное значение радиуса(конец фильтрации) в виде параметра
# h = 0.5 #Шаг
# r = 0 + h #Первоначальный радиус

# Фильтрация в цикле, нет визуализации
# while r <= c:
#     vr.construction_simplicial_complex(point_array, distance_matrix, detailed_filtering, r)
#     r += h
# print(detailed_filtering[0], '\n', detailed_filtering[1])


# Поэтапная фильтарация (радиус задается вручную), имеется визуализация для каждого этапа
# vr.construction_simplicial_complex(point_array, distance_matrix, detailed_filtering, 2)
# # vr.visualization_complex(detailed_filtering, point_array, 0)
# vr.construction_simplicial_complex(point_array, distance_matrix, detailed_filtering, 3)
# # vr.visualization_complex(detailed_filtering, point_array, 3)
# vr.construction_simplicial_complex(point_array, distance_matrix, detailed_filtering, 3.5)
# # vr.visualization_complex(detailed_filtering, point_array, 3.5)
# vr.construction_simplicial_complex(point_array, distance_matrix, detailed_filtering, 4)
# vr.visualization_complex(detailed_filtering, point_array, 4)
# print(detailed_filtering[0], '\n', detailed_filtering[1])


# Облако точек, расположенных около окружности (задаются координаты центра, радиус и шум)
def circle_points(h, k, r, noise):
    noise_x = random.uniform(-noise, noise)
    noise_y = random.uniform(-noise, noise)
    theta = random.random() * 2 * pi
    return [(h + cos(theta) * r) + noise_x, (k + sin(theta) * r) + noise_y]


# Облако из 600 точек, расположенных около 4 окружностей
# xy = [circle_points(1,2,3, 0.3) for _ in range(250)]
# xy.extend([circle_points(5,2,1, 0.3) for _ in range(70)])
# xy.extend([circle_points(4.5,-1,2, 0.5) for _ in range(180)])
# xy.extend([circle_points(-2,-2,2.5, 0.4) for _ in range(100)])


# Произвольное облако точек
# xy = [[1, 6], [1, 8], [2, 3], [2, 5], [3, 9], [4, 1], [4, 3], [4, 11], [6, 11],
#       [7, 0], [9, 1], [9, 9], [9, 11], [10, 3], [11, 4], [11, 6], [11, 8], [6, 2], [2, 9], [12, 7],
#       [5, 7], [4, 4], [8, 8], [8, 9], [9, 8], [7, 5], [3, 6], [1, 8], [7, 4], [6, 9],
#       [5, 1], [1, 1], [8, 6], [12, 6], [2, 10], [10, 4], [2, 4], [0, 5], [10, 0], [12, 3]]


xy = [circle_points(0, 0, 3.5, 0.8) for _ in range(400)]
xy.extend([circle_points(5, 0, 5, 0.8) for _ in range(500)])
xy.extend([circle_points(6.5, 0, 0.7, 0.7) for _ in range(50)])
# xy.extend([circle_points(3,0, 9, 0.6) for _ in range(1050)])


# point_data1 = pd.DataFrame(xy, columns=['x', 'y'])
# px.scatter(point_data1, x="x", y="y").show()


share = 10  # Во сколько раз уменьшить выборку

# 1-мерный остов, ориентиры выбираются случайно
# landmarks = wc.get_landmarks_random(xy, share)
# matrix_d = wc.get_distance_matrix(xy, landmarks)
# edges = wc.find_edges_skeleton(matrix_d, landmarks)
# wc.visualization_skeleton(xy, landmarks, edges) #Визуализация


# 1-мерный остов, ориентиры выбираются с помощью критерия maxmin
# landmarks = wc.get_landmarks_maxmin(xy, share)
# matrix_d = wc.get_distance_matrix(xy, landmarks)
# edges = wc.find_edges_skeleton(matrix_d, landmarks)
# wc.visualization_skeleton(xy, landmarks, edges) #Визуализация

# Добавляем в комплекс треугольники и визуализируем то, что получилось
# n = len(landmarks)
# m = wc.get_adjacency_matrix(edges, n)
# triangles = wc.get_triangles(m)
# wc.visualization_2dim_skeleton(xy, landmarks, edges, triangles) #Визуализация


landmarks = wc.get_landmarks_maxmin(xy, share)
matrix_d = wc.get_distance_matrix(xy, landmarks)
edges = wc.find_edges_skeleton(matrix_d, landmarks)
# wc.visualization_skeleton(xy, landmarks, edges)

lst_mv = wc.get_values_mv(2, matrix_d)

# Первоначальная фильтрация(t=0), состоящая из 0-мерных симплексов
n = len(matrix_d[0])
detailed_filtering = [[], []]
for i in range(n):
    lst = [i]
    detailed_filtering[0].append(lst)
    detailed_filtering[1].append(0)

wc.filtering_witnesses(matrix_d, detailed_filtering, 2, 0.4)
wc.visualization_filtering(xy, landmarks, detailed_filtering, 0.4)
