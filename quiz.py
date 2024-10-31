import numpy as np
from env import BikingQuizEnv
from agent import QLearningAgent

class BikingQuiz:
    def __init__(self):
        # Define question pools for each level and difficulty combination
        self.questions = {
            "beginner": {
                "easy": [
                    {"question": "Is it mandatory to use bike lights at night?", "answer": "yes"},
                    {"question": "Can you ride a bike on the sidewalk?", "answer": "no"},
                ],
                "medium": [
                    {"question": "Are bike helmets mandatory in the Netherlands?", "answer": "no"},
                    {"question": "Should you yield to pedestrians at crossings?", "answer": "yes"},
                ],
                "hard": [
                    {"question": "What color should your bike light be at the front?", "answer": "white"},
                    {"question": "What is the maximum speed in residential areas for bikes?", "answer": "30 km/h"},
                ],
            },
            "intermediate": {
                "easy": [
                    {"question": "Can you ride two abreast on Dutch bike paths?", "answer": "yes"},
                    {"question": "Is it allowed to overtake other cyclists?", "answer": "yes"},
                ],
                "medium": [
                    {"question": "What is the fine for using a phone while biking?", "answer": "140 euros"},
                    {"question": "Is there a designated side of the road for cyclists?", "answer": "yes"},
                ],
                "hard": [
                    {"question": "Are bike trailers allowed on highways?", "answer": "no"},
                    {"question": "How close to the curb should you cycle?", "answer": "1 meter"},
                ],
            },
            "advanced": {
                "easy": [
                    {"question": "Is cycling allowed in pedestrian zones?", "answer": "sometimes"},
                    {"question": "Can cyclists use car lanes if bike lanes are occupied?", "answer": "yes"},
                ],
                "medium": [
                    {"question": "Are e-bikes allowed on standard bike paths?", "answer": "yes"},
                    {"question": "What is the minimum age to operate an e-bike?", "answer": "16"},
                ],
                "hard": [
                    {"question": "What is the legal blood alcohol limit for cyclists?", "answer": "0.5‰"},
                    {"question": "What is the penalty for cycling under the influence?", "answer": "200 euros"},
                ],
            },
        }
        # Initialize unused question pools for each difficulty
        self.unused_questions = {level: {diff: q_set.copy() for diff, q_set in self.questions[level].items()} for level in self.questions}

    def ask_question(self, level, difficulty):
        """ Ask a question based on the user level and difficulty, ensuring no repetition. """
        question_set = self.unused_questions[level][difficulty]

        if not question_set:
            print(f"\nAll {difficulty} questions for {level} level have been used. Re-populating the question pool.")
            self.unused_questions[level][difficulty] = self.questions[level][difficulty].copy()
            question_set = self.unused_questions[level][difficulty]

        question = np.random.choice(question_set)
        question_set.remove(question)
        return question


class InteractiveBikingQuizGame:
    def __init__(self, agent, quiz):
        self.agent = agent
        self.env = agent.env
        self.quiz = quiz
        self.current_state = 0
        self.score = 0
        self.correct_streak = 0
        self.incorrect_streak = 0

    def get_user_answer(self, question, answer):
        """Ask the user the actual question and check their answer."""
        print(f"\nQuestion: {question}")
        user_answer = input("Your answer: ").strip().lower()
        return 1 if user_answer == answer.lower() else 0  # Correct answer

    def play_round(self):
        """Play one round of the quiz, where the AI chooses the difficulty."""
        difficulty = self.agent.choose_action(self.current_state)
        level_name = self.env.states[self.current_state]  # Get the level name

        print(f"Your current level is now: {level_name.capitalize()}")
        print(f"\nPresenting a {difficulty} question.")

        # Get a question from the biking quiz based on user level and difficulty
        question_data = self.quiz.ask_question(level_name, difficulty)
        question = question_data["question"]
        answer = question_data["answer"]

        # Check if the user answered correctly
        user_correct = self.get_user_answer(question, answer)

        # Update correct and incorrect streaks
        if user_correct:
            self.correct_streak += 1
            self.incorrect_streak = 0
            print("Correct!")
        else:
            self.correct_streak = 0
            self.incorrect_streak += 1
            print(f"Incorrect! The correct answer was: {answer}.")

        # Use streaks to manage level change sensitivity
        if self.correct_streak >= 2:  # Level up after 2 correct answers in a row
            reward, new_state, done = self.env.step(difficulty, correct=True)
            self.correct_streak = 0  # Reset streak after level change
        elif self.incorrect_streak >= 2:  # Level down after 2 incorrect answers in a row
            reward, new_state, done = self.env.step(difficulty, correct=False)
            self.incorrect_streak = 0  # Reset streak after level change
        else:
            reward, new_state, done = self.env.step(difficulty, correct=user_correct)

        # Update the agent's Q-table based on the results
        self.agent.update_q_table(self.current_state, difficulty, reward, new_state)

        # Update level and score
        previous_state = self.current_state
        self.current_state = new_state
        self.score += user_correct

        # Notify the user of a level change
        if self.current_state != previous_state:
            new_level_name = self.env.states[self.current_state]
            print(f"Your current level is now: {new_level_name.capitalize()}")

        if done:
            print("Congratulations! You've reached the advanced level.")
            return True
        return False

    def play(self):
        """Run the quiz until the user reaches the terminal state (advanced)."""
        game_over = False
        round_num = 1

        while not game_over:
            print(f"\n--- Round {round_num} ---")
            game_over = self.play_round()
            round_num += 1

        print(f"Game Over! Your final score is {self.score}.")

if __name__ == "__main__":
    env = BikingQuizEnv()
    agent = QLearningAgent(env, learning_rate=0.1, discount_factor=0.9, epsilon=0.01)

    try:
        q_table_loaded = np.load('trained_q_table.npy')
        agent.env.q_table = q_table_loaded
        print("Q-table loaded successfully!")
    except FileNotFoundError:
        print("Trained Q-table not found! Please train the agent first.")

    quiz = BikingQuiz()
    interactive_quiz_game = InteractiveBikingQuizGame(agent, quiz)
    interactive_quiz_game.play()