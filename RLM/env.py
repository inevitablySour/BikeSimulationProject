import random

class BikingQuizEnv:
    def __init__(self):
        # Define different levels and difficulties for questions
        self.levels = ["beginner", "intermediate", "advanced"]
        self.difficulties = ["easy", "medium", "hard"]
        self.questions = {
            "beginner": {
                "easy": ["Beginner Easy Q1", "Beginner Easy Q2"],
                "medium": ["Beginner Medium Q1", "Beginner Medium Q2"],
                "hard": ["Beginner Hard Q1", "Beginner Hard Q2"]
            },
            "intermediate": {
                "easy": ["Intermediate Easy Q1", "Intermediate Easy Q2"],
                "medium": ["Intermediate Medium Q1", "Intermediate Medium Q2"],
                "hard": ["Intermediate Hard Q1", "Intermediate Hard Q2"]
            },
            "advanced": {
                "easy": ["Advanced Easy Q1", "Advanced Easy Q2"],
                "medium": ["Advanced Medium Q1", "Advanced Medium Q2"],
                "hard": ["Advanced Hard Q1", "Advanced Hard Q2"]
            }
        }
        self.state = None

    def reset(self, level="beginner", difficulty="easy"):
        """ Reset to the initial question level and difficulty """
        self.state = (level, difficulty)
        return self.state

    def get_question(self):
        """ Retrieve a question based on the current state (level and difficulty) """
        level, difficulty = self.state
        return random.choice(self.questions[level][difficulty])

    def step(self, correct):
        """ Transition state based on whether the answer is correct """
        level, difficulty = self.state
        base_reward = 10 if correct else -5

        if level == "advanced" and difficulty == "hard" and correct:
            reward = base_reward + 5  # Extra reward for advanced-hard correct answers
        elif level == "intermediate" and difficulty == "medium" and correct:
            reward = base_reward + 3  # Smaller reward bump for intermediate-medium
        else:
            reward = base_reward

        if correct:
            if difficulty == "easy":
                self.state = (level, "medium")
            elif difficulty == "medium":
                self.state = (level, "hard")
            else:
                next_level_index = min(self.levels.index(level) + 1, len(self.levels) - 1)
                self.state = (self.levels[next_level_index], "easy")
        else:
            if difficulty == "hard":
                self.state = (level, "medium")
            elif difficulty == "medium":
                self.state = (level, "easy")
            else:
                prev_level_index = max(self.levels.index(level) - 1, 0)
                self.state = (self.levels[prev_level_index], "hard")

        return self.state, reward