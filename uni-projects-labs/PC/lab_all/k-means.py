import numpy as np
import functions as f

if __name__ == '__main__':
    # algorytm k-średnich dla danych z 2D z 15 centrami lub dla danych 9D z 2 centrami

    # opcja = int(input("Rysowanie punktów ze zbioru S1 - wybierz 1 \n\t\t\tze zbioru breast - wybierz 2\n"))
    opcja = 1
    if opcja == 1:
        sciezka = r's1.txt'
        wymiar = 2
        check = 10
    elif opcja == 2:
        sciezka = r'breast.txt'
        wymiar = 9
        check = 0.1
    else:
        print("błędny wybór")
        exit(-1)

    dataset = f.load_data(sciezka)
    s_x, s_y = dataset.shape
    cents, cent_colors = f.load_centers(wymiar)
    for i in range (20):
        grouped_points = f.cluster_membership(cents, dataset, s_x, wymiar)
        new_centers = f.drawing_graphs(grouped_points, cents, cent_colors, wymiar, 'K-means', iteration=i)
        if (np.abs(new_centers - cents) < check).all():
            break
        else:
            cents = new_centers
    # print(cents)
