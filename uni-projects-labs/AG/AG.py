import random
import numpy as np
from copy import copy
import matplotlib.pyplot as plt


class Specimen:
    def __init__(self, n: int = 5, res: int = 20):
        self.res = res
        self.n = n
        self.x1 = 0.
        self.x2 = 0.
        self.J = 0.0
        self.u_bin = np.random.randint(2, size=(n, res))     # initial random binary values
        self.u = np.zeros(n)
        self.bin2dec()                                       # turn binary representation to decimal values

    def bin2dec(self):
        """
        Method that converts binary to decimal
        :return: 
        """
        g1 = 0.                                             # lower bound for parameters
        g2 = 1.                                             # upper bound for parameters
        for i in range(self.n):  # convert u_bin to u
            # convert binary representation to decimal value
            u_bin_val = sum(b * 2**(self.res - 1 - j) for j, b in enumerate(self.u_bin[i]))
            # scale value from binary representation to the selected range
            self.u[i] = round(g1 + (u_bin_val * g2 / ((2**self.res) - 1)), 6)
        self.count_J()

    def count_J(self):
        """
        Method to count J value
        :return: 
        """
        self.x1 = 0.  # initial values
        self.x2 = 0.
        for i in range(1, self.n):
            # compute state model value for the drawn parameters u
            self.x1, self.x2 = self.x2, 2 * self.x2 - self.x1 + (1 / (self.n**2)) * self.u[i - 1]
        # compute J value
        self.J = self.x2 - (1 / (2 * self.n)) * sum(u**2 for u in self.u)

    def mutate(self, probability:int = 0.01):
        """
        Method that performs mutation by flipping (0 -> 1 and 1 -> 0)
        :probability: probabilty of mutation (default value 0.01) = 1%
        :return: 
        """
        if random.random() <= probability:
            k = random.randint(0, self.n - 1)
            k_id = random.randint(0, self.res - 1)
            self.u_bin[k][k_id] = 1 if self.u_bin[k][k_id] == 0 else 0
            self.bin2dec()


def crossbreed(population: list, pop_num: int):
    """
    Function that breeds speciments 
    
    :param population: list of specimens
    :param pop_num: number of specimens
    :return: 
    """
    ids=list(range(0, pop_num))                              # losowanie par
    random.shuffle(ids)
    pairs=[]
    while(ids):
        px=ids.pop()
        py=ids.pop()
        pair=(px, py)
        pairs.append(pair)
    p_k=np.random.rand(pop_num // 2)
    crossover_ids=np.where(p_k < 0.6)                       # wybranie par, dla których wylosowana liczba
                                                            # jest mniejsza od prawdopodobieństwa krzyżowania
                                                            # obrane prawdopodobieństwo krzyżowania = 60%
    for el in crossover_ids[0]:                             # dla każdej pary wybranej do krzyżowania
        selected_pair=pairs[int(el)]
        parent_1=copy(population[selected_pair[0]])
        parent_2=copy(population[selected_pair[1]])
        parent_1.u_bin=parent_1.u_bin.flatten()             # złożenie n wymiarowej tablicy parametrów w tab. jednowym.
        parent_2.u_bin=parent_2.u_bin.flatten()
        rand=random.randint(0,parent_1.u_bin.size-1)        # losowanie pozycji krzyżowania
        temp1=parent_1.u_bin[:rand]
        parent_1.u_bin[:rand]=parent_2.u_bin[:rand]
        parent_2.u_bin[:rand]=temp1
        parent_1.u_bin=parent_1.u_bin.reshape((parent_1.n,parent_1.res))
        parent_2.u_bin=parent_2.u_bin.reshape((parent_2.n,parent_2.res))
        population[selected_pair[0]]=copy(parent_1)
        population[selected_pair[0]].bin2dec()
        population[selected_pair[1]]=copy(parent_2)
        population[selected_pair[1]].bin2dec()


def selection(population: list, pop_num: int):
    """
    Function that performs selection: 'eliminates weak specimens'

    metoda proporcjonalna
    :param population: 
    :param pop_num: 
    :return: 
    """
    population.sort(key=lambda x: x.J)                  # sortowanie po wartości wskaźnika
    min_C = population[0].J
    J_sum=0
    f_przystosowania=np.ndarray(pop_num, dtype=float)  # przekształcenie na fun. przystosowania dla zad. maksymalizacji
    for i, osobnik in enumerate(population):
        f_przystosowania[i]=osobnik.J-min_C
        J_sum+=f_przystosowania[i]
    f_przystosowania_relative=f_przystosowania/J_sum    # obliczenie proporcji
    dystryb=np.cumsum(f_przystosowania_relative)        # obliczenie dystrybuanty
    list_of_ids=[]
    for i in range(population.__len__()):               # selection proporcjonalna
        rand=random.random()                            # liczba losowana z zakresu 0 do 1
        j=0
        while(rand > dystryb[j]):                       # gdy wylosowana liczba jest mniejsza od dystrybuanty
            j += 1                                      # następuje wyjście z pętli
        list_of_ids.append(j)                           # element o danym id zostanie dodany do nowej populacji
    new_population=[]
    for el in list_of_ids:
        new_population.append(population[el])
    return new_population


def j_mean_in_population(x_population):
    """
    Function that ...
    :param x_population:
    :return:
    """
    j_m = 0
    for el in x_population:
        j_m += el.J
    return (j_m/pop_num)


def u_mean_in_population(population: list, pop_num: int):
    """
    Function that ...
    :param population: list of specimens
    :param pop_num: number of specimens
    :return:
    """
    return_list = []
    np_pop = np.zeros(pop_num)
    for j in range(population[0].n):
        for i, el in enumerate(population):
            np_pop[i]=el.u[j]
        return_list.append(np.mean(np_pop))
    return return_list


def standard_deviation(population: list, pop_num: int, type: str = "J"):
    """
    Function that calculates standard deviation
    :param population: list of specimens
    :param pop_num: number of specimens
    :param type:
    :return:
    """
    return_list = []
    np_pop = np.zeros(pop_num)
    if type == "J":
        for i, el in enumerate(population):
            np_pop[i] = el.J
        return_list.append(np.std(np_pop))
    elif type == "u":
        for j in range(population[0].n):
            for i, el in enumerate(population):
                np_pop[i] = el.u[j]
            return_list.append(np.std(np_pop))
    return return_list


if __name__ == '__main__':
    # ====== POTRZEBNE STAŁE I ZMIENNE ===== #
    l_epok = 20000
    pop_num = 100
    l_param = 30

    x1_max, x2_max = [], []  # list of max x1 and max x2 values for every epoch

    j_avg, j_std, j_max = [], [], [] # list of J values for every epoch

    u_std = [[] for i in range(l_param)]
    u_avg = [[] for i in range(l_param)]


    # ====== TWORZENIE POCZĄTKOWEJ POPULACJI ===== #
    population = [Specimen(n=l_param) for i in range(pop_num)]


    # ====== ZADANIA WYKONYWANE W KAŻDYM POKOLENIU ===== #
    for i in range(l_epok):
        new_population = selection(population, pop_num)           # selection
        crossbreed(new_population, pop_num)                       # krzyżowanie

        [specimen.mutate() for specimen in new_population]       # mutacja
        
        population = copy(new_population)                        # reprodukcja

        # ====== ZAPISANIE WARTOŚCI POTRZEBNYCH DO NARYSOWANIA WYKRESÓW ===== #
        population.sort(key=lambda x: x.J)

        j_avg.append(j_mean_in_population(population))                  # obliczenie średniej J w danej populacji
        j_std.append(standard_deviation(population, pop_num,"J")[0])     # obliczenie odchylenia standardowego J w danej populacji
        j_max.append(population[pop_num-1].J)                           # wybranie maksymalnej wartości J z danej populacji

        x1_max.append(population[pop_num-1].x1)                         # wybranie x1 i x2 dla parametrów dających maks. J w danej populacji
        x2_max.append(population[pop_num - 1].x2)

        u_std_list = standard_deviation(population, pop_num, "u")           # obliczenie odchylenia standardowego dla kolejnych parametrów u w danej populacji
        u_avg_list = u_mean_in_population(population, pop_num)             # obliczenie średniej kolejnych parametrów u w danej populacji

        for k in range(population[0].n):
            u_std[k].append(u_std_list[k])
            u_avg[k].append(u_avg_list[k])

    # ===== UZYSKANE WYNIKI J W OSTATNIM POKOLENIU ===== #
    print()
    print(f'Maxymalne J={j_max[l_epok - 1]}')
    print(f'Średnie J={j_avg[l_epok - 1]}')

    # ===== RYSOWANIE WYKRESÓW ===== #
    x_num = np.linspace(1, l_epok, l_epok)
    # średnia, maks i odchylenie standardowe J
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot()
    plt.grid()
    ax.set_title("Średnia wartości wskaźnika jakości sterowania J w kolejnych pokoleniach \n"
                 f"liczba parametrów N = {population[0].n}")
    
    ax.set_xlabel('Pokolenie')
    ax.set_ylabel("J [u]")
    ax.plot(x_num, j_avg, label="AVG J")
    
    # std powiększone dwukrotnie, w celu uwidocznienia go na wykresie
    ax.fill_between(x_num, j_avg - 2 * np.asarray(j_std), j_avg + 2 * np.asarray(j_std), alpha=0.2, label="STD J")
    ax.plot(x_num, j_max, label="MAX J")
    ax.legend(loc='lower right')
    plt.show()

    # średnia, maks i odchylenie standardowe u
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot()
    for i in range(population[0].n):
        ax.plot(x_num, u_avg[i],'-x',label=f'U [{i}]')
        ax.fill_between(x_num, np.asarray(u_avg[i]) - 2 * np.asarray(u_std[i]), np.asarray(u_avg[i]) + 2 * np.asarray(u_std[i]), alpha=0.2)
    ax.set_title("Parametry sterowania u[k] w kolejnych pokoleniach \n"
                 "liczba parametrów N = " + str(population[0].n))
    ax.set_xlabel('Pokolenie')
    ax.set_ylabel("u[k]")
    ax.legend(loc='upper right', ncol=5)
    plt.show()

    # x1, x2
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(projection='3d')
    ax.set_title("X1_X2")
    ax.plot(x1_max, x2_max, x_num,label=f'X1_X2')
    ax.set_title("Optymalne wartości parametrów dla modelu stanowego \nliczba parametrów N = " + str(population[0].n))
    ax.set_xlabel("x1 max")
    ax.set_ylabel("x2 max")
    ax.set_zlabel('Pokolenie')
    ax.legend(loc='upper right')
    plt.show()

