import numpy as np


class KanervaCoder:
    def __init__(self, dims, ptypes, n_active, limits, dist=None, seed=None):
        np.random.seed(seed)
        self._n_pts = ptypes
        self._k = n_active
        self._lims = np.array(limits)
        # POTRZEBNE DO SKALOWANIA PKT DO 0,1
        self._ranges = self._lims[:, 1] - self._lims[:, 0]
        # LOSOWANIE PKT W PRZEDZIALE 0,1 DLA USTALONYCH WYMIAROW
        self._pts = np.random.random([self._n_pts, dims])
        # USTAWIANIE DOMYSLNEGO OBLICZANIA DYSTANSU
        # self._dist = dist or (lambda x1, x2: np.max(np.abs(x1 - x2), axis=1))
        self._dist = dist or (lambda x1, x2: np.max(np.sqrt(np.subtract(x1,x2)**2), axis=1))
        
    @property
    def n_ptypes(self):
        return self._n_pts

    def __getitem__(self, x):
        # NORMALIZACJA PUNKTU WEJSCIOWEGO DO PRZEDZIALU 0,1
        xs = (x - self._lims[:, 0]) / self._ranges
        # OBLICZANIE DYSTANSU
        distances = self._dist(self._pts, xs)
        # SORTOWANIE WZGLEDEM K-TEGO PUNKTU I WYBRANIE POSORTOWANYCH
        return np.argpartition(distances, self._k)[:self._k]
    
    def decode_indices(self, indices):
        # ZWYKLE ZWRACANIE ZDEKODOWANYCH STANOW
        return self._pts[indices]


class EpsilonGreedy:
    def __getitem__(self, epsilon_best_action):
        epsilon, best_action, best_action_index, action_space = epsilon_best_action
        if np.random.random() < epsilon:
            action_index = np.random.randint(0, len(action_space) - 1)
            action = action_space[action_index]
        else:
            action = best_action
            action_index = best_action_index
        return action, action_index


class Agent:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.set_variables()
        self.NUM_PARAMS = 1024
        self.action_space = np.linspace(-self._Fmax, self._Fmax, self.NUM_PARAMS // 100)

        limits = [[-np.pi / 2, np.pi / 2],
                  [-2, 2],
                  [-60, 60],
                  [-70, 70]]
        
        self.coder = KanervaCoder(dims = 4, ptypes = self.NUM_PARAMS, n_active = 32, limits = limits, seed = 316)
        self.weights = [np.random.rand(self.coder.n_ptypes) for _ in self.action_space]

        self.exploration_method = EpsilonGreedy()

    def set_variables(self):
        self._Fmax = 1200
        self._step_size = 0.05
        self._gravity = 9.8135
        self._friction = 0.02
        self._mass_pendulum = 20
        self._cart_width = 25

    def calculate_new_state(self, stan, F):
        F = np.clip(F, -self._Fmax, self._Fmax)
        hh, momwah = self._step_size * 0.5, self._mass_pendulum * self._cart_width
        cwoz, cwah = self._mass_pendulum * self._gravity, self._mass_pendulum * self._gravity

        def update_state(stan):
            sx, cx = np.sin(stan[0]), np.cos(stan[0])
            c1 = self._mass_pendulum + self._mass_pendulum * sx**2
            c2 = momwah * stan[1]**2 * sx
            c3 = self._friction * stan[3] * cx
            return np.array([stan[1], ((cwah+cwoz)*sx-c2*cx+c3-F*cx)/(self._cart_width*c1), stan[3], (c2-cwah*sx*cx-c3+F)/c1])

        stanpoch = update_state(stan)
        stanh = stan + stanpoch[:4] * hh
        stann = stan + update_state(stanh) * self._step_size
        stann[0] = (stann[0] + np.pi) % (2 * np.pi) - np.pi

        return stann
    
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
    
    def calculate_Q(self, state, action_index):
        coded_state = self.coder[state]
        return np.sum(self.weights[action_index][coded_state]) #/ (np.max(self.weights) + 1e-10)
    
    def get_best_action(self, state):
        Qs = []
        for action_index in range(len(self.action_space)):
            Qs.append(self.calculate_Q(state, action_index))

        best_action_index = np.argmax(Qs)
        return self.action_space[best_action_index], best_action_index
    
    # def get_best_action(self, state):
    #     Qs = np.array([self.calculate_Q(state, action_index) for action_index in range(len(self.action_space))])
    #     best_action_index = np.argmax(Qs)
    #     return self.action_space[best_action_index], best_action_index

    # def get_best_action(self, state):
    #         Qs = []
    #         for action_index in range(len(self.action_space)):
    #             Qs.append(self.calculate_Q(state, action_index))
    #         best_action_index = np.argmax(Qs)
    #         return self.action_space[best_action_index], best_action_index 
       
    def start_training(self):
        episode_num = 100000000
        alpha = 0.2 # najlepsze 0.2
        epsilon = 0.7
        epsilon_min = 0.01
        epsilon_discount = 0.9999
        gamma = 0.9

        initial_states_list = np.array([[np.pi/6, 0, 0, 0],[0, np.pi/3, 0, 0], [0, 0, -10, 1], [0, 0, 0, -10], 
                                        [np.pi/12, np.pi/6, 0, 0],[np.pi/12, -np.pi/6, 0, 0], [-np.pi/12, np.pi/6, 0, 0], 
                                        [-np.pi/12, -np.pi/6, 0, 0],[np.pi/12, 0, 0, 0], [0, 0, -10, 10]],dtype=float)

        initial_states_num, _ = initial_states_list.shape

        steps = []
        Rs = []
        state_to_start = 0

        thresh = 100
        for episode in range(episode_num):

            # initial_state = episode % initial_states_num
            state = initial_states_list[state_to_start, :]

            state_to_start += 1
            if state_to_start > len(initial_states_list)-1:
                state_to_start = 0

            krok = 0
            czy_wahadlo_przewrocilo_sie = 0
            while (krok < 1000) & (czy_wahadlo_przewrocilo_sie == 0):
                krok += 1

                # EKSPLORACJA EPSILON GREEDY
                A, A_index = self.exploration_method[(epsilon, self.get_best_action(state)[0], self.get_best_action(state)[1], self.action_space)]
                # A_index = np.where(self.action_space == A)[0][0]

                # wyznaczenie nowego stanu:
                state_prime = self.calculate_new_state(state, A)

                czy_wahadlo_przewrocilo_sie = (abs(state_prime[0]) >= np.pi / 2)
                R = self.calculate_reward(state, state_prime, A)

                # Aktualizujemy wartosci Q dla aktualnego stanu i wybranej akcji:
                # w = w + alfa * (R + gamma * np.max(Q[S', a, w]) - Q[S, A, w]) * delta_w * Q[S,A,w]

                coded_state = self.coder[state]
                self.weights[A_index][coded_state] += alpha * (R + gamma * self.calculate_Q(state_prime, self.get_best_action(state_prime)[1]))- self.calculate_Q(state, A_index)

                state = state_prime # S <- S'

                #DEBUG
                Rs.append(R)
                
            epsilon *= epsilon_discount
            epsilon = max(epsilon, epsilon_min)
            steps.append(krok)

            if int(np.mean(steps)) > thresh:
                thresh += 100
                print("Przekroczono threshold 100 kroków, zapisywanie wag ...")
                np.save(f"weights_{int(np.mean(steps))}.npy", self.weights)
                self.pendulum_test()
            if episode % 10 == 0:
                print(f"Średnia liczba kroków: {np.mean(steps):.4f}, Epizod: {episode}, Stan wag: {len(np.unique(self.weights))}, Epsylon: {epsilon:.4f}, Akcja: {A:.2f}, R: {np.mean(Rs):.2f}")
                steps = [0]
                Rs = [0]


    def pendulum_test(self):
        Fmax, krokcalk, g, tar, masawoz, masawah, drw = self._Fmax, self._step_size,self._gravity,self._friction,self._mass_pendulum,self._mass_pendulum,self._cart_width
        pli = open('historia.txt', 'w')
        pli.write("Fmax = " + str(Fmax) + "\n")
        pli.write("krokcalk = " + str(krokcalk) + "\n")
        pli.write("g = " + str(g) + "\n")
        pli.write("tar = " + str(tar) + "\n")
        pli.write("masawoz = " + str(masawoz) + "\n")
        pli.write("masawah = " + str(masawah) + "\n")
        pli.write("drw = " + str(drw) + "\n")

        initial_states_list = np.array([[np.pi/6, 0, 0, 0],[0, np.pi/3, 0, 0], [0, 0, -10, 1], [0, 0, 0, -10], 
                                        [np.pi/12, np.pi/6, 0, 0],[np.pi/12, -np.pi/6, 0, 0], [-np.pi/12, np.pi/6, 0, 0], 
                                        [-np.pi/12, -np.pi/6, 0, 0],[np.pi/12, 0, 0, 0], [0, 0, -10, 10]],dtype=float)

        initial_states_num, _ = initial_states_list.shape

        state_to_start = 0        

        sr_suma_nagrod = 0
        liczba_krokow = 0

        for episode in range(initial_states_num):

            state = initial_states_list[state_to_start, :]

            state_to_start += 1
            if state_to_start > len(initial_states_list)-1:
                state_to_start = 0

            suma_nagrod_epizodu = 0
            krok = 0
            czy_wahadlo_przewrocilo_sie = 0
            while (krok < 1000) & (czy_wahadlo_przewrocilo_sie == 0):
                krok += 1

                A, _ = self.get_best_action(state)

                # wyznaczenie nowego stanu:
                state_prime = self.calculate_new_state(state, A)

                czy_wahadlo_przewrocilo_sie = (abs(state_prime[0]) >= np.pi / 2)
                R = self.calculate_reward(state, state_prime, A)
                
                suma_nagrod_epizodu = suma_nagrod_epizodu + R

                pli.write(str(episode + 1) + "  " + str(state[0]) + "  " + str(state[1]) + "  " + str(state[2]) + "  " + str(state[3]) + "  " + str(A) + "\n")

                state = state_prime

            sr_suma_nagrod = sr_suma_nagrod + suma_nagrod_epizodu / initial_states_num
            liczba_krokow = liczba_krokow + krok
            print("w %d epizodzie suma nagrod = %g, liczba krokow = %d" %(episode, suma_nagrod_epizodu, krok))

        print("srednia suma nagrod w epizodzie = %g" % (sr_suma_nagrod))
        print("srednia liczba krokow ustania wahadla = %g" % (liczba_krokow/initial_states_num))

        pli.close()

if __name__ == "__main__":
    pendulum_agent = Agent()
    pendulum_agent.start_training()
