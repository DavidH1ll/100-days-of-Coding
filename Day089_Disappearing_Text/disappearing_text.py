import tkinter as tk
from tkinter import messagebox, filedialog

BG = "#1a1a2e"
FG = "#e0e0e0"
ACCENT = "#e94560"
WIDGET_BG = "#16213e"
TIMEOUT_SECONDS = 5


class DisappearingTextApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Disappearing Text")
        self.window.config(bg=BG, padx=20, pady=15)
        self.window.minsize(650, 450)

        self.timeout = TIMEOUT_SECONDS
        self.time_remaining = self.timeout
        self.timer_id = None
        self.saved = True

        self._build_ui()
        self._reset_timer()

    def _build_ui(self):
        tk.Label(self.window, text="✍ Disappearing Text", font=("Arial", 18, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=(0, 5))

        description = f"Stop typing for {self.timeout} seconds and your text disappears!"
        tk.Label(self.window, text=description, font=("Arial", 9), fg="#777", bg=BG).pack(pady=(0, 10))

        # Info bar
        info_frame = tk.Frame(self.window, bg=BG)
        info_frame.pack(fill="x", pady=(0, 8))

        self.timer_label = tk.Label(info_frame, text=f"⏱ {self.timeout}s", font=("Consolas", 16, "bold"),
                                     fg=ACCENT, bg=BG)
        self.timer_label.pack(side="left")

        self.word_count_label = tk.Label(info_frame, text="Words: 0", font=("Arial", 10),
                                          fg="#777", bg=BG)
        self.word_count_label.pack(side="right")

        # Timeout config
        config_frame = tk.Frame(self.window, bg=BG)
        config_frame.pack(fill="x", pady=(0, 8))
        tk.Label(config_frame, text="Timeout (seconds):", font=("Arial", 9),
                 fg="#777", bg=BG).pack(side="left")
        self.timeout_var = tk.IntVar(value=self.timeout)
        tk.Spinbox(config_frame, from_=3, to=30, textvariable=self.timeout_var, width=4,
                   font=("Arial", 10), bg=WIDGET_BG, fg=FG, buttonbackground="#333",
                   relief="flat", command=self._update_timeout).pack(side="left", padx=(6, 0))

        # Text area
        self.text_widget = tk.Text(self.window, font=("Arial", 12), bg=WIDGET_BG, fg=FG,
                                    insertbackground=ACCENT, relief="flat", padx=12, pady=12,
                                    wrap="word", undo=True)
        self.text_widget.pack(fill="both", expand=True, pady=(0, 10))
        self.text_widget.bind("<KeyRelease>", self._on_type)
        self.text_widget.bind("<Button-1>", lambda e: self._reset_timer())

        # Buttons
        btn_frame = tk.Frame(self.window, bg=BG)
        btn_frame.pack()

        tk.Button(btn_frame, text="💾 Save", font=("Arial", 10), bg="#2d4059", fg=FG,
                  relief="flat", padx=14, pady=4, command=self._save_text).pack(side="left", padx=4)

        tk.Button(btn_frame, text="🗑 Clear", font=("Arial", 10), bg="#555", fg=FG,
                  relief="flat", padx=14, pady=4, command=self._clear_text).pack(side="left", padx=4)

    def _update_timeout(self):
        self.timeout = self.timeout_var.get()
        self.time_remaining = self.timeout
        description = f"Stop typing for {self.timeout} seconds and your text disappears!"
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Label) and "Stop typing" in (widget.cget("text") or ""):
                widget.config(text=description)

    def _on_type(self, event=None):
        self._reset_timer()
        words = len(self.text_widget.get("1.0", "end-1c").split())
        self.word_count_label.config(text=f"Words: {words}")

    def _reset_timer(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
        self.time_remaining = self.timeout
        self.timer_label.config(text=f"⏱ {self.time_remaining}s", fg=ACCENT)
        self.timer_id = self.window.after(1000, self._countdown)

    def _countdown(self):
        self.time_remaining -= 1
        self.timer_label.config(text=f"⏱ {self.time_remaining}s")

        if self.time_remaining <= 2:
            self.timer_label.config(fg="#f44747")
        else:
            self.timer_label.config(fg=ACCENT)

        if self.time_remaining <= 0:
            self._delete_text()
        else:
            self.timer_id = self.window.after(1000, self._countdown)

    def _delete_text(self):
        self.text_widget.delete("1.0", "end")
        self.word_count_label.config(text="Words: 0")
        self._reset_timer()
        self.timer_label.config(text="💨 Gone!", fg="#f44747")
        self.window.after(1500, lambda: self.timer_label.config(text=f"⏱ {self.timeout}s", fg=ACCENT))

    def _save_text(self):
        content = self.text_widget.get("1.0", "end-1c")
        if not content:
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Text saved to:\n{path}")

    def _clear_text(self):
        if self.text_widget.get("1.0", "end-1c").strip():
            if messagebox.askyesno("Clear", "Delete all text?"):
                self.text_widget.delete("1.0", "end")
                self.word_count_label.config(text="Words: 0")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    DisappearingTextApp().run()
