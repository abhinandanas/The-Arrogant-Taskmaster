# The Arrogant Taskmaster

## Idea Behind the Project
The goal of this project was to build a highly creative, out-of-the-box productivity application that actively bullies the user into completing their tasks. Instead of standard reminders, "The Arrogant Taskmaster" uses dynamic, context-aware insults based on the type of task entered (e.g., studying, coding, going to the gym). It utilizes a background threading system to trap the user in an escalating loop of aggressive notifications and forces them through a sarcastic, multi-step interrogation process before allowing them to mark a task as "Done." It turns a mundane utility into a comedic, interactive experience.

## Features
- **Context-Aware Roasts:** The application parses task names for keywords (like "study," "code," or "clean") and generates tailored insults based on the user's failures in those specific areas.
- **Escalating Harassment Loop:** Tasks trigger a background thread that traps the user in a `while` loop, firing increasingly aggressive desktop notifications until the task is marked complete.
- **The "Are You Sure?" Interrogation:** Marking a task as "Done" requires the user to survive a multi-step popup interrogation questioning their integrity before the task is actually removed from the active list.
- **Modern Dark Mode UI:** Built with CustomTkinter to look sleek and premium, heavily contrasting the hostile nature of the application.

## Technologies Used
- **Python:** Core application logic and background threading.
- **CustomTkinter:** Modern UI framework for building the dark mode desktop window.
- **Plyer:** Integration for native Windows/macOS desktop notifications.
- **Tkinter (messagebox):** Implementation of the interactive interrogation popups.

## Prerequisites
To run this application, you will need Python installed on your machine. You will also need to install the required external libraries.

```bash
pip install customtkinter plyer
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/abhinandanas/The-Arrogant-Taskmaster.git
cd The-Arrogant-Taskmaster
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python main.py
```

## How to Use

1. Add a task in the input field
2. Get insulted by notifications every 15 seconds
3. Click "Done?" to complete (if you can handle the interrogation)
4. Use "Stop" to stop individual task notifications
5. Use "Stop All" to stop all notifications

## Warning

This app is intentionally rude and passive-aggressive. Use at your own risk of hurt feelings.

## License

MIT License - Feel free to fork and make it even more insulting.