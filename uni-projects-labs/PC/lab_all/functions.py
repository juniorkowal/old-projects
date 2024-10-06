import math
import matplotlib.pyplot as plt
import numpy as np

def load_data(path):
    try:
        with open(path) as file:
            all_lines = file.readlines()
            lines = np.array([line.split() for line in all_lines], dtype=float)
        return lines
    except FileNotFoundError:
        print("Nie ma takiego pliku lub sciezki!")
        exit()


def load_centers(dim):
    # centra
    if dim == 2:
        # # prawdziwe
        # dla k-means powinno się ładować inne
        c1 = [604328, 574379]
        c2 = [801908, 318382]
        c3 = [416383, 786204] #750000
        c4 = [822771, 732034]
        c5 = [850993, 157873]
        c6 = [338586, 563537]
        c7 = [169274, 348574]
        c8 = [619259, 397671]
        c9 = [241071, 844424]
        c10 = [321801, 165319]
        c11 = [139493, 557352]
        c12 = [508785, 174800]
        c13 = [398934, 404142]
        c14 = [860858, 546059]
        c15 = [674365, 860464]
        c_colors = ['#a74992', '#aa99c5', '#EaE4ef', '#2d73b9', '#49bdef', '#00a9a4', '#00a54e', '#aed673', '#faf519',
                    '#f38044', '#5c3e90', '#f9c7c2', '#959595', '#000000', '#ff33cc']
        return np.array([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15]), np.array(c_colors)

    elif dim == 9:
        c1 = [5, 5, 5, 1, 2, 1, 3, 1, 1]
        c2 = [5, 10, 10, 10, 6, 10, 6, 5, 2]
        c_colors =['#f9c7c2', '#5c3e90']
        return np.array([c1, c2]), np.array(c_colors)


def distance(center, point):
    # odległość punktu do centrum
    return np.sqrt(np.sum((np.abs(center - point))**2))


def new_center(cluster_points):
    # wyliczanie środka ciężkości dla danego klastra
    points_array = np.transpose(cluster_points)
    return np.sum(points_array, axis=0)/points_array.shape[0]


def cluster_membership(center_points, data, size, dimensions):
    # wybranie do którego centrum jest najblizej
    dependencies = np.zeros((size, dimensions + 1), dtype=int)
    for el_id, element in enumerate(data):
        mini = math.inf
        id = 0
        # w tej pętli wybieramy dla którego centrum dla tego konkretnego elementu jest najbliżej
        for c_id, center in enumerate(center_points):
            dist = distance(center, element)
            if dist < mini:
                mini = dist
                id = c_id
        for i in range(dimensions):
            dependencies[el_id][i] = element[i]  # wypełnienie pustego dependencies aktualnym elementem
        dependencies[el_id][dimensions] = id  # i przypisanie elementu do centrum
    return np.transpose(dependencies)


def drawing_graphs(points,centrums, colors, dimension, subscription, iteration=0):
    # rysowanie wykresów i obliczanie nowych środków dla każdego klastra
    fig = plt.figure( dpi=200)
    fig.suptitle(subscription+f'\n i = {iteration}', fontsize=10)
    if dimension ==2:
        ax = fig.add_subplot()
        ax.set_xlabel('x', fontsize=10)
        ax.set_ylabel('y', fontsize=10)
        new_centums = np.zeros((15,dimension))
    elif dimension == 9:
        a1 = fig.add_subplot(131, projection='3d')
        a2 = fig.add_subplot(132, projection='3d')
        a3 = fig.add_subplot(133, projection='3d')
        new_centums = np.zeros((2, dimension))      # (how many centers, how many dimensions)
    current_group = np.zeros(dimension)
    for cen_id, cen in enumerate(centrums):
        current_group = np.array([(np.extract(points[dimension] == cen_id, points[a]).tolist()) for a, _ in enumerate(current_group)])
        if dimension == 2:
            ax.plot(current_group[0], current_group[1], '.', color=colors[cen_id])  # , label='Punkty pomiarowe')
            #ax.plot(cen[0], cen[1], 'ro')
        elif dimension == 9:
            a1.scatter(current_group[0], current_group[1], current_group[2],
                       color=colors[cen_id])  # , label='Punkty pomiarowe')
            # a1.scatter(cen[0], cen[1], cen[2], color='red')
            a2.scatter(current_group[3], current_group[4], current_group[5], color=colors[cen_id])
            # a2.scatter(cen[0], cen[1], cen[2], color='red')
            a3.scatter(current_group[6], current_group[7], current_group[8], color=colors[cen_id])
            # a3.scatter(cen[0], cen[1], cen[2], color='red')
        new_centums[cen_id] = new_center(current_group)
    plt.show()
    return new_centums
