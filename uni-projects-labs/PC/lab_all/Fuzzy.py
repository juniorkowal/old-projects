import numpy as np
import functions as f
from fcmeans import FCM
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # siec dla danych z 2D z 15 centrami lub dla danych 9D z 2 centrami
    # wybór opcji
    opcja = 2
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
    dataset = f.load_data(sciezka)
    s_x, s_y = dataset.shape
    cents, cent_colors = f.load_centers(wymiar)
    grouped_points = f.cluster_membership(cents, dataset, s_x, wymiar)

    # dostosowanie doanych na wejście fuzzy c-means
    data_to_fuzzy = np.transpose(grouped_points[:wymiar])
    fcm = FCM(n_clusters=l_centers)
    fcm.fit(data_to_fuzzy)

    # outputs
    cents = fcm.centers
    predictions = fcm.predict(data_to_fuzzy)

    # tablica wynikowa przesyłana do funkcji rysowania wykresów
    after_fuzzy = np.zeros((wymiar + 1, s_x), dtype=int)
    after_fuzzy[:wymiar] = grouped_points[:wymiar]
    after_fuzzy[wymiar] = predictions
    f.drawing_graphs(after_fuzzy, cents, cent_colors, wymiar, "Fuzzy")

