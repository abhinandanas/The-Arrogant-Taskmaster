import customtkinter as ctk
import time
import threading
from plyer import notification
import random
from tkinter import messagebox

# --- 1. SETUP UI ---
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

app = ctk.CTk()  
app.geometry("550x700")
app.title("The Arrogant Taskmaster")

active_tasks = {}
task_reminders = {} # Count how many times the user has been insulted for each task
task_meters = {} # Store the AnalogMeter widget for each task

# --- 2. THE ARROGANT DICTIONARY ---
# Categorized insults that target specific life failures
# --- 2. THE EXPANDED ARROGANT DICTIONARY ---
ROAST_DICTIONARY = {
    "study": [
        "Still haven't started '{}'? Bold strategy for someone with your GPA.",
        "Your future self is currently working at a fast-food joint because of '{}'.",
        "Books don't bite, but failure does. Open '{}' already.",
        "Is '{}' too complex for your tiny brain? Should I find a picture book version?",
        "Watching you ignore '{}' is like watching a train wreck in slow motion.",
        "I guess mediocrity is your life goal. Keep ignoring '{}'.",
        "Your parents' disappointment is manifesting. Do '{}'."
    ],
    "read": [
        "TikTok completely melted your attention span. Let's see if you can still '{}'.",
        "Words are hard, I know. But try to do '{}' anyway.",
        "Reading requires actual brain activity, which explains why you're avoiding '{}'.",
        "Are you waiting for the movie adaptation of '{}'?",
        "Just look at the pictures if '{}' is too difficult for you."
    ],
    "write": [
        "ChatGPT writes better than you ever will. But go ahead and try to '{}'.",
        "Staring blankly at a blinking cursor won't complete '{}'.",
        "I'm sure your draft for '{}' will be a masterpiece of grammatical errors.",
        "Procrastinating on '{}' won't make you more creative. It just makes you lazier.",
        "Just type some words. It’s going to be garbage anyway, so finish '{}'."
    ],
    "clean": [
        "Are you waiting for the mold to become sentient? Go do '{}'.",
        "I can smell your lack of discipline from the CPU. Finish '{}'.",
        "Your room is a biohazard. '{}' is the least of your concerns, but start there.",
        "Evolution took millions of years, yet here you are, refusing to '{}'.",
        "The bacteria in your room are more productive than you. Do '{}'.",
        "Pigs keep cleaner pens than this. Start '{}' before the health department arrives."
    ],
    "code": [
        "Still debugging '{}'? Just delete the repo, it's embarrassing.",
        "StackOverflow is tired of your questions about '{}'.",
        "Your code for '{}' probably looks like a cat walked across the keyboard.",
        "Imagine being a programmer and being defeated by '{}'. Pathetic.",
        "If bugs were currency, you'd be a billionaire for '{}'.",
        "Did you really push that to main? Fix '{}' before someone sees it."
    ],
    "work": [
        "Do you actually want to keep your job? Finish '{}'.",
        "Minimum effort yields minimum wage. Do '{}'.",
        "Your boss is already drafting your termination letter. Might want to do '{}'.",
        "You're the reason they have to micromanage people. Finish '{}'."
    ],
    "email": [
        "Just type 'Hope this finds you well' and hit send on '{}'. Stop overthinking.",
        "They are going to skim it anyway. Stop crying and do '{}'.",
        "Drafting '{}' isn't defusing a bomb. Just press send, coward."
    ],
    "call": [
        "They are definitely ignoring your calls anyway. But try doing '{}'.",
        "Social interaction is terrifying for you, I get it. But go '{}'.",
        "Avoidance isn't a personality trait. Do '{}' and stop being a coward.",
        "They'll probably hang up, but go ahead and '{}'.",
        "Are you going to practice what you'll say in the mirror first? Just do '{}'."
    ],
    "eat": [
        "Ordering takeout again instead of '{}'? Your arteries are screaming.",
        "Microwaving pizza rolls doesn't count as cooking. Go do '{}'.",
        "You're built like a soggy noodle. Go '{}' and get some actual nutrients.",
        "Eating junk food won't fill the void of your uncompleted tasks. Do '{}'."
    ],
    "water": [
        "You are essentially a dried-up houseplant with complex emotions. Do '{}'.",
        "Your kidneys are begging for mercy. Do '{}'.",
        "Dehydration is a choice, and you're making a stupid one. Do '{}'."
    ],
    "gym": [
        "The only thing you're 'working out' is my patience. Do '{}'.",
        "Gravity is winning. Go do '{}'.",
        "You're making the bench press look like a nap. Finish '{}'.",
        "You've been paying for that membership for 6 months. Go '{}'.",
        "Your muscles are evaporating as we speak. Go '{}'."
    ],
    "sleep": [
        "You're tired from doing absolutely nothing all day. But fine, do '{}'.",
        "Your sleep schedule is more ruined than your career prospects. Do '{}'.",
        "Closing your eyes won't make your responsibilities disappear. Do '{}'."
    ],
    "default": [ 
        "I am physically ill looking at '{}' still on this list.",
        "Do you take pride in being a professional procrastinator of '{}'?",
        "Every second you ignore '{}', your IQ drops by 5 points.",
        "Just delete the app. You clearly aren't capable of '{}'.",
        "If laziness were an Olympic sport, you'd be a gold medalist for '{}'.",
        "My fans are spinning faster just to deal with your incompetence on '{}'.",
        "I've seen slugs move faster than you're moving on '{}'.",
        "Your potential is a myth. '{}' is the reality.",
        "I calculate a 0% chance of you actually completing '{}'.",
        "I'd ask you to hurry up with '{}', but I know you don't respect my time.",
        "You are the bottleneck in your own life. Finish '{}'."
    ]
}

ARROGANT_FOLLOW_UPS = [
    "ARE YOU STILL THERE? '{}' is rotting!",
    "I'm actually impressed by how much you don't care about '{}'.",
    "Hey loser, '{}' isn't going to fix itself.",
    "I'm bored. You're boring. Do '{}' and prove me wrong.",
    "Is your 'Enter' key broken, or are you just failing at '{}' again?",
    "I'm literally a piece of software and I have more drive than you. Do '{}'.",
    "Did you fall asleep staring at the screen? '{}' is still waiting.",
    "I'm updating my database: User is entirely useless at '{}'.",
    "Blink twice if you need me to do '{}' for you. Oh wait, I can't. You have to.",
    "You have the audacity to sit there while '{}' is incomplete?"
]

def get_insult(task_name):
    task_lower = task_name.lower()
    # Check for keywords
    for keyword, roasts in ROAST_DICTIONARY.items():
        if keyword in task_lower:
            return random.choice(roasts).format(task_name)
    # Default insult if no keyword matches
    return random.choice(ROAST_DICTIONARY["default"]).format(task_name)

def annoy_user_loop(task_name, wait_time=15):
    """The background loop that repeatedly fires notifications."""
    while active_tasks.get(task_name) == True:
        time.sleep(wait_time)
        
        if active_tasks.get(task_name) == True:
            task_reminders[task_name] += 1
            
            # Update meter safely on main thread
            def update_meter(t=task_name, r=task_reminders[task_name]):
                if t in task_meters and active_tasks.get(t):
                    # 10% per notification
                    task_meters[t].set_pressure(r * 0.1)
            app.after(0, update_meter)
            
            # Level 1: Standard Arrogance
            if task_reminders[task_name] == 1:
                title = "⚠️ INCOMPETENCE DETECTED"
                msg = get_insult(task_name)
            
            # Level 2: Personal Attacks
            elif task_reminders[task_name] == 2:
                title = "🛑 STILL NOTHING?"
                msg = random.choice(ARROGANT_FOLLOW_UPS).format(task_name)
            
            # Level 3: Pure Arrogance
            else:
                title = "💀 GIVE UP ALREADY"
                msg = f"This is reminder #{task_reminders[task_name]}. You are a failure at {task_name}. Just quit."

            notification.notify(
                title=title,
                message=msg,
                app_name="Arrogant Taskmaster",
                timeout=8 
            )

class AnalogMeter(ctk.CTkFrame):
    def __init__(self, master, size=100, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.size = size
        
        # Determine canvas size (width=size, height=size/2 + some padding for text)
        canvas_width = size
        canvas_height = int(size / 2) + 20
        
        self.canvas = ctk.CTkCanvas(self, width=canvas_width, height=canvas_height, 
                                    bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.margin = 10
        self.bbox_coords = (self.margin, self.margin, self.size - self.margin, self.size - self.margin)
        
        # Background track (gray)
        self.canvas.create_arc(*self.bbox_coords, start=0, extent=180, 
                               style="arc", outline="#444444", width=8)
        
        # Foreground track (starts empty)
        self.fg_arc = self.canvas.create_arc(*self.bbox_coords, start=180, extent=0, 
                                             style="arc", outline="#00cc00", width=8)
                                             
        # Text label for percentage
        self.text_id = self.canvas.create_text(canvas_width / 2, canvas_height - 10, 
                                               text="0%", fill="white", font=("Helvetica", 14, "bold"))
        
    def set_pressure(self, value):
        # Validate value
        value = max(0.0, min(1.0, value))
        
        # Calculate extent (negative to draw clockwise from 180)
        extent = -int(value * 180)
        
        # Determine color
        if value <= 0.3:
            color = "#00cc00" # green
        elif value <= 0.7:
            color = "#ff9900" # orange
        else:
            color = "#ff3333" # red
            
        # Update canvas
        self.canvas.itemconfig(self.fg_arc, extent=extent, outline=color)
        self.canvas.itemconfig(self.text_id, text=f"{int(value * 100)}%", fill=color)

# --- 3. UI LAYOUT ---
header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(pady=(30, 10), fill="x", padx=30)

title_label = ctk.CTkLabel(header_frame, text="The Arrogant Taskmaster", font=("Helvetica", 28, "bold"), text_color="#ff474c")
title_label.pack()

subtitle_label = ctk.CTkLabel(header_frame, text="I'm smarter than you, and I know you won't do these.", font=("Helvetica", 14, "italic"), text_color="gray")
subtitle_label.pack(pady=(5, 15))

input_frame = ctk.CTkFrame(app, fg_color="#2b2b2b", corner_radius=15)
input_frame.pack(pady=10, padx=30, fill="x")

task_entry = ctk.CTkEntry(input_frame, placeholder_text="Type a task you'll eventually ignore...", width=320, height=50, font=("Helvetica", 16), border_width=0)
task_entry.pack(side="left", padx=(20, 5), pady=20)

task_list_frame = ctk.CTkScrollableFrame(app, width=480, height=400, corner_radius=15, fg_color="#1e1e1e")
task_list_frame.pack(pady=20, padx=30, fill="both", expand=True)

# --- 4. THE INTERROGATION LOGIC ---
def add_task():
    task = task_entry.get().strip()
    
    if task != "" and task not in active_tasks:
        active_tasks[task] = True
        task_reminders[task] = 0
        
        task_item_frame = ctk.CTkFrame(task_list_frame, fg_color="#2b2b2b", corner_radius=10)
        task_item_frame.pack(fill="x", pady=8, padx=10)

        task_label = ctk.CTkLabel(task_item_frame, text=f"📍 {task}", font=("Helvetica", 16, "bold"))
        task_label.pack(side="left", padx=20, pady=20)

        # Create meter
        meter = AnalogMeter(task_item_frame, size=80)
        meter.pack(side="left", padx=10, pady=5)
        task_meters[task] = meter

        def try_complete_task(t=task, frame=task_item_frame):
            # FIRST INTERROGATION
            if messagebox.askyesno("Wait a minute...", f"Did you actually do '{t}', or are you lying to a computer program?"):
                # SECOND INTERROGATION
                if messagebox.askyesno("Seriously?", "Are you SURE? I'll know if you're lying. Your lack of progress is evident."):
                    # THIRD INTERROGATION (Final insult)
                    messagebox.showinfo("Fine.", "I'll remove it. But we both know you probably did a mediocre job.")
                    frame.destroy() 
                    active_tasks[t] = False
                    if t in task_meters:
                        del task_meters[t]
                else:
                    messagebox.showwarning("Caught You.", "I knew it. Go back to your hole and finish it.")
            else:
                messagebox.showwarning("Honesty is a start.", "At least you admit you're lazy. Now go do it.")

        def stop_notifications(t=task, frame=task_item_frame):
            active_tasks[t] = False
            if t in task_meters:
                del task_meters[t]
            frame.destroy()
            messagebox.showinfo("Stopped", f"Fine. I'll stop nagging you about '{t}'. But you're still a failure.")

        stop_button = ctk.CTkButton(task_item_frame, text="Stop", width=70, height=40,
                                   fg_color="#666666", hover_color="#888888",
                                   font=("Helvetica", 12, "bold"), command=stop_notifications)
        stop_button.pack(side="right", padx=5)

        done_button = ctk.CTkButton(task_item_frame, text="Done?", width=90, height=40, 
                                    fg_color="#3a3a3a", hover_color="#ff474c", 
                                    font=("Helvetica", 13, "bold"), command=try_complete_task)
        done_button.pack(side="right", padx=15)
        
        threading.Thread(target=annoy_user_loop, args=(task, 15), daemon=True).start()
        task_entry.delete(0, 'end')

add_button = ctk.CTkButton(input_frame, text="Add", command=add_task, width=100, height=50, font=("Helvetica", 16, "bold"), fg_color="#ff474c", hover_color="#cc0000")
add_button.pack(side="right", padx=(5, 10), pady=20)

def stop_all_tasks():
    for task in list(active_tasks.keys()):
        active_tasks[task] = False
    # Clear the task list display
    for widget in task_list_frame.winfo_children():
        widget.destroy()
    messagebox.showinfo("All Stopped", "Fine. I'll stop all notifications. You're hopeless anyway.")

stop_all_button = ctk.CTkButton(input_frame, text="Stop All", command=stop_all_tasks, width=80, height=50, font=("Helvetica", 14, "bold"), fg_color="#666666", hover_color="#888888")
stop_all_button.pack(side="right", padx=(5, 20), pady=20)

app.bind('<Return>', lambda event: add_task())
app.mainloop()