import numpy as np

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.05, epsilon_decay=0.9999995):
        self.actions = actions  # Actions are difficulties (easy, medium, hard)
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay
        self.q_table = {}


    def get_q_value(self, state, action):
        """ Return Q value for a given state-action pair """
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        """ Update Q value based on the Q-learning update rule """
        max_q_next = max([self.get_q_value(next_state, a) for a in self.actions])
        old_q = self.get_q_value(state, action)
        new_q = old_q + self.alpha * (reward + self.gamma * max_q_next - old_q)
        self.q_table[(state, action)] = new_q

    def select_action(self, state):
        """ Select action based on epsilon-greedy policy """
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        q_values = [self.get_q_value(state, action) for action in self.actions]
        max_q = max(q_values)
        return self.actions[q_values.index(max_q)]

    def decay_epsilon(self):
        """ Decay epsilon for exploration-exploitation balance """
        self.epsilon *= self.epsilon_decay

    def get_q_table(self):
        """ Return the entire Q-table """
        return self.q_table
    def print_q_table(self):
        for state_action, q_value in self.q_table.items():
            state, action = state_action
            print(f"State: {state}, Action: {action}, Q-Value: {q_value:.2f}")

    def save_q_table(self, file_path):
        """Save the Q-table to a .npy file."""
        np.save(file_path, self.q_table)