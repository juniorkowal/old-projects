import numpy as np
from sklearn_som.som import SOM
import functions as fun


if __name__ == '__main__':
    # algorytm SOM dla danych z 2D z 15 centrami lub dla danych 9D z 2 centrami
    # wybór opcji
    opcja = 1
    if opcja == 1:
        sciezka = r's1.txt'
        wymiar = 2
        check = 10
        l_centers = 15
    elif opcja == 2:
        sciezka = r'breast.txt'
        wymiar = 9
        check = 0.1
        l_centers = 2
    else:
        print("błędny wybór")
        exit(-1)

    # załadowanie danych, centrów i utworzenie np.array
    # w której są współrzędne oraz przynależność do klastra
    dataset = fun.load_data(sciezka)
    s_x, s_y = dataset.shape
    cents, cent_colors = fun.load_centers(wymiar)
    grouped_points = fun.cluster_membership(cents, dataset, s_x, wymiar)
    to_file = np.transpose(grouped_points)
    path_new = "./klustry.txt"
    with open(path_new, "w", encoding='utf-8') as file:
        for i, grpts in enumerate(to_file):
            file.write(str(grpts[0]) + '\t')
            file.write(str(grpts[1]) + '\t')
            file.write(str(grpts[2])+ '\n')
    # dostosowanie doanych na wejście sieci SOM
    data_to_SOM = np.transpose(grouped_points[:wymiar])
    # Build a 15x1 SOM (15 clusters) (opcja == 1)
    som = SOM(m=l_centers, n=1, dim=wymiar, random_state=1234)
    # Fit it to the data
    som.fit(data_to_SOM)
    # Assign each datapoint to its predicted cluster
    predictions = som.predict(data_to_SOM)

    # tablica wynikowa przesyłana do funkcji rysowania wykresów
    after_SOM = np.zeros((wymiar + 1, s_x), dtype=int)
    after_SOM[:wymiar] = grouped_points[:wymiar]
    after_SOM[wymiar] = predictions
    fun.drawing_graphs(after_SOM, cents, cent_colors, wymiar, "SOM")


