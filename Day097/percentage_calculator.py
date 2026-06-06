import tkinter as tk

BG = "#1e1e1e"
FG = "#d4d4d4"
ACCENT = "#4ec9b0"
BTN_BG = "#2d2d2d"
BTN_ACTIVE = "#3d3d3d"
OP_BG = "#333333"


class PercentageCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Percentage Calculator")
        self.window.config(bg=BG, padx=20, pady=15)
        self.window.minsize(400, 500)

        self.mode = tk.StringVar(value="percent_of")
        self.display_var = tk.StringVar(value="0")
        self.input1 = ""
        self.input2 = ""
        self.active_input = "input1"
        self.history = []

        self._build_display()
        self._build_mode_selector()
        self._build_numpad()
        self._build_history()

    def _build_display(self):
        disp_frame = tk.Frame(self.window, bg=BG)
        disp_frame.pack(fill="x", pady=(0, 10))

        self.mode_label = tk.Label(disp_frame, text="X% of Y", font=("Arial", 9),
                                    fg="#888", bg=BG)
        self.mode_label.pack(anchor="w")

        tk.Entry(disp_frame, textvariable=self.display_var, font=("Arial", 20),
                 bg=BTN_BG, fg=FG, justify="right", relief="flat",
                 state="readonly", readonlybackground=BTN_BG).pack(fill="x", pady=(4, 0))

    def _build_mode_selector(self):
        modes = [
            ("X% of Y", "percent_of"),
            ("X is what % of Y", "what_percent"),
            ("% Change", "percent_change"),
            ("Tip Calculator", "tip_calc"),
        ]
        frame = tk.Frame(self.window, bg=BG)
        frame.pack(fill="x", pady=(0, 10))

        for text, value in modes:
            tk.Radiobutton(
                frame, text=text, variable=self.mode, value=value,
                font=("Arial", 9), fg=FG, bg=BG, selectcolor=BG,
                activebackground=BG, activeforeground=ACCENT,
                command=self._mode_changed, indicatoron=False,
                padx=8, pady=4, relief="flat"
            ).pack(side="left", padx=2)

    def _build_numpad(self):
        pad_frame = tk.Frame(self.window, bg=BG)
        pad_frame.pack(fill="x")

        buttons = [
            ("7", "8", "9", "C"),
            ("4", "5", "6", "DEL"),
            ("1", "2", "3", "="),
            ("0", "00", ".", "CLR"),
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, label in enumerate(row):
                btn = tk.Button(
                    pad_frame, text=label, font=("Arial", 13, "bold"),
                    bg=BTN_BG if label != "=" else ACCENT,
                    fg=FG if label != "=" else BG,
                    activebackground=BTN_ACTIVE,
                    relief="flat", padx=16, pady=10,
                    command=lambda l=label: self._on_button(l)
                )
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)
                pad_frame.columnconfigure(col_idx, weight=1)

    def _build_history(self):
        self.history_frame = tk.Frame(self.window, bg=BG)
        self.history_frame.pack(fill="both", expand=True, pady=(10, 0))

        tk.Label(self.history_frame, text="History", font=("Arial", 9, "bold"),
                 fg="#888", bg=BG).pack(anchor="w")

        self.history_text = tk.Text(self.history_frame, height=6, font=("Consolas", 9),
                                     bg=BTN_BG, fg="#888", relief="flat",
                                     state="disabled", padx=8, pady=6)
        self.history_text.pack(fill="both", expand=True)

    def _mode_changed(self):
        labels = {
            "percent_of": "X% of Y",
            "what_percent": "X is what % of Y",
            "percent_change": "% Change",
            "tip_calc": "Tip Calculator",
        }
        self.mode_label.config(text=labels.get(self.mode.get(), ""))
        self._clear()

    def _on_button(self, label):
        if label in "0123456789.":
            current = getattr(self, self.active_input)
            if label == "." and "." in current:
                return
            setattr(self, self.active_input, current + label)
            self._update_display()
        elif label == "00":
            current = getattr(self, self.active_input)
            setattr(self, self.active_input, current + "00")
            self._update_display()
        elif label == "DEL":
            current = getattr(self, self.active_input)
            setattr(self, self.active_input, current[:-1])
            self._update_display()
        elif label == "C":
            setattr(self, self.active_input, "")
            self._update_display()
        elif label == "CLR":
            self._clear()
        elif label == "=":
            self._calculate()

    def _update_display(self):
        if self.mode.get() == "tip_calc":
            self.display_var.set(f"Bill: {self.input1 or '0'}  Tip: {self.input2 or '15'}%")
        else:
            self.display_var.set(f"{self.input1 or '0'} | {self.input2 or '0'}")

    def _clear(self):
        self.input1 = ""
        self.input2 = ""
        self.active_input = "input1"
        self.display_var.set("0")

    def _calculate(self):
        try:
            v1 = float(self.input1) if self.input1 else 0
            v2 = float(self.input2) if self.input2 else 0
        except ValueError:
            self.display_var.set("Error")
            return

        mode = self.mode.get()
        if mode == "percent_of":
            result = (v1 / 100) * v2
            formula = f"{v1}% of {v2} = {result:.2f}"
        elif mode == "what_percent":
            result = (v1 / v2) * 100 if v2 != 0 else 0
            formula = f"{v1} is {result:.2f}% of {v2}"
        elif mode == "percent_change":
            result = ((v2 - v1) / v1) * 100 if v1 != 0 else 0
            direction = "increase" if result >= 0 else "decrease"
            formula = f"{v1} → {v2}: {abs(result):.2f}% {direction}"
        elif mode == "tip_calc":
            tip = v1 * (v2 / 100)
            total = v1 + tip
            formula = f"Bill ${v1:.2f} + {v2}% tip = ${total:.2f} (tip: ${tip:.2f})"

        self.display_var.set(formula[:50])
        self._add_to_history(formula)
        self.input1 = ""
        self.input2 = ""
        self.active_input = "input1"

    def _add_to_history(self, entry):
        self.history.insert(0, entry)
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")
        for h in self.history[:10]:
            self.history_text.insert("end", h + "\n")
        self.history_text.config(state="disabled")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    PercentageCalculator().run()
