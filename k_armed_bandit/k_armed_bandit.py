import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tqdm import trange
import strategy

matplotlib.use('Agg')

K = 10

class Action:
    def __init__(self, distribution=None):
        self.mean = np.random.randn()
        self.distribution = distribution if distribution is not None else np.random.choice(["normal", "constant", "uniform"], p=[1, 0, 0])
    
    def get_reward(self):
        if self.distribution == "normal":
            return np.random.randn() + self.mean
        elif self.distribution == "uniform":
            return np.random.rand() + self.mean
        else:
            return self.mean

def simulate(strategies, runs=2000, time=1000):
    rewards = np.zeros((len(strategies), runs, time))
    best_action_choices = np.zeros(rewards.shape)

    for i, strategy in enumerate(strategies):
        print(f"Running strategy {i + 1}/{len(strategies)}...")
        for r in trange(runs):
            actions = [Action() for _ in range(K)]
            best_action = np.argmax([action.mean for action in actions])
            strategy.reset()
            for t in range(time):
                action = strategy.act()
                reward = actions[action].get_reward()
                rewards[i, r, t] = reward
                strategy.update(action, reward)

                if action == best_action:
                    best_action_choices[i, r, t] = 1

    mean_rewards = rewards.mean(axis=1)
    mean_best_action_choices = best_action_choices.mean(axis=1)

    return mean_rewards, mean_best_action_choices

def plot_results(strategies, rewards, best_action_choices):

    plt.figure(figsize=(10, 20))
    plt.subplot(2,1,1)

    for strategy, reward in zip(strategies, rewards):
        plt.plot(reward, label=f"{strategy.name}")
    plt.xlabel('Steps')
    plt.ylabel('Average reward')
    plt.legend()

    plt.subplot(2,1,2)
    for strategy, choices in zip(strategies, best_action_choices):
        plt.plot(choices, label=f"{strategy.name}")
    plt.xlabel('Steps')
    plt.ylabel('% Optimal action')
    plt.legend()

    plt.savefig("./images/results.png")
    plt.close()


if __name__ == "__main__":

    strategies = [
        strategy.EpsilonGreedy(K),
        strategy.EpsilonGreedy(K, epsilon=0.1),
        strategy.UCB(K, c=2),
        strategy.Gradient(K)
    ]

    rewards, best_action_choices = simulate(strategies)

    plot_results(strategies, rewards, best_action_choices)
