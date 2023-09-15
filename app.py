import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Variable Timer")
        self.root.geometry("600x200")  # Set initial window size
        
        # Create frames for organizing widgets
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # Initial Duration Entry
        self.initial_duration_label = tk.Label(input_frame, text="Initial Duration (seconds):")
        self.initial_duration_label.grid(row=0, column=0, padx=10)
        
        self.initial_duration_entry = tk.Entry(input_frame)
        self.initial_duration_entry.grid(row=0, column=1)
        
        # Acceleration Entry
        self.acceleration_label = tk.Label(input_frame, text="Acceleration (default is 0):")
        self.acceleration_label.grid(row=1, column=0, padx=10)
        
        self.acceleration_entry = tk.Entry(input_frame)
        self.acceleration_entry.grid(row=1, column=1)
        
        # Start Button
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Pause Button
        self.pause_button = tk.Button(button_frame, text="Pause", state=tk.DISABLED, command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=5)
        
        # Cancel Button
        self.cancel_button = tk.Button(button_frame, text="Cancel", state=tk.DISABLED, command=self.cancel_timer)
        self.cancel_button.grid(row=0, column=2, padx=5)
        
        # Timer Label
        self.timer_label = tk.Label(root, text="Timer: 0 seconds", font=("Helvetica", 18))
        self.timer_label.pack(pady=10)
        
        # Initialize variables
        self.duration = 0
        self.initial_duration = 0
        self.acceleration = 0
        self.paused = False
        self.running = False

    def start_timer(self):
        if not self.running:
            try:
                self.duration = int(self.initial_duration_entry.get())
                self.initial_duration = self.duration
                self.acceleration = float(self.acceleration_entry.get())
                if self.duration <= 0 or self.acceleration < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Invalid input")
                return

            self.running = True
            self.pause_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.DISABLED)
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()

    def run_timer(self):
        while self.duration > 0 and self.running:
            if not self.paused:
                self.duration -= 1
                self.timer_label.config(text=f"Timer: {self.duration} seconds")
                self.check_notifications()
                time.sleep(1 / (1 + self.acceleration * ((self.initial_duration - self.duration) - self.initial_duration / 2) / self.initial_duration))
        if self.running:
            self.running = False
            self.timer_label.config(text="Timer: 0 seconds")
            self.pause_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)
            messagebox.showinfo("Timer Finished", "Timer has finished!")

    def check_notifications(self):
        if self.duration == 300:  # 5 minutes left
            notification_text = "5 minutes remaining."
        elif self.duration == 60:  # 1 minute left
            notification_text = "1 minute remaining."
        else:
            return
        
        print(f"Sending notification: {notification_text}")
        os.system(f"osascript -e 'display notification \"{notification_text}\"'")
            
    def pause_timer(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")

    def cancel_timer(self):
        if self.running:
            self.running = False
            self.timer_thread.join()
            self.timer_label.config(text="Timer: 0 seconds")
            self.pause_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
