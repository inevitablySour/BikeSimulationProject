from env import BikingQuizEnv
from agent import QLearningAgent
import random

class Trainer:
    def __init__(self, episodes=1000000, steps_per_episode=100):
        self.env = BikingQuizEnv()
        self.agent = QLearningAgent(actions=["easy", "medium", "hard"])
        self.episodes = episodes
        self.steps_per_episode = steps_per_episode

    def train(self):
        for episode in range(self.episodes):
            state = self.env.reset()  # Start from the initial level
            total_reward = 0

            for step in range(self.steps_per_episode):
                # Agent selects action (difficulty level) based on the current state
                difficulty = self.agent.select_action(state)

                # Environment provides a question and calculates the new state and reward
                question = self.env.get_question()

                # Simulate the user's response randomly for training purposes
                correct = random.choice([True, False])  # Randomly simulate user correctness
                next_state, reward = self.env.step(correct)
                total_reward += reward

                # Update Q-table for the agent
                self.agent.update_q_value(state, difficulty, reward, next_state)
                state = next_state

            # Decay epsilon after each episode to reduce exploration over time
            self.agent.decay_epsilon()

            # Optional: print progress every 100,000 episodes
            if (episode + 1) % 100000 == 0:
                print(f"Episode {episode + 1}/{self.episodes}, Total Reward: {total_reward}, Epsilon: {self.agent.epsilon}")

        self.agent.save_q_table('trained_q_table_new.npy')

if __name__ == "__main__":
    trainer = Trainer(episodes=1000000, steps_per_episode=100)
    trainer.train()
    print(trainer.agent.print_q_table())