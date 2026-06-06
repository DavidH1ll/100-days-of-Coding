import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

BG = "#1e1e1e"
FG = "#d4d4d4"
ACCENT = "#4ec9b0"
WIDGET_BG = "#2d2d2d"
PRIORITY_COLORS = {"High": "#f44747", "Medium": "#e6a817", "Low": "#6a9955"}
TASK_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


class TodoApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("To Do Agenda")
        self.window.config(bg=BG, padx=20, pady=15)
        self.window.minsize(500, 550)
        self.tasks = self._load_tasks()

        self._build_ui()
        self._refresh_list()
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_tasks(self):
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE) as f:
                return json.load(f)
        return []

    def _save_tasks(self):
        with open(TASK_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def _build_ui(self):
        tk.Label(self.window, text="📋 To Do Agenda", font=("Arial", 18, "bold"),
                  fg=ACCENT, bg=BG).pack(pady=(0, 10))

        # Input frame
        input_frame = tk.Frame(self.window, bg=BG)
        input_frame.pack(fill="x", pady=(0, 8))

        self.task_entry = tk.Entry(input_frame, font=("Arial", 11), bg=WIDGET_BG, fg=FG,
                                    insertbackground=FG, relief="flat", width=30)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.task_entry.bind("<Return>", lambda e: self._add_task())

        self.priority_var = tk.StringVar(value="Medium")
        tk.OptionMenu(input_frame, self.priority_var, "High", "Medium", "Low",
                      command=lambda _: None).pack(side="left", padx=(0, 8))

        tk.Button(input_frame, text="+ Add", font=("Arial", 10, "bold"),
                  bg=ACCENT, fg=BG, relief="flat", padx=12, pady=3,
                  command=self._add_task).pack(side="left")

        # Due date
        date_frame = tk.Frame(self.window, bg=BG)
        date_frame.pack(fill="x", pady=(0, 10))
        tk.Label(date_frame, text="Due (YYYY-MM-DD):", font=("Arial", 9),
                 fg="#888", bg=BG).pack(side="left")
        self.date_entry = tk.Entry(date_frame, font=("Arial", 9), bg=WIDGET_BG, fg=FG,
                                    insertbackground=FG, relief="flat", width=12)
        self.date_entry.pack(side="left", padx=(6, 0))

        # Task list
        self.canvas = tk.Canvas(self.window, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.task_frame = tk.Frame(self.canvas, bg=BG)

        self.task_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * e.delta / 60), "units"))

        # Stats bar
        self.stats_label = tk.Label(self.window, text="", font=("Arial", 9),
                                     fg="#888", bg=BG)
        self.stats_label.pack(pady=(8, 0))

    def _add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return

        task = {
            "id": datetime.now().timestamp(),
            "text": text,
            "priority": self.priority_var.get(),
            "due_date": self.date_entry.get().strip() or None,
            "completed": False,
            "created": datetime.now().isoformat(),
        }
        self.tasks.append(task)
        self._save_tasks()
        self.task_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self._refresh_list()

    def _toggle_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self._save_tasks()
        self._refresh_list()

    def _delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self._save_tasks()
        self._refresh_list()

    def _refresh_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        sorted_tasks = sorted(self.tasks, key=lambda t: (
            t["completed"],
            {"High": 0, "Medium": 1, "Low": 2}.get(t["priority"], 1),
            t.get("due_date") or "9999",
        ))

        for task in sorted_tasks:
            self._add_task_row(task)

        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["completed"])
        self.stats_label.config(text=f"Tasks: {total} | Done: {done} | Remaining: {total - done}")

    def _add_task_row(self, task):
        color = PRIORITY_COLORS.get(task["priority"], FG)
        frame = tk.Frame(self.task_frame, bg=WIDGET_BG, padx=10, pady=6)
        frame.pack(fill="x", pady=2)

        # Priority indicator
        tk.Frame(frame, bg=color, width=4).pack(side="left", fill="y", padx=(0, 8))

        # Checkbox
        var = tk.BooleanVar(value=task["completed"])
        cb = tk.Checkbutton(frame, variable=var, bg=WIDGET_BG, activebackground=WIDGET_BG,
                            selectcolor=WIDGET_BG, fg=FG, command=lambda: self._toggle_task(task["id"]))
        cb.pack(side="left")

        # Task text
        text = task["text"]
        if task["completed"]:
            text = f"\u0336{text}\u0336"
        tk.Label(frame, text=text, font=("Arial", 11),
                 fg="#666" if task["completed"] else FG, bg=WIDGET_BG,
                 anchor="w").pack(side="left", padx=(6, 10))

        # Due date
        if task.get("due_date"):
            tk.Label(frame, text=f"📅 {task['due_date']}", font=("Arial", 9),
                     fg="#888", bg=WIDGET_BG).pack(side="left", padx=(0, 10))

        # Priority badge
        tk.Label(frame, text=task["priority"], font=("Arial", 8, "bold"),
                 fg=color, bg=WIDGET_BG).pack(side="left", padx=(0, 10))

        # Delete button
        tk.Button(frame, text="✕", font=("Arial", 9), fg="#f44747", bg=WIDGET_BG,
                  relief="flat", padx=4, bd=0, activebackground=WIDGET_BG,
                  command=lambda: self._delete_task(task["id"])).pack(side="right")

    def _on_close(self):
        self._save_tasks()
        self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    TodoApp().run()
