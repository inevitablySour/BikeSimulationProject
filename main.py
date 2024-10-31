import numpy as np
from env import BikingQuizEnv
from agent import QLearningAgent

class QuizGame:
    def __init__(self, agent):
        self.agent = agent
        self.env = agent.env  # Use the same environment as the agent
        self.current_state = 0  # Starting as a beginner
        self.score = 0  # Track the user's score

    def get_user_answer(self, difficulty):
        """ Simulate the user answering the question """
        if difficulty == 'easy':
            return np.random.choice([1, 0], p=[0.8, 0.2])
        elif difficulty == 'medium':
            return np.random.choice([1, 0], p=[0.6, 0.4])
        else:
            return np.random.choice([1, 0], p=[0.4, 0.6])

    def play_round(self):
        # Agent chooses the difficulty based on the current state
        difficulty = self.agent.choose_action(self.current_state)
        print(f"\nPresenting a {difficulty} question to the user.")

        # Simulate user answering the question
        user_correct = self.get_user_answer(difficulty)
        print(f"User answered {'correctly' if user_correct else 'incorrectly'}.")

        # Update state and reward based on the environment's response
        reward, new_state, done = self.env.step(difficulty)
        self.agent.update_q_table(self.current_state, difficulty, reward, new_state)

        # Update the current state
        self.current_state = new_state
        self.score += user_correct

        if done:
            print("Congratulations! You've reached the advanced level.")
            return True  # Game ends when the advanced state is reached
        return False  # Continue the game if not done

    def play(self):
        """ Run the quiz until the user reaches the advanced state """
        game_over = False
        round_num = 1

        while not game_over:
            print(f"\n--- Round {round_num} ---")
            game_over = self.play_round()
            round_num += 1

        print(f"Game Over! Your final score is {self.score}.")

# Main entry point to run the quiz game
if __name__ == "__main__":
    # Initialize the environment and agent
    env = BikingQuizEnv()
    agent = QLearningAgent(env, learning_rate=0.1, epsilon=0.1)  # Use lower epsilon for more exploitation during quiz

    # Load the trained Q-table from file
    try:
        q_table_loaded = np.load('trained_q_table_new.npy')
        agent.env.q_table = q_table_loaded  # Load the Q-table into the agent's environment
        print("Q-table loaded successfully!")
    except FileNotFoundError:
        print("Trained Q-table not found! Please train the agent first.")

    # Run the quiz with the loaded agent
    quiz_game = QuizGame(agent)
    quiz_game.play()