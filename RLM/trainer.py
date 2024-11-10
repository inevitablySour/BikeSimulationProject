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
            state = self.env.reset()
            total_reward = 0

            for step in range(self.steps_per_episode):

                difficulty = self.agent.select_action(state)

                question = self.env.get_question()

                correct = random.choice([True, False])
                next_state, reward = self.env.step(correct)
                total_reward += reward

                self.agent.update_q_value(state, difficulty, reward, next_state)
                state = next_state

            self.agent.decay_epsilon()

            if (episode + 1) % 100000 == 0:
                print(f"Episode {episode + 1}/{self.episodes}, Total Reward: {total_reward}, Epsilon: {self.agent.epsilon}")

        self.agent.save_q_table('RLM/trained_q_table.npy')

if __name__ == "__main__":
    trainer = Trainer(episodes=1000000, steps_per_episode=100)
    trainer.train()
    print(trainer.agent.print_q_table())