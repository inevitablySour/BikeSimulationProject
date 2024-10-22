import numpy as np

class BikingQuizEnv:
    def __init__(self):
        self.states = ['beginner', 'intermediate', 'advanced']  # skill levels
        self.actions = ['easy', 'medium', 'hard']  # difficulty levels
        self.q_table = np.zeros((len(self.states), len(self.actions)))  # Initialize Q-table
        self.state = 0  # Start as a beginner

    def get_state_index(self):
        return self.state

    def get_action_index(self, action):
        return self.actions.index(action)


    def step(self, action):
        if action == 'easy':
            reward = np.random.choice([0.1, 0], p=[0.8, 0.2])
        elif action == 'medium':
            reward = np.random.choice([0.4, 0], p=[0.6, 0.4])  # Increased reward
        else:
            reward = np.random.choice([0.6, 0], p=[0.4, 0.6])  # Increased reward

        # Adjust skill level and return done (increased chance of moving up/down)
        if reward > 0:
            if np.random.rand() < 0.5:  # 50% chance of moving up on success
                if self.state < len(self.states) - 1:
                    self.state += 1
        else:
            if np.random.rand() < 0.5:  # 50% chance of moving down on failure
                if self.state > 0:
                    self.state -= 1

        done = self.state == len(self.states) - 1  # Done when reaching advanced state
        return reward, self.state, done

    def reset(self):
        self.state = 0  # Reset to beginner