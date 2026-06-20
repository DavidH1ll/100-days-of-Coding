"""Day 81 - Typing Speed Test (Tkinter GUI).

A 60-second typing speed test with a random passage. WPM, accuracy,
and completion are computed in :mod:`scoring` so they can be
unit-tested without a display.

Run with::

    python main.py
"""

from __future__ import annotations

import random
import time
import tkinter as tk

from scoring import (
    PASSAGES,
    compute_accuracy,
    compute_completion,
    compute_wpm,
)

BG = "#1e1e1e"
FG = "#d4d4d4"
ACCENT = "#4ec9b0"
ACCENT_ERR = "#f44747"
ACCENT_CORRECT = "#6a9955"
WIDGET_BG = "#2d2d2d"

TEST_DURATION_SECONDS = 60
TICK_INTERVAL_MS = 1000
MIN_TYPED_FOR_EARLY_END = 1  # must type at least 1 char before early end
EXCELLENT_WPM_THRESHOLD = 40


class TypingSpeedTest:
    """Tkinter application for a 60-second typing test."""

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Typing Speed Test")
        self.window.config(bg=BG, padx=30, pady=20)
        self.window.minsize(750, 550)

        self.time_left = TEST_DURATION_SECONDS
        self.timer_running = False
        self.timer_id: str | None = None
        self.start_time: float | None = None
        self.current_passage = ""
        self.total_chars = 0
        self.correct_chars = 0

        self._build_ui()
        self._load_passage()

    def _build_ui(self) -> None:
        tk.Label(
            self.window, text="⌨ Typing Speed Test", font=("Consolas", 22, "bold"),
            fg=ACCENT, bg=BG,
        ).pack(pady=(0, 10))

        self.timer_label = tk.Label(
            self.window, text=f"⏱ {TEST_DURATION_SECONDS}", font=("Consolas", 32, "bold"),
            fg=ACCENT, bg=BG,
        )
        self.timer_label.pack(pady=(0, 5))

        self.stats_label = tk.Label(
            self.window, text="WPM: 0 | Accuracy: 0%", font=("Consolas", 12),
            fg=FG, bg=BG,
        )
        self.stats_label.pack(pady=(0, 10))

        self.passage_frame = tk.Frame(self.window, bg=WIDGET_BG, padx=15, pady=12)
        self.passage_frame.pack(fill="x", pady=(0, 10))

        self.passage_label = tk.Label(
            self.passage_frame, text="", font=("Consolas", 12),
            fg=FG, bg=WIDGET_BG, wraplength=680, justify="left",
        )
        self.passage_label.pack()

        self.text_widget = tk.Text(
            self.window, height=6, font=("Consolas", 13),
            bg=WIDGET_BG, fg=FG, insertbackground=ACCENT,
            relief="flat", padx=10, pady=10, wrap="word",
            state="disabled",
        )
        self.text_widget.pack(fill="x", pady=(0, 15))
        self.text_widget.bind("<KeyRelease>", self._on_key)

        btn_frame = tk.Frame(self.window, bg=BG)
        btn_frame.pack()

        self.start_btn = tk.Button(
            btn_frame, text="▶ Start", font=("Consolas", 12, "bold"),
            bg=ACCENT, fg=BG, activebackground="#3cb896",
            relief="flat", padx=20, pady=6, cursor="hand2",
            command=self._start_test,
        )
        self.start_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(
            btn_frame, text="↺ New Passage", font=("Consolas", 12),
            bg="#555", fg=FG, activebackground="#666",
            relief="flat", padx=16, pady=6, cursor="hand2",
            command=self._load_passage,
        )
        self.reset_btn.pack(side="left", padx=5)

        self.result_label = tk.Label(self.window, text="", font=("Consolas", 13, "bold"), fg=ACCENT, bg=BG)
        self.result_label.pack(pady=(10, 0))

    def _load_passage(self) -> None:
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False
        self.time_left = TEST_DURATION_SECONDS
        self.timer_label.config(text=f"⏱ {TEST_DURATION_SECONDS}")
        self.stats_label.config(text="WPM: 0 | Accuracy: 0%")
        self.result_label.config(text="")
        self.current_passage = random.choice(PASSAGES)
        self.passage_label.config(text=self.current_passage)
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.config(state="disabled")
        self.start_btn.config(state="normal")

    def _start_test(self) -> None:
        if self.timer_running:
            return
        self.timer_running = True
        self.start_time = time.time()
        self.total_chars = 0
        self.correct_chars = 0
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.focus_set()
        self.start_btn.config(state="disabled")
        self.result_label.config(text="")
        self._update_timer()

    def _update_timer(self) -> None:
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"⏱ {self.time_left}")
            self._update_stats()
            self.timer_id = self.window.after(TICK_INTERVAL_MS, self._update_timer)
        else:
            self._end_test()

    def _on_key(self, event: tk.Event | None = None) -> None:
        if not self.timer_running:
            return
        self._update_stats()
        if event and event.keysym == "Return":
            typed = self.text_widget.get("1.0", "end-1c").strip()
            if (
                typed
                and len(typed) >= MIN_TYPED_FOR_EARLY_END
                and typed[-1] not in ".!?"
                and len(typed) >= len(self.current_passage)
            ):
                self._end_test()

    def _update_stats(self) -> None:
        typed = self.text_widget.get("1.0", "end-1c")
        if not typed:
            return

        self.total_chars = len(typed)
        self.correct_chars = sum(
            (1 for i, c in enumerate(typed)
             if i < len(self.current_passage) and c == self.current_passage[i]),
        )

        elapsed = time.time() - (self.start_time or 0)
        wpm = compute_wpm(self.correct_chars, elapsed)
        accuracy = compute_accuracy(self.correct_chars, self.total_chars)

        self.stats_label.config(text=f"WPM: {wpm} | Accuracy: {accuracy}%")

        if self.time_left <= 5:
            self.timer_label.config(fg=ACCENT_ERR)
        else:
            self.timer_label.config(fg=ACCENT)

    def _end_test(self) -> None:
        self.timer_running = False
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

        typed = self.text_widget.get("1.0", "end-1c")
        elapsed = time.time() - (self.start_time or 0)
        if elapsed <= 0:
            elapsed = TEST_DURATION_SECONDS

        correct = sum(
            (1 for i, c in enumerate(typed)
             if i < len(self.current_passage) and c == self.current_passage[i]),
        )
        total_passage = len(self.current_passage)

        wpm = compute_wpm(correct, elapsed)
        accuracy = compute_accuracy(correct, len(typed)) if typed else 0
        completion = compute_completion(len(typed), total_passage)

        self.result_label.config(
            text=f"Results: {wpm} WPM | {accuracy}% Accuracy | {completion}% Complete",
            fg=ACCENT_CORRECT if wpm >= EXCELLENT_WPM_THRESHOLD else ACCENT,
        )
        self.text_widget.config(state="disabled")
        self.start_btn.config(state="normal")
        self._highlight_errors()

    def _highlight_errors(self) -> None:
        typed = self.text_widget.get("1.0", "end-1c")
        self.text_widget.config(state="normal")

        for i, c in enumerate(typed):
            tag = "correct" if i < len(self.current_passage) and c == self.current_passage[i] else "error"
            self.text_widget.tag_add(tag, f"1.{i}", f"1.{i+1}")

        self.text_widget.tag_config("correct", foreground=ACCENT_CORRECT)
        self.text_widget.tag_config("error", foreground=ACCENT_ERR, overstrike=True)
        self.text_widget.config(state="disabled")

    def run(self) -> None:
        self.window.mainloop()


if __name__ == "__main__":
    TypingSpeedTest().run()
