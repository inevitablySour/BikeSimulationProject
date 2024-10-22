import numpy as np

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    def choose_action(self, state):
        # Epsilon-greedy strategy for exploration vs exploitation
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.env.actions)  # Explore
        else:
            action_index = np.argmax(self.env.q_table[state])
            return self.env.actions[action_index]  # Exploit

    def update_q_table(self, state, action, reward, next_state):
        # Get indices for state and action
        state_index = self.env.get_state_index()
        action_index = self.env.get_action_index(action)

        # Current Q-value for the state-action pair
        current_q_value = self.env.q_table[state_index, action_index]

        # Maximum Q-value for the next state (for all possible actions)
        best_next_action = np.max(self.env.q_table[next_state])

        # Apply Q-learning formula to compute the new Q-value
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount_factor * best_next_action)

        # Update the Q-table with the new Q-value
        self.env.q_table[state_index, action_index] = new_q_value