import numpy as np
import plotly.graph_objects as go
import random


def get_landmarks_maxmin(point_cloud, share):
    value = int(len(point_cloud) / share)
    landmarks = []
    landmarks.append(random.choice(point_cloud))
    matrix = []
    for i in point_cloud:
        d = [((i[0] - landmarks[0][0]) ** 2 + (i[1] - landmarks[0][1]) ** 2) ** (1 / 2)]
        matrix.append(d)
    while len(landmarks) < value:
        min_values = []
        for i in matrix:
            min_values.append(min(i))
        t = min_values.index(max(min_values))
        landmarks.append(point_cloud[t])
        for i in range(len(point_cloud)):
            d = ((point_cloud[i][0] - point_cloud[t][0]) ** 2 +
                 (point_cloud[i][1] - point_cloud[t][1]) ** 2) ** (1 / 2)
            matrix[i].append(d)
    return landmarks


def get_landmarks_random(point_cloud, share):
    value = int(len(point_cloud) / share)
    lst = [i for i in range(0, len(point_cloud))]
    landmarks_ind = np.random.choice(lst, value, replace=False)
    landmarks = []
    for i in landmarks_ind:
        landmarks.append(point_cloud[i])
    return landmarks


def get_distance_matrix(witnesses, landmarks):
    distance_matrix = []
    for i in witnesses:
        lst = []
        for j in landmarks:
            d = ((i[0] - j[0]) ** 2 + (i[1] - j[1]) ** 2) ** (1 / 2)
            lst.append(d)
        distance_matrix.append(lst)
    return distance_matrix


def get_adjacency_matrix(e, n):
    v = [i for i in range(n)]
    m = []
    for i in range(len(v)):
        lst = []
        for j in range(len(v)):
            if i == j:
                lst.append(0)
            elif [v[i], v[j]] in e or [v[j], v[i]] in e:
                lst.append(1)
            else:
                lst.append(0)
        m.append(lst)
    return m


def find_edges_skeleton(distance_matrix, landmarks):
    k = len(landmarks)
    edges = []
    for i in distance_matrix:
        if i[0] > i[1]:
            mn1 = 1
            mn2 = 0
        else:
            mn1 = 0
            mn2 = 1
        for t in range(2, k):
            if i[t] < i[mn1]:
                mn2 = mn1
                mn1 = t
            else:
                if i[t] < i[mn2]:
                    mn2 = t
        if [mn1, mn2] not in edges and [mn2, mn1] not in edges:
            edges.append([mn1, mn2])
    return edges


def get_triangles(matrix):
    triangles = []
    h = len(matrix)
    for a in range(0, h):
        for b in range(a + 1, h):
            if not matrix[a][b]:
                continue
            for c in range(b + 1, h):
                if matrix[b][c] and matrix[a][c] and [a, b, c] not in triangles:
                    triangles.append([a, b, c])
    return triangles


def visualization_skeleton(witnesses, landmarks, edges):
    x1, y1 = [], []
    for i in witnesses:
        x1.append(i[0])
        y1.append(i[1])
    x2, y2 = [], []
    for i in landmarks:
        x2.append(i[0])
        y2.append(i[1])
    x3, y3 = [], []
    for i in edges:
        x3.append(landmarks[i[0]][0])
        x3.append(landmarks[i[1]][0])
        y3.append(landmarks[i[0]][1])
        y3.append(landmarks[i[1]][1])
        x3.append(0)
        y3.append(None)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers', name='witness'))
    fig.add_trace(go.Scatter(x=x2, y=y2, mode='markers', name='landmark'))

    fig.add_trace(go.Scatter(x=x3, y=y3, name='1-simplex'))
    fig.update_layout(title="one - dimensional skeleton")
    fig.show()


def visualization_2dim_skeleton(witnesses, landmarks, edges, triangles):
    x1, y1 = [], []
    for i in witnesses:
        x1.append(i[0])
        y1.append(i[1])
    x2, y2 = [], []
    for i in landmarks:
        x2.append(i[0])
        y2.append(i[1])
    x3, y3 = [], []
    for i in edges:
        x3.append(landmarks[i[0]][0])
        x3.append(landmarks[i[1]][0])
        y3.append(landmarks[i[0]][1])
        y3.append(landmarks[i[1]][1])
        x3.append(0)
        y3.append(None)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers', name='witness'))
    fig.add_trace(go.Scatter(x=x2, y=y2, mode='markers', name='landmark'))
    fig.add_trace(go.Scatter(x=x3, y=y3, name='1-simplex'))

    for i in triangles:
        x, y = [], []
        x.append(landmarks[i[0]][0])
        x.append(landmarks[i[1]][0])
        x.append(landmarks[i[2]][0])
        x.append(landmarks[i[0]][0])
        y.append(landmarks[i[0]][1])
        y.append(landmarks[i[1]][1])
        y.append(landmarks[i[2]][1])
        y.append(landmarks[i[0]][1])
        x.append(0)
        y.append(None)
        fig.add_trace(go.Scatter(x=x, y=y, fill='toself', fillcolor='#483D8B', name='2-simplex'))

    fig.show()


# Фильтрация

def search_second_minimum(lst):
    k = len(lst)
    if lst[0] > lst[1]:
        mn1 = 1
        mn2 = 0
    else:
        mn1 = 0
        mn2 = 1
    for t in range(2, k):
        if lst[t] < lst[mn1]:
            mn2 = mn1
            mn1 = t
        else:
            if lst[t] < lst[mn2]:
                mn2 = t
    return (lst[mn2])


def get_values_mv(number, matrix):
    k = len(matrix[0])
    lst_mv = []
    if number == 0:
        lst_mv = [0 for _ in range(k)]
    elif number == 1:
        for i in matrix:
            lst_mv.append(min(i))
    elif number == 2:
        for i in matrix:
            p = search_second_minimum(i)
            lst_mv.append(p)
    elif number == 3:
        for i in matrix:
            l = i.copy()
            l.sort()
            mn1 = l[0]
            for t in range(1, len(l) - 2):
                if mn1 < l[t] < l[t + 1]:
                    lst_mv.append(l[t + 1])
                    break
    return lst_mv


def filtering_witnesses(distance_matrix, detailed_filtering, mv, t):
    e = []
    lst_mv = get_values_mv(mv, distance_matrix)
    for q in range(len(distance_matrix)):
        for i in range(len(distance_matrix[q]) - 1):
            for j in range(1, len(distance_matrix[q])):
                if max(distance_matrix[q][i], distance_matrix[q][j]) <= lst_mv[q] + t:
                    if [i, j] not in detailed_filtering[0] and [j, i] not in detailed_filtering[0] and i != j:
                        detailed_filtering[0].append([i, j])
                        detailed_filtering[1].append(t)
                        e.append([i, j])
    adj_matrix = get_adjacency_matrix(e, len(distance_matrix[0]))
    triangles = get_triangles(adj_matrix)
    for tr in triangles:
        detailed_filtering[0].append(tr)
        detailed_filtering[1].append(t)
    return detailed_filtering


def visualization_filtering(point_array, landmarks, filtered_complex, t):
    x, y, x0, y0, x1, y1, x2, y2 = [], [], [], [], [], [], [], []
    for i in point_array:
        x.append(i[0])
        y.append(i[1])
    tr = []
    for simpl in filtered_complex[0]:
        if len(simpl) == 1:
            point = landmarks[simpl[0]]
            x0.append(point[0])
            y0.append(point[1])
        elif len(simpl) == 2:
            point1 = landmarks[simpl[0]]
            point2 = landmarks[simpl[1]]
            x1.append(point1[0])
            x1.append(point2[0])
            y1.append(point1[1])
            y1.append(point2[1])
            x1.append(0)
            y1.append(None)
        elif len(simpl) == 3:
            tr.append(simpl)

    # Визуализация
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='0-simplex'))
    fig.add_trace(go.Scatter(x=x0, y=y0, mode='markers', name='0-simplex'))
    fig.add_trace(go.Scatter(x=x1, y=y1, name='1-simplex'))

    for i in tr:
        x, y = [], []
        x.append(landmarks[i[0]][0])
        x.append(landmarks[i[1]][0])
        x.append(landmarks[i[2]][0])
        x.append(landmarks[i[0]][0])
        y.append(landmarks[i[0]][1])
        y.append(landmarks[i[1]][1])
        y.append(landmarks[i[2]][1])
        y.append(landmarks[i[0]][1])
        x.append(0)
        y.append(None)
        fig.add_trace(go.Scatter(x=x, y=y, fill='toself', fillcolor='#483D8B', name='2-simplex'))
    fig.update_layout(title=f"t = {t}")
    fig.show()
