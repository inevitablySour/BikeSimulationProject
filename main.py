import tkinter as tk
from tkinter import messagebox
import random
from agent import QLearningAgent
from biking_rules import questions

class BikingQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maastricht Biking Quiz")
        self.agent = QLearningAgent(actions=["easy", "medium", "hard"], q_table_path="trained_q_table_new.npy")
        self.level = "beginner"
        self.difficulty = "easy"
        self.score = 0
        self.state = (self.level, self.difficulty)
        self.question_data = None

        # Setup GUI
        self.question_label = tk.Label(root, text="", wraplength=400)
        self.question_label.pack(pady=20)

        self.options = []
        for i in range(3):  # assuming 3 multiple-choice options per question
            option_button = tk.Button(root, text="", width=50, command=lambda idx=i: self.check_answer(idx))
            option_button.pack(pady=5)
            self.options.append(option_button)

        self.load_question()

    def load_question(self):
        # Select the best action based on AI
        action = self.agent.select_action(self.state)
        self.difficulty = action
        self.question_data = random.choice(questions[self.level][self.difficulty])

        # Update GUI with new question and options
        self.question_label.config(text=self.question_data["question"])
        for idx, option in enumerate(self.question_data["options"]):
            self.options[idx].config(text=option)

    def check_answer(self, selected_idx):
        selected_answer = self.question_data["options"][selected_idx]
        if selected_answer == self.question_data["answer"]:
            self.score += 10
            messagebox.showinfo("Correct", "That's correct!")
        else:
            self.score -= 5
            messagebox.showerror("Incorrect", f"The correct answer was: {self.question_data['answer']}")

        # Adjust state based on performance
        if self.score >= 30 and self.level == "beginner":
            self.level = "intermediate"
        elif self.score >= 60 and self.level == "intermediate":
            self.level = "advanced"

        self.state = (self.level, self.difficulty)
        self.load_question()

if __name__ == "__main__":
    root = tk.Tk()
    quiz_app = BikingQuizGUI(root)
    root.mainloop()