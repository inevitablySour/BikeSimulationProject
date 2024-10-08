# 2D Biking Simulation Game

## Project Overview
This project is a 2D biking simulation game focused on helping beginners learn the rules of biking and improve their skills in a fun, interactive environment. The game provides real-time feedback to players and tracks their progress, helping them improve over time. The goal is to create an educational tool that promotes healthy and safe biking practices.

## Features
- Interactive Tutorials: Real-time biking rule tutorials.
- AI-Driven Feedback: Players get immediate feedback when they make mistakes (e.g., running a red light, not signaling a turn).
- Progress Tracking: Tracks the player's performance and suggests areas for improvement.
- 2D Graphics: Simple 2D world with customizable biking levels.

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
- Arcade: Used for creating the 2D game engine, managing graphics, inputs, and game logic.
- Pillow: Used for handling and manipulating game assets like images and sprites.
- Pygame: An alternative library for handling 2D game creation and managing game loops.

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

- Arcade
- Pillow
- Pygame

Run the following command in your terminal or command prompt:

```terminal
pip install arcade pillow pygame
```

#### 2. Special Instructions for Pillow

If you encounter an error while installing Pillow, follow the additional instructions below based on your operating system.

### For macOS Users

1. Install Xcode Command Line Tools:

   ```terminal
   xcode-select --install
   ```

1. Install Homebrew (if not already installed):

   ```terminal
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   
2. Install required dependencies via Homebrew:

   ```terminal
   brew install libjpeg libtiff little-cms2
   ```

3. Reinstall Pillow:

   ```terminal
   pip install Pillow
   ```

### For Windows Users

1. Install Windows Build Tools:

   ```terminal
   npm install -g windows-build-tools
   ```

   (Note: This requires Node.js to be installed. If you don’t have Node.js, you can install it from https://nodejs.org)
   
2. Reinstall Pillow:

   ```terminal
   pip install --no-cache-dir --force-reinstall Pillow
   ```
   
If you encounter further issues, try installing an older version of Pillow:

```terminal
pip install Pillow==8.4.0
```

## How to Run the Project

1. After successfully installing the libraries, you can run the game using:

   ```terminal
   python main.py
   ```
