import numpy as np
from abc import ABC, abstractmethod

class Strategy(ABC):

    def __init__(self, k):
        self.k = k

    @property
    @abstractmethod
    def name():
        pass

    @abstractmethod
    def act(self) -> int:
        pass
    
    @abstractmethod
    def update(self, action, reward):
        pass

    @abstractmethod
    def reset(self):
        pass

class MyStrategy(Strategy):
    pass # TODO: implement your own strategy!

class EpsilonGreedy(Strategy):

    def __init__(self, k, epsilon=0, initial=0):
        super().__init__(k)
        self.epsilon = epsilon
        self.initial = initial
        self.q_estimations = np.zeros(self.k) + self.initial
        self.selections = np.zeros(self.k)
        self.indices = np.arange(self.k)

    @property
    def name(self):
        name_str = ""
        if (self.epsilon == 0):
            name_str = "Greedy"
        else:
            name_str = f"$\\epsilon$-greedy, $\\epsilon = {self.epsilon}$"
        if (self.initial != 0):
            name_str += f", init: {self.initial}"
        return name_str
    
    def act(self):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.indices)
        else:
            q_max = np.max(self.q_estimations)
            return np.random.choice(np.where(self.q_estimations == q_max)[0])

    def update(self, action, reward):
        self.selections[action] += 1
        self.q_estimations[action] += (reward - self.q_estimations[action]) / self.selections[action]
    
    def reset(self):
        self.q_estimations = np.zeros(self.k) + self.initial
        self.selections = np.zeros(self.k)

class UCB(Strategy):

    def __init__(self, k, c=1, initial=0):
        super().__init__(k)
        self.c = c
        self.initial = initial
        self.q_estimations = np.zeros(self.k) + self.initial
        self.selections = np.zeros(self.k)
        self.t = 0
    
    @property
    def name(self):
        return f"UCB, $c = {self.c}$"

    def act(self):
        UCB_estimations = self.q_estimations + self.c * np.sqrt(np.log(self.t + 1) / (self.selections + 1e-5))
        UCB_max = np.max(UCB_estimations)
        return np.random.choice(np.where(UCB_estimations == UCB_max)[0])

    def update(self, action, reward):
        self.t += 1
        self.selections[action] += 1
        self.q_estimations[action] += (reward - self.q_estimations[action]) / self.selections[action]
    
    def reset(self):
        self.t = 0
        self.q_estimations = np.zeros(self.k) + self.initial
        self.selections = np.zeros(self.k)

class Gradient(Strategy):

    def __init__(self, k, alpha=0.1):
        super().__init__(k)
        self.alpha = alpha
        self.preferences = np.zeros(self.k)
        self.indices = np.arange(self.k)
        self.baseline = 0
        self.t = 0
    
    @property
    def name(self):
        return f"Gradient, $\\alpha = {self.alpha}$"

    def act(self):
        return np.random.choice(self.indices, p=self.softmax(self.preferences))
    
    def update(self, action, reward):
        self.t += 1
        self.baseline += (reward - self.baseline) / self.t
        one_hot = np.zeros(self.k)
        one_hot[action] = 1
        self.preferences += self.alpha * (reward - self.baseline) * (one_hot - self.softmax(self.preferences))
    
    def reset(self):
        self.t = 0
        self.baseline = 0
        self.preferences = np.zeros(self.k)

    def softmax(self, x):
        return np.exp(x)/sum(np.exp(x))