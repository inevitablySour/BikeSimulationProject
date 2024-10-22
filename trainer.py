from env import BikingQuizEnv
from agent import QLearningAgent
import time
import numpy as np

def train_agent(env, agent, episodes=1000000, max_steps_per_episode=100, epsilon_decay=0.995):
    for episode in range(episodes):
        state = env.get_state_index()
        step_count = 0
        done = False

        # Decay epsilon (exploration rate) after each episode
        agent.epsilon = max(agent.epsilon * epsilon_decay, 0.01)  # Ensure epsilon doesn't go below 0.01

        while not done and step_count < max_steps_per_episode:
            # Choose action
            action = agent.choose_action(state)

            # Take action and get reward
            reward, next_state, done = env.step(action)

            # Update Q-table
            agent.update_q_table(state, action, reward, next_state)

            # Move to the next state
            state = next_state
            step_count += 1

        # Reset the environment after each episode
        env.reset()

if __name__ == "__main__":
    env = BikingQuizEnv()
    agent = QLearningAgent(env, learning_rate=0.1, epsilon=0.9)
      # Multiply epsilon by this factor every episode

    start_time = time.time()

    # Train the agent
    train_agent(env, agent, episodes=1000000, max_steps_per_episode=100, epsilon_decay = 0.995)  # Start with just 1 episode for testing

    # After training
    np.save('trained_q_table.npy', agent.env.q_table)
    print("Q-table saved successfully!")

    # Print the Q-table after training
    print("Trained Q-table:")
    print(env.q_table)

    end_time = time.time()
    print(f"Training completed in {end_time - start_time} seconds")