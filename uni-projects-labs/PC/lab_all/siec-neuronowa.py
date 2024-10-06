import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
import functions as f

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

    # podział danych na współrzędne pkt i przynależnosci do klastrów
    data_in = np.transpose(grouped_points[:wymiar])
    data_out = grouped_points[wymiar]

    # podział na zbiory testowy (20%) i do trenowania(80%)
    testowy = 0.2
    d_in_train, d_in_test, d_out_train, d_out_test = train_test_split(data_in,data_out, test_size=testowy, random_state=0)
    # ???


    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(d_in_train)
    # struktura sieci (jest to sieć CNN bo ma warstwy Dense)
    model = tf.keras.Sequential(
        [
            normalizer,
            tf.keras.layers.Input(shape=wymiar),
            tf.keras.layers.Dense(5),
            tf.keras.layers.Dense(10),
            tf.keras.layers.Dense(l_centers, activation='softmax')   # tu na koniec musi byc softmax (bo jest skończony),
                                                                    # a nie relu bo relu nieskończone
        ]
    )
    # wypisanie jak wygląda model
    model.summary()
    model.compile(
        # loss - na co ma zwracać uwagę sieć
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer="adam", metrics=["accuracy"])

    # uczenie się modelu, zbiór walidacyjny to 20% treningowego
    model.fit(d_in_train, d_out_train, batch_size=32, epochs=30, verbose=1, validation_split=0.2)

    # zapis do modelu
    model.save(f'model{wymiar}D')
    # odczyt (można pominąć zapis i odczyt, ale jakby ktoś chciał to tak działa)
    model1 = tf.keras.models.load_model('model'+str(wymiar)+'D')

    # predykcja na danych pozostawionych wcześniej do testu
    pred = model1.predict(d_in_test)
    # w pred otrzymujemy dla każdego punktu wagi dla każdego neuronu z ostatniej warstwy
    # więc wybieramy dla którego neuronu waga była największa
    predictions = np.array([x.argmax() for x in pred])

    # rysowanie wykresu dla danych testowych
    # w funkcji poniżej dla opcji 1 => int(testowy*s_x)
    # dla opcji 2 => int(testowy*s_x)+1
    after_CNN = np.zeros((wymiar+1,int(testowy*s_x+opcja/2)), dtype=int)
    after_CNN[:wymiar] = np.transpose(d_in_test)
    after_CNN[wymiar] = predictions
    f.drawing_graphs(after_CNN,cents, cent_colors, wymiar, "Sieć neuronowa")