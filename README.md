# Biking Rules Quiz and Analysis Tool

## Project Overview
This project is a multiple-choice biking rules quiz designed to help users learn and reinforce their understanding of biking regulations, specifically focusing on the rules in Maastricht. The quiz provides immediate feedback and tracks each user’s progress, adjusting the difficulty level based on performance. After completing the quiz, users receive a personalized analysis of their strengths and weaknesses. All results are logged for further analysis and can be exported for review.

## Features
- Adaptive Difficulty: The quiz adjusts question difficulty based on the user’s performance, moving through beginner, intermediate, and advanced levels.
- Real-Time Feedback: Users receive immediate feedback on each question, with correct/incorrect messages shown in the same window.
- Progress Tracking: Tracks progress with a visual progress bar and adjusts the user’s level based on cumulative score.
- Detailed Analysis: Provides a summary of incorrectly answered questions by category, helping users focus on areas that need improvement. 
- Data Export: Exports quiz data, including correct and incorrect answers by category, to an Excel file for comprehensive analysis.


## Git Installation Instructions

### For Windows Users

1. Go to the Git website: https://git-scm.com/
2. Download the Git installer by clicking on "Download for Windows."
3. Once the download is complete, open the installer and follow the setup wizard.
   - Choose default options unless you have specific preferences.
   - Make sure to check the option that adds Git to your system PATH so you can run Git commands from the command prompt.
4. Verify installation by opening Command Prompt and running:

   ```terminal
   git --version
   ```

### For macOS Users

1. Open the terminal.
2. Run the following command to install Git via Xcode Command Line Tools:

   ```terminal
   xcode-select --install
   ```

3. Confirm the installation by running:

   ```terminal
   git --version
   ```

Alternatively, you can install Git using Homebrew if you have it installed:

   ```terminal
   brew install git
   ```

## Libraries Used
- tkinter: Provides the GUI framework for the quiz and analysis windows.
- matplotlib: Generates charts for the analysis of quiz performance.
- pandas: Exports quiz data to an Excel file for further analysis.

## Installation Instructions

### Prerequisites
Make sure you have Python 3.6+ installed. You can verify your Python version by running the following command:

```terminal
python --version
```

If you don't have Python installed, you can download it from the official Python website: https://www.python.org/downloads/

### Installation Steps

#### 1. Install Libraries

For this project, you will need to install the following Python libraries:

- tkinter
- matplotlib
- pandas

Run the following command in your terminal or command prompt to install the necessary libraries:

```terminal
pip install matplotlib pandas
```

#### 2. Special Instructions for macOS Users

If you encounter issues installing matplotlib, you may need to install additional dependencies:


1. Install Xcode Command Line Tools:

   ```terminal
   xcode-select --install
   ```

2. Install Homebrew (if not already installed):

   ```terminal
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   
3. Install required dependencies via Homebrew:

   ```terminal
   brew install pkg-config freetype
   ```

4. Reinstall Matplotlib:

   ```terminal
   pip install matplotlib
   ```

### Analysis and Data Export

1. ##### Automatic Analysis:

    Upon quiz completion, a new window opens, displaying a chart with a breakdown of incorrect answers by topic. This allows users to identify specific areas for improvement.
   
2. ##### Exporting to Excel:

    The quiz results are stored in a JSON file and can be exported to an Excel file. The export includes:

   - A detailed table with each question answered, categorized by correct and incorrect answers.
   - A summary table that lists each topic alongside the number of correct and incorrect responses associated with it.
   
If you encounter further issues, try installing an older version of Pillow:

```terminal
pip install Pillow==8.4.0
```

## How to Run the Project

1. After successfully installing the libraries, you can run the game using:

   ```terminal
   python main.py
   ```
