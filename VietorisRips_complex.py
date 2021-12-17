import plotly.graph_objects as go


def get_distance_matrix(point_cloud, n):
    distance_matrix = []

    for i in range(n):
        lst = []
        for j in range(n):
            d = ((point_cloud[i][0] - point_cloud[j][0]) ** 2 + (point_cloud[i][1] - point_cloud[j][1]) ** 2) ** (1 / 2)
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


def construction_simplicial_complex(point_cloud, distance_matrix, filtering, r):
    n = len(point_cloud)
    k = 1
    edges = []
    for i in range(n - 1):
        for j in range(k, n):
            if distance_matrix[i][j] <= r and [i, j] not in filtering[0]:
                filtering[0].append([i, j])
                filtering[1].append(r)
        k += 1

    for lst in filtering[0]:
        if len(lst) == 2:
            edges.append(lst)

    matrix = get_adjacency_matrix(edges, n)
    h = len(matrix)
    for a in range(0, h):
        for b in range(a + 1, h):
            if not matrix[a][b]:
                continue
            for c in range(b + 1, h):
                if matrix[b][c] and matrix[a][c] and [a, b, c] not in filtering[0]:
                    filtering[0].append([a, b, c])
                    filtering[1].append(r)

    return filtering


def visualization_complex(filtered_complex, point_array, t):
    x0, y0, x1, y1, x2, y2 = [], [], [], [], [], []
    for simpl in filtered_complex[0]:
        if len(simpl) == 1:
            point = point_array[simpl[0]]
            x0.append(point[0])
            y0.append(point[1])
        elif len(simpl) == 2:
            point1 = point_array[simpl[0]]
            point2 = point_array[simpl[1]]
            x1.append(point1[0])
            x1.append(point2[0])
            y1.append(point1[1])
            y1.append(point2[1])
            x1.append(0)
            y1.append(None)
        elif len(simpl) == 3:
            point1 = point_array[simpl[0]]
            point2 = point_array[simpl[1]]
            point3 = point_array[simpl[2]]
            x2.append(point1[0])
            x2.append(point2[0])
            x2.append(point3[0])
            x2.append(point1[0])

            y2.append(point1[1])
            y2.append(point2[1])
            y2.append(point3[1])
            y2.append(point1[1])

            x2.append(0)
            y2.append(None)

    # Визуализация

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, name='1-simplex'))
    fig.add_trace(go.Scatter(x=x0, y=y0, mode='markers', name='0-simplex'))
    fig.add_trace(go.Scatter(x=x2, y=y2,
                             fill='toself', fillcolor='#483D8B', name='2-simplex'))
    fig.update_layout(title=f"r = {t}")
    fig.show()
