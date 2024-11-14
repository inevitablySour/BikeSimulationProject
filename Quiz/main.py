import tkinter as tk
from tkinter import ttk
import random
import json
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from RLM.agent import QLearningAgent


with open('Quiz/biking_questions.json', 'r') as f:
    questions = json.load(f)

class BikingQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maastricht Biking Quiz")

        self.user_id = self.get_next_user_id()
        self.agent = QLearningAgent(actions=["easy", "medium", "hard"], q_table_path="RLM/trained_q_table.npy")
        self.level = "beginner"
        self.difficulty = "easy"
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.start_time = time.time()
        self.question_number = 1
        self.state = (self.level, self.difficulty)
        self.question_data = None
        self.results = []


        self.setup_quiz_interface()
        self.load_question()

    def get_next_user_id(self):
        """Determine the next available User ID by counting existing entries in the JSON file."""
        try:
            with open("quiz_results.json", "r") as f:
                return sum(1 for _ in f) + 1
        except FileNotFoundError:
            return 1

    def setup_quiz_interface(self):
        """Set up the main quiz interface."""
        self.info_label = tk.Label(self.root, text="", font=("Arial", 12), fg="yellow")
        self.info_label.pack(pady=10)

        self.question_label = tk.Label(self.root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.options = []
        for i in range(3):
            option_button = tk.Button(self.root, text="", width=50, command=lambda idx=i: self.check_answer(idx))
            option_button.pack(pady=(3, 2))
            self.options.append(option_button)

        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"))
        self.feedback_label.pack(pady=5)

        self.progress_label = tk.Label(self.root, text="Progress to Next Level", font=("Arial", 10))
        self.progress_label.pack(pady=(5, 0))

        self.progress_bar = ttk.Progressbar(self.root, length=400, maximum=30, mode='determinate')
        self.progress_bar.pack(pady=(5, 15))
        self.update_progress_bar()

    def update_info_label(self):
        """Update the information label with question number, difficulty, and user level."""
        self.info_label.config(text=f"Question: {self.question_number} | Level: {self.level.capitalize()} | Difficulty: {self.difficulty.capitalize()}")

    def update_progress_bar(self):
        """Update the progress bar based on the score and current level."""
        if self.level == "beginner":
            self.progress_bar['maximum'] = 30
            self.progress_bar['value'] = min(self.score, 30)
            self.progress_label.config(text="Progress to Next Level")
        elif self.level == "intermediate":
            self.progress_bar['maximum'] = 30
            self.progress_bar['value'] = min(self.score - 30, 30)
            self.progress_label.config(text="Progress to Next Level")
        elif self.level == "advanced" and self.score >= 90:
            self.show_congratulations()
        else:
            self.progress_bar['maximum'] = 30
            self.progress_bar['value'] = min(self.score - 60, 30)

    def load_question(self):
        """Load a question based on the AI-selected difficulty."""
        # Select the best action based on AI and update difficulty
        action = self.agent.select_action(self.state)
        self.difficulty = action

        # Update info label with the correct difficulty before displaying the question
        self.update_info_label()
        self.update_progress_bar()

        # Select a random question from the chosen difficulty level
        self.question_data = random.choice(questions[self.level][self.difficulty])

        # Display question and options
        self.question_label.config(text=self.question_data["question"])
        for idx, option in enumerate(self.question_data["options"]):
            self.options[idx].config(text=option)

        # Clear feedback label
        self.feedback_label.config(text="")

    def check_answer(self, selected_idx):
        """Check the selected answer and provide feedback."""
        selected_answer = self.question_data["options"][selected_idx]
        is_correct = selected_answer == self.question_data["answer"]
        if is_correct:
            self.score += 10
            self.correct_answers += 1
            self.show_feedback("Correct!", "lime")
        else:
            self.score -= 5
            self.incorrect_answers += 1
            self.show_feedback(f"Incorrect! The correct answer was: {self.question_data['answer']}", "red")

        self.results.append({
            "user_id": self.user_id,
            "question": self.question_data["question"],
            "correct": is_correct,
            "tags": self.question_data["tags"]
        })

        if self.score >= 60:
            self.level = "advanced"
        elif 30 <= self.score < 60:
            self.level = "intermediate"
        else:
            self.level = "beginner"

        self.state = (self.level, self.difficulty)
        self.question_number += 1

        self.root.after(1500, self.load_question)

    def show_feedback(self, message, color):
        """Show feedback in the same window and hide other elements, including the progress bar."""
        self.question_label.pack_forget()
        for option_button in self.options:
            option_button.pack_forget()
        self.progress_label.pack_forget()
        self.progress_bar.pack_forget()

        self.feedback_label.config(text=message, fg=color)
        self.feedback_label.pack()
        self.root.after(1500, self.restore_question_layout)

    def restore_question_layout(self):
        """Restore question, options, and progress bar after feedback is shown."""
        self.question_label.pack(pady=20)
        for option_button in self.options:
            option_button.pack(pady=(3, 2))
        self.feedback_label.pack_forget()

        self.progress_label.pack(pady=(5, 0))
        self.progress_bar.pack(pady=(5, 15))

    def show_congratulations(self):
        """Display a congratulations message with quiz statistics, save results, and show analysis."""
        for widget in self.root.winfo_children():
            widget.pack_forget()

        end_time = time.time()
        total_time = end_time - self.start_time
        minutes, seconds = divmod(total_time, 60)

        congrats_label = tk.Label(self.root, text="Congratulations!", font=("Arial", 24, "bold"), fg="green")
        congrats_label.pack(pady=20)

        stats_message = (
            f"You've completed the quiz!\n\n"
            f"Correct Answers: {self.correct_answers}\n"
            f"Incorrect Answers: {self.incorrect_answers}\n"
            f"Total Time: {int(minutes)} minutes and {int(seconds)} seconds"
        )
        stats_label = tk.Label(self.root, text=stats_message, font=("Arial", 14))
        stats_label.pack(pady=10)

        with open("quiz_results.json", "a") as f:
            json.dump(self.results, f)
            f.write("\n")

        self.show_analysis()

    def show_analysis(self):
        """Analyze the user's data and display a graph of incorrect answers by tag in a new window."""
        incorrect_by_tag = Counter()

        for entry in self.results:
            if not entry["correct"]:
                incorrect_by_tag.update(entry["tags"])

        tags = list(incorrect_by_tag.keys())
        counts = list(incorrect_by_tag.values())

        plot_window = tk.Toplevel(self.root)
        plot_window.title(f"Analysis for User ID {self.user_id}")

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(tags, counts, color="red")
        ax.set_title(f"Incorrect Answers by Tag for User ID {self.user_id}")
        ax.set_xlabel("Tag")
        ax.set_ylabel("Number of Incorrect Answers")
        ax.set_xticklabels(tags, rotation=45, ha="right")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    quiz_app = BikingQuizGUI(root)
    root.mainloop()