import json
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

class QuizAnalysis:
    def __init__(self, data_file="Quiz/quiz_results.json"):
        self.data_file = data_file
        self.all_results = []

        self.load_data()

    def load_data(self):
        """Load all quiz results from the JSON file."""
        try:
            with open(self.data_file, "r") as f:
                for line in f:
                    session_results = json.loads(line)
                    self.all_results.extend(session_results)
        except FileNotFoundError:
            print("Data file not found. Please ensure the data file exists.")

    def analyze_all_data(self):
        """Aggregate data for all users and plot incorrect answers by tag."""
        incorrect_by_tag = Counter()

        for entry in self.all_results:
            if not entry["correct"]:
                incorrect_by_tag.update(entry["tags"])

        tags = list(incorrect_by_tag.keys())
        counts = list(incorrect_by_tag.values())

        plt.figure(figsize=(10, 6))
        plt.bar(tags, counts, color="red")
        plt.title("Aggregate Incorrect Answers by Tag (All Users)")
        plt.xlabel("Tag")
        plt.ylabel("Number of Incorrect Answers")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()  # Adjust layout to fit labels
        plt.show()

    def export_to_excel(self, output_file="Quiz/quiz_results.xlsx"):
        """Export quiz results to an Excel file with separate tables for detailed results and summary by tag."""
        if not self.all_results:
            print("No data available to export.")
            return

        data = {
            "User ID": [entry["user_id"] for entry in self.all_results],
            "Question": [entry["question"] for entry in self.all_results],
            "Tags": [", ".join(entry["tags"]) for entry in self.all_results],
            "Correct": [1 if entry["correct"] else 0 for entry in self.all_results],
            "Incorrect": [0 if entry["correct"] else 1 for entry in self.all_results]
        }
        detailed_df = pd.DataFrame(data)

        tag_counts = {}
        for entry in self.all_results:
            for tag in entry["tags"]:
                if tag not in tag_counts:
                    tag_counts[tag] = {"correct": 0, "incorrect": 0}
                if entry["correct"]:
                    tag_counts[tag]["correct"] += 1
                else:
                    tag_counts[tag]["incorrect"] += 1

        summary_data = {
            "Tag": list(tag_counts.keys()),
            "Correct Answers": [tag_counts[tag]["correct"] for tag in tag_counts],
            "Incorrect Answers": [tag_counts[tag]["incorrect"] for tag in tag_counts]
        }
        summary_df = pd.DataFrame(summary_data)

        with pd.ExcelWriter(output_file) as writer:
            detailed_df.to_excel(writer, sheet_name="Detailed Results", index=False)
            summary_df.to_excel(writer, sheet_name="Summary by Tag", index=False)
        print(f"Data exported to {output_file} successfully.")

# Usage example
if __name__ == "__main__":
    analysis = QuizAnalysis()
    analysis.analyze_all_data()
    analysis.export_to_excel()