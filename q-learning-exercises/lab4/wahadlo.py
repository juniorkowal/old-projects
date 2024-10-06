import numpy as np
import random


def tile_coding(arrays, nums):
    coded_indices = [np.max(np.digitize(num, array) - 1, 0) for array, num in zip(arrays, nums)]

    return coded_indices

def create_start_var(bins_num = 20):
    a = np.linspace(-np.pi / 2, np.pi / 2, bins_num)
    a_p = np.linspace(-2, 2, bins_num)
    x = np.linspace(-60, 60, bins_num)
    v = np.linspace(-70, 70, bins_num)
    f = np.linspace(-1200, 1200, bins_num*2)

    # coordinates_5d = np.zeros(shape=(bins_num,bins_num,bins_num,bins_num,bins_num))
    coordinates_5d = np.random.uniform(-0.01, 0.01,size=(bins_num,bins_num,bins_num,bins_num,bins_num*2))
    return a, a_p, x, v, f, coordinates_5d

class Agent():
    def __init__(self) -> None:
        self.set_variables()

    def set_variables(self):
        self.Fmax = 1200
        self.krokcalk = 0.05
        self.g = 9.8135
        self.tar = 0.02
        self.masawoz = 20
        self.masawah = 20
        self.drw = 25

    def calculate_new_state(self, stan, F):
        F = np.clip(F, -self.Fmax, self.Fmax)
        hh, momwah = self.krokcalk * 0.5, self.masawah * self.drw
        cwoz, cwah = self.masawoz * self.g, self.masawah * self.g

        def update_state(stan):
            sx, cx = np.sin(stan[0]), np.cos(stan[0])
            c1 = self.masawoz + self.masawah * sx**2
            c2 = momwah * stan[1]**2 * sx
            c3 = self.tar * stan[3] * cx
            return np.array([stan[1], ((cwah+cwoz)*sx-c2*cx+c3-F*cx)/(self.drw*c1), stan[3], (c2-cwah*sx*cx-c3+F)/c1])

        stanpoch = update_state(stan)
        stanh = stan + stanpoch[:4] * hh
        stann = stan + update_state(stanh) * self.krokcalk
        stann[0] = (stann[0] + np.pi) % (2 * np.pi) - np.pi

        return stann

    def calculate_Q(self, coded_state, V):
        return V[coded_state[0],coded_state[1],coded_state[2],coded_state[3],coded_state[4]]

    def calculate_reward(self, s, ns, F):
        dev_penalty = np.dot([1, 0.25, 0.0025, 0.0025], ns)
        tip_penalty = (np.abs(ns[0]) >= np.pi / 2) * 1000
        angle_thresh = np.pi / 24
        pos_thresh = 0.5
        angle_close = np.maximum(0, angle_thresh - np.abs(ns[0]))
        pos_close = np.maximum(0, pos_thresh - np.abs(ns[2]))
        state_bonus = (angle_close * 50) + (pos_close * 0.5)
        force_change_penalty = 0.0001 * F
        reward = -(dev_penalty + tip_penalty) + state_bonus - force_change_penalty
        return reward

    def epsilon_greedy(self, epsilon, state, V, limits):
        if random.random() < epsilon:
            action_index = random.randint(0, len(limits[-1]) - 1)  # Choosing a random action
        else:
            action_index = self.get_best_action(state, V, limits)

        return action_index

    def get_best_action(self, state, V, limits):
        Qs = [self.calculate_Q(tile_coding(limits, np.append(state, action)), V) for action in limits[-1]]
        best_action = np.argmax(Qs)
        return best_action

    def start_training(self):
        episode_num = 100000000
        alpha = 0.2            # wsp.szybkosci uczenia(moze byc funkcja czasu)
        epsilon = 0.7           # wsp.eksploracji(moze byc funkcja czasu)
        epsilon_min = 0.01
        epsilon_discount = 0.9999
        gamma = 0.9
        self.params_num = 5

        # [alfa, alfa*, x, v, f (actions)]
        a,b,c,d,e,V = create_start_var(self.params_num)
        encoding_bins = (a,b,c,d,e)
        print("Liczba zakodowanych stanów: ",self.params_num*len(encoding_bins))

        # tablica wag
        # V = np.zeros(self.params_num*len(encoding_bins))
        # V = np.random.uniform(-0.01, 0.01, size=self.params_num*len(encoding_bins))
        # print(V)
        print(V.shape)

        stanp = np.array([[np.pi/6,0, 0, 0],[0, np.pi/3, 0, 0], [0, 0, -10, 1], [0, 0, 0, -10], [np.pi/12, np.pi/6, 0, 0],
                        [np.pi/12, -np.pi/6, 0, 0], [-np.pi/12, np.pi/6, 0, 0], [-np.pi/12, -np.pi/6, 0, 0],
                        [np.pi/12, 0, 0, 0], [0, 0, -10, 10]],dtype=float)

        liczba_stanow_poczatkowych, _ = stanp.shape

        steps = []
        Qs=[]
        Qs_p=[]
        Rs = []
        self.weights = {}
        for episode in range(episode_num): # DLA KAŻDEGO EPIZODU
            # Wybieramy stan poczatkowy:
            # stan = rand(1,4).*[pi/1.5 pi/1.5 20 20] - [pi/3 pi/3 10 10] % met.losowa
            nr_stanup = episode %  liczba_stanow_poczatkowych # ZAINICJUJ STAN POCZĄTKOWY Z LOSOWEJ LISTY
            state = stanp[nr_stanup, :]

            krok = 0
            czy_wahadlo_przewrocilo_sie = 0
            while (krok < 1000) & (czy_wahadlo_przewrocilo_sie == 0):
                krok += 1

                # EKSPLORACJA EPSILON GREEDY
                A_index = self.epsilon_greedy(epsilon, state, V, encoding_bins)
                A = encoding_bins[len(encoding_bins)-1][A_index]

                # wyznaczenie nowego stanu:
                state_prime = self.calculate_new_state(state, A)

                czy_wahadlo_przewrocilo_sie = (abs(state_prime[0]) >= np.pi / 2)
                R = self.calculate_reward(state, state_prime, A)

                # Aktualizujemy wartosci Q dla aktualnego stanu i wybranej akcji:
                # w = w + alfa * (R + gamma * np.max(Q[S', a, w]) - Q[S, A, w]) * delta_w * Q[S,A,w]
                coded_Q = tile_coding(encoding_bins, np.append(state,A))
                # Q dla aktualnego state S, A, w
                Q = self.calculate_Q(coded_Q, V)

                # Najlepsza akcja przy Q dla state_prime
                Q_prime_best_action = self.get_best_action(state_prime, V, encoding_bins)
                coded_Q_prime = tile_coding(encoding_bins, np.append(state_prime,Q_prime_best_action))
                Q_prime = self.calculate_Q(coded_Q_prime, V)

                V[coded_Q[0],coded_Q[1],coded_Q[2],coded_Q[3],coded_Q[4]] += alpha * (R + gamma * Q_prime - Q)


                state = state_prime # S <- S'
                # DEBUG
                Qs.append(Q)
                Qs_p.append(Q_prime)
                Rs.append(R)

            epsilon *= epsilon_discount
            epsilon = max(epsilon, epsilon_min)
            # DEBUG
            steps.append(krok)
            # print(krok)
            # co jakis czas test z wygenerowaniem historii do pliku:
            if episode % 10 == 0:
                # self.wahadlo_test(stanp, V)
                print(f"Średnia liczba kroków: {np.mean(steps):.4f}, Epizod: {episode}, Stan wag: {len(np.unique(V))}, Epsylon: {epsilon:.4f}, Akcja: {A:.2f}, Q: {np.mean(Qs):.2f}, Q_prime: {np.mean(Qs_p):.2f}, R: {np.mean(Rs):.2f}, V: {np.mean(V):.2f}")
            if episode % 1000 == 0:
                self.wahadlo_test(stanp, V)
            if episode % 2000 == 0:
                np.save(f"weights_{episode}.npy", V)

    def wahadlo_test(self,stanp, V):
        Fmax, krokcalk, g, tar, masawoz, masawah, drw = self.Fmax, self.krokcalk,self.g,self.tar,self.masawoz,self.masawah,self.drw
        pli = open('historia_duzo_parametrow.txt', 'w')
        pli.write("Fmax = " + str(Fmax) + "\n")
        pli.write("krokcalk = " + str(krokcalk) + "\n")
        pli.write("g = " + str(g) + "\n")
        pli.write("tar = " + str(tar) + "\n")
        pli.write("masawoz = " + str(masawoz) + "\n")
        pli.write("masawah = " + str(masawah) + "\n")
        pli.write("drw = " + str(drw) + "\n")

        a,b,c,d,e,_ = create_start_var(self.params_num)
        encoding_bins = (a,b,c,d,e)
        print("Liczba zakodowanych stanów: ",self.params_num*len(encoding_bins))

        self.params_num = 5

        sr_suma_nagrod = 0
        liczba_krokow = 0

        stanp = np.array([[np.pi/6,0, 0, 0],[0, np.pi/3, 0, 0], [0, 0, -10, 1], [0, 0, 0, -10], [np.pi/12, np.pi/6, 0, 0],
                        [np.pi/12, -np.pi/6, 0, 0], [-np.pi/12, np.pi/6, 0, 0], [-np.pi/12, -np.pi/6, 0, 0],
                        [np.pi/12, 0, 0, 0], [0, 0, -10, 10]],dtype=float)

        liczba_stanow_poczatkowych, lparam = stanp.shape

        for epizod in range(liczba_stanow_poczatkowych):
            # Wybieramy stan poczatkowy:
            nr_stanup = epizod
            state = stanp[nr_stanup, :]

            krok = 0
            suma_nagrod_epizodu = 0
            czy_przewrocenie_wahadla = 0
            while (krok < 1000) & (czy_przewrocenie_wahadla == 0):
                krok = krok + 1

                A_index = self.get_best_action(state, V, encoding_bins)
                A = encoding_bins[len(encoding_bins)-1][A_index]

                # wyznaczenie nowego stanu:
                state_prime = self.calculate_new_state(state, A)

                czy_przewrocenie_wahadla = (abs(state_prime[0]) >= np.pi / 2)
                R = self.calculate_reward(state, state_prime, A)

                suma_nagrod_epizodu = suma_nagrod_epizodu + R

                pli.write(str(epizod + 1) + "  " + str(state[0]) + "  " + str(state[1]) + "  " + str(state[2]) + "  " + str(state[3]) + "  " + str(A) + "\n")

                state = state_prime

            sr_suma_nagrod = sr_suma_nagrod + suma_nagrod_epizodu / liczba_stanow_poczatkowych
            liczba_krokow = liczba_krokow + krok
            print("w %d epizodzie suma nagrod = %g, liczba krokow = %d" %(epizod, suma_nagrod_epizodu, krok))

        print("srednia suma nagrod w epizodzie = %g" % (sr_suma_nagrod))
        print("srednia liczba krokow ustania wahadla = %g" % (liczba_krokow/liczba_stanow_poczatkowych))

        pli.close()

if __name__ == "__main__":
    wahadlo = Agent()
    wahadlo.start_training()