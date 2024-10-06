import numpy as np
import torch
import torch.nn as nn


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


class NeuralQLearning(torch.nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=64):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            # nn.Dropout(p=dropout_prob),
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            # nn.Dropout(p=dropout_prob),
            nn.Linear(hidden_dim * 2, action_dim),
            nn.Sigmoid()
        )

    def forward(self, state) -> torch.Tensor:
        # state = state.numpy()
        # return self.model(torch.from_numpy(state))
        return self.model(state)
        

class ReplayBuffer():
    def __init__(self, max_size):
        self.max_size = max_size
        self.buffer = []

    def store_sample(self, state, action, reward, next_state):
        self.buffer.append((state, action, reward, next_state))

        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def sample(self, k=1):
        samples_count = min(len(self.buffer), k)
        indices = np.random.choice(len(self.buffer), samples_count, replace=False)

        samples = [self.buffer[idx] for idx in indices]

        return samples


class Agent:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.set_variables()
        self.NUM_PARAMS = 10000
        self.KANERVA_N = 4
        self.ACTIONS_NUM = 10
        self.BATCH_SIZE = 100

        self.action_space = np.linspace(-self._Fmax, self._Fmax, self.ACTIONS_NUM)

        limits = [[-np.pi / 2, np.pi / 2],
                  [-2, 2],
                  [-60, 60],
                  [-70, 70]]

        self.exploration_method = EpsilonGreedy()

        self.neural_approx = NeuralQLearning(self.KANERVA_N, len(self.action_space))
        self.neural_approx_target = NeuralQLearning(self.KANERVA_N, len(self.action_space))
        self.neural_approx_target.load_state_dict(self.neural_approx.state_dict())

        self.buffer = ReplayBuffer(self.NUM_PARAMS)

        lr = 0.01
        self.criterion = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.neural_approx.parameters(), lr)

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
    
    def learn(self):
        replays = self.buffer.sample(self.BATCH_SIZE)

        states_features_batch = torch.tensor([replay[0] for replay in replays], dtype=torch.float32)
        action_indexes_batch = torch.tensor([replay[1] for replay in replays], dtype=torch.int64).unsqueeze(1)
        reward_batch = torch.tensor([replay[2] for replay in replays], dtype=torch.float32)
        next_states_features_batch = torch.tensor([replay[3] for replay in replays], dtype=torch.float32)

        q_values_pred = self.neural_approx(states_features_batch).gather(1, action_indexes_batch).squeeze(1)

        with torch.no_grad():
            q_values_target = reward_batch + self.gamma * self.neural_approx_target(next_states_features_batch).max(1).values

        loss = self.criterion(q_values_pred, q_values_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()    
    
    def calculate_Q(self, state, action_index):
        with torch.inference_mode():
            return self.neural_approx.predict(state)[action_index]
    
    def get_best_action(self, state):
        with torch.inference_mode():
            best_action_index = self.neural_approx(torch.from_numpy(state.astype(np.float32))).argmax().item()

        return self.action_space[best_action_index], best_action_index



    def start_training(self):
        episode_num = 100000000
        self.alpha = 0.2 # najlepsze 0.2
        epsilon = 0.7
        epsilon_min = 0.01
        epsilon_discount = 0.9999
        self.gamma = 0.9

        initial_states_list = np.array([[np.pi/6, 0, 0, 0],[0, np.pi/3, 0, 0], [0, 0, -10, 1], [0, 0, 0, -10], 
                                        [np.pi/12, np.pi/6, 0, 0],[np.pi/12, -np.pi/6, 0, 0], [-np.pi/12, np.pi/6, 0, 0], 
                                        [-np.pi/12, -np.pi/6, 0, 0],[np.pi/12, 0, 0, 0], [0, 0, -10, 10]],dtype=float)

        initial_states_num, _ = initial_states_list.shape

        steps = []
        Rs = []
        

        thresh = 100
        for episode in range(episode_num):
            self.neural_approx.train()
            self.neural_approx_target.train()
            
            initial_state = episode % initial_states_num
            state = initial_states_list[initial_state, :]

            krok = 0
            czy_wahadlo_przewrocilo_sie = 0
            q_errors = 0

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

                self.buffer.store_sample(state, A_index, R, state_prime)

                loss = self.learn()
                q_errors += loss

                # for state, action_index, reward, next_state in self.buffer.sample(self.BATCH_SIZE):
                #     self.update_weights(state, next_state, reward, action_index)

                if krok % 5 == 0:
                    self.neural_approx_target.load_state_dict(self.neural_approx.state_dict())

                state = state_prime # S <- S'

                #DEBUG
                Rs.append(R)

            # for state, action_index, reward, next_state in self.buffer.sample(10):
            #     self.update_weights(state, next_state, reward, int(action_index))      

            self.neural_approx.eval()
            self.neural_approx_target.eval()

            epsilon *= epsilon_discount
            epsilon = max(epsilon, epsilon_min)
            steps.append(krok)

            if int(np.mean(steps)) > thresh:
                print(f"Przekroczono threshold {thresh} kroków, zapisywanie wag self.weights ...")
                print("Kroki: ", steps)
                thresh += 100
                # np.save(f"weights_{int(np.mean(steps))}.npy", self.weights)
                self.pendulum_test()
            if episode % 10 == 0:
                # self.wahadlo_test(stanp, V)
                print(f"Średnia liczba kroków: {np.mean(steps):.4f}, Epizod: {episode}, Q_error: {q_errors/krok}, Epsylon: {epsilon:.4f}, Akcja: {A:.2f}, R: {np.mean(Rs):.2f}")
                steps = []
                Rs = []

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

        sr_suma_nagrod = 0
        liczba_krokow = 0

        for episode in range(initial_states_num):

            initial_state = episode % initial_states_num
            state = initial_states_list[initial_state, :]

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
