import tkinter as tk
from tkinter import messagebox
import json
import os

TASKS_FILE = "tasks.json"

class TaskScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("✅ Daily Task Scheduler")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="black")

        self.tasks = []
        self.task_widgets = []
        self.task_vars = []
        self.load_tasks()

        self.task_var = tk.StringVar()

        tk.Label(root, text="Enter Task:", font=("Helvetica", 14, "bold"), bg="black", fg="yellow").pack(pady=10)

        entry_frame = tk.Frame(root, bg="black")
        entry_frame.pack(pady=5)

        self.task_entry = tk.Entry(entry_frame, textvariable=self.task_var, font=("Helvetica", 12), width=30, bg="#222", fg="yellow", insertbackground="yellow")
        self.task_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(entry_frame, text="Add Task", command=self.add_task, bg="yellow", fg="black", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)

        self.task_frame = tk.Frame(root, bg="black")
        self.task_frame.pack(pady=10)

        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Save Tasks", command=self.save_tasks, bg="yellow", fg="black", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Exit", command=root.quit, bg="yellow", fg="black", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=10)

        self.refresh_list()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as file:
                self.tasks = json.load(file)

    def save_tasks(self):
        with open(TASKS_FILE, "w") as file:
            json.dump(self.tasks, file)

    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.tasks.append(task)
            self.task_var.set("")
            self.refresh_list()
        else:
            messagebox.showwarning("Empty", "Please enter a task!")

    def refresh_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        self.task_widgets.clear()
        self.task_vars.clear()

        for i, task in enumerate(self.tasks):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(
                self.task_frame, text=task, font=("Helvetica", 12, "bold"), variable=var,
                command=lambda i=i: self.task_checked(i), 
                bg="black", fg="yellow", selectcolor="green",
                activebackground="black", activeforeground="lime",
                highlightthickness=0, bd=0, padx=10, indicatoron=True
            )
            cb.pack(anchor="w", pady=4)
            self.task_vars.append(var)
            self.task_widgets.append(cb)

    def task_checked(self, index):
        task_name = self.tasks[index]
        del self.tasks[index]
        self.refresh_list()
        self.save_tasks()
        messagebox.showinfo("✅ Task Completed", f"🎉 Great! You completed the task:\n\n'{task_name}'")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskScheduler(root)
    root.mainloop()


