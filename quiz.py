import numpy as np
from env import BikingQuizEnv
from agent import QLearningAgent

class BikingQuiz:
    def __init__(self):
        self.easy_questions = [
            {"question": "Is it mandatory to use bike lights at night?", "answer": "yes"},
            {"question": "Can you ride a bike on the sidewalk?", "answer": "no"},
            {"question": "Do you have to wear a helmet when biking?", "answer": "no"},
        ]
        self.medium_questions = [
            {"question": "What is the maximum speed for bikes in a bicycle lane?", "answer": "25 km/h"},
            {"question": "Are you allowed to hold your phone while biking?", "answer": "no"},
            {"question": "What color should your front bike light be?", "answer": "white"},
        ]
        self.hard_questions = [
            {"question": "What is the fine for cycling without lights at night?", "answer": "55 euros"},
            {"question": "What is the minimum age for a child to ride a bike on the road?", "answer": "12"},
            {"question": "What is the minimum tire pressure required for a road bike?", "answer": "4 bar"},
        ]
        # Initialize the unused questions for each difficulty level
        self.unused_easy = self.easy_questions.copy()
        self.unused_medium = self.medium_questions.copy()
        self.unused_hard = self.hard_questions.copy()

    def ask_question(self, difficulty):
        """ Ask a question based on the difficulty, ensuring no repetition. """
        if difficulty == 'easy':
            question_set = self.unused_easy
        elif difficulty == 'medium':
            question_set = self.unused_medium
        else:
            question_set = self.unused_hard

        # If all questions in the current difficulty level have been asked, reset the pool
        if not question_set:
            print(f"\nAll {difficulty} questions have been used. Re-populating the question pool.")
            if difficulty == 'easy':
                self.unused_easy = self.easy_questions.copy()
                question_set = self.unused_easy
            elif difficulty == 'medium':
                self.unused_medium = self.medium_questions.copy()
                question_set = self.unused_medium
            else:
                self.unused_hard = self.hard_questions.copy()
                question_set = self.unused_hard

        # Pick a random question from the unused questions and remove it from the set
        question = np.random.choice(question_set)
        question_set.remove(question)
        return question

# Integrate the biking quiz into the interactive game
class InteractiveBikingQuizGame:
    def __init__(self, agent, quiz):
        self.agent = agent
        self.env = agent.env  # Use the same environment as the agent
        self.quiz = quiz  # Biking quiz instance
        self.current_state = 0  # Start as a beginner
        self.score = 0  # Track the user's score

    def get_user_answer(self, question, answer):
        """ Ask the user the actual question and check their answer. """
        print(f"\nQuestion: {question}")
        user_answer = input("Your answer: ").strip().lower()

        if user_answer == answer.lower():
            return 1  # Correct answer
        else:
            return 0  # Incorrect answer

    def play_round(self):
        """ Play one round of the quiz, where the AI chooses the difficulty. """
        difficulty = self.agent.choose_action(self.current_state)
        print(f"\nPresenting a {difficulty} question.")

        # Get a question from the biking quiz
        question_data = self.quiz.ask_question(difficulty)
        question = question_data["question"]
        answer = question_data["answer"]

        # Get the user's answer
        user_correct = self.get_user_answer(question, answer)

        # Get the reward and new state from the environment
        reward, new_state, done = self.env.step(difficulty)

        # Update the agent's Q-table based on the results
        self.agent.update_q_table(self.current_state, difficulty, reward, new_state)

        # Move to the new state
        self.current_state = new_state
        self.score += user_correct  # Update score based on the user's correct answers

        if done:
            print("Congratulations! You've reached the advanced level.")
            return True  # End the game if the advanced level is reached
        return False  # Continue playing otherwise

    def play(self):
        """ Run the quiz until the user reaches the terminal state (advanced). """
        game_over = False
        round_num = 1

        while not game_over:
            print(f"\n--- Round {round_num} ---")
            game_over = self.play_round()
            round_num += 1

        print(f"Game Over! Your final score is {self.score}.")

# Main entry point for the interactive biking quiz
if __name__ == "__main__":
    # Initialize the environment and agent
    env = BikingQuizEnv()
    agent = QLearningAgent(env, learning_rate=0.1, discount_factor=0.9, epsilon=0.01)  # Lower epsilon for more exploitation

    # Load the trained Q-table
    try:
        q_table_loaded = np.load('trained_q_table.npy')
        agent.env.q_table = q_table_loaded  # Load the Q-table into the agent's environment
        print("Q-table loaded successfully!")
    except FileNotFoundError:
        print("Trained Q-table not found! Please train the agent first.")

    # Create a quiz instance with biking questions
    quiz = BikingQuiz()

    # Run the interactive quiz with real questions about biking in the Netherlands
    interactive_quiz_game = InteractiveBikingQuizGame(agent, quiz)
    interactive_quiz_game.play()