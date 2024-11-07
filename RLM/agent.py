import numpy as np

class QLearningAgent:
    def __init__(self, actions, q_table_path=None):
        self.actions = actions
        self.q_table = np.load(q_table_path, allow_pickle=True).item() if q_table_path else {}


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
        """Select action based on Q-table values."""
        q_values = {action: self.q_table.get((state, action), 0) for action in self.actions}
        best_action = max(q_values, key=q_values.get)
        return best_action

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