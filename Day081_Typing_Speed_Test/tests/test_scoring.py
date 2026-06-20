"""Tests for the Day 81 typing speed test scoring functions."""

from __future__ import annotations

from scoring import (
    CHARS_PER_WORD,
    MIN_MINUTES,
    PASSAGES,
    compute_accuracy,
    compute_completion,
    compute_wpm,
)


class TestPassages:
    def test_passages_is_non_empty(self) -> None:
        assert len(PASSAGES) > 0

    def test_all_passages_are_non_empty_strings(self) -> None:
        for p in PASSAGES:
            assert isinstance(p, str)
            assert len(p) > 0

    def test_passages_have_typical_wpm_content(self) -> None:
        # Sanity: each passage should be at least a few words long
        for p in PASSAGES:
            assert len(p.split()) >= 8


class TestComputeWpm:
    def test_zero_chars_zero_time(self) -> None:
        assert compute_wpm(0, 0) == 0

    def test_zero_chars_with_time(self) -> None:
        assert compute_wpm(0, 60) == 0

    def test_zero_time_avoids_division_by_zero(self) -> None:
        # elapsed = 0 would normally be 0 minutes; should hit MIN_MINUTES floor
        result = compute_wpm(0, 0)
        assert result == 0

    def test_basic_wpm_calculation(self) -> None:
        # 5 chars in 60 seconds = 1 WPM (5 chars = 1 "word")
        assert compute_wpm(CHARS_PER_WORD, 60) == 1

    def test_typical_typing_speed(self) -> None:
        # 250 correct chars in 60 seconds = 50 WPM
        # (250 / 5 chars-per-word) / 1 minute = 50 wpm
        assert compute_wpm(250, 60) == 50

    def test_returns_integer(self) -> None:
        assert isinstance(compute_wpm(100, 60), int)

    def test_higher_accuracy_higher_wpm(self) -> None:
        # Same time, more correct chars → higher WPM
        low = compute_wpm(50, 60)
        high = compute_wpm(200, 60)
        assert high > low

    def test_longer_time_lower_wpm(self) -> None:
        # Same correct chars, longer time → lower WPM
        fast = compute_wpm(200, 30)
        slow = compute_wpm(200, 120)
        assert fast > slow


class TestComputeAccuracy:
    def test_zero_total_returns_zero(self) -> None:
        assert compute_accuracy(0, 0) == 0

    def test_negative_total_returns_zero(self) -> None:
        # Defensive: don't crash on weird input
        assert compute_accuracy(5, -1) == 0

    def test_perfect_accuracy(self) -> None:
        assert compute_accuracy(100, 100) == 100

    def test_zero_accuracy(self) -> None:
        assert compute_accuracy(0, 100) == 0

    def test_partial_accuracy(self) -> None:
        # 75 of 100 correct = 75%
        assert compute_accuracy(75, 100) == 75

    def test_returns_integer(self) -> None:
        assert isinstance(compute_accuracy(33, 100), int)

    def test_truncates_not_rounds(self) -> None:
        # 33/100 = 0.33 → 33 (not 33.x rounded)
        assert compute_accuracy(33, 100) == 33


class TestComputeCompletion:
    def test_zero_total_returns_zero(self) -> None:
        assert compute_completion(0, 0) == 0

    def test_zero_typed_zero_percent(self) -> None:
        assert compute_completion(0, 100) == 0

    def test_full_completion(self) -> None:
        assert compute_completion(100, 100) == 100

    def test_partial_completion(self) -> None:
        assert compute_completion(50, 100) == 50

    def test_caps_at_100_when_over_typed(self) -> None:
        # User types more than the passage length
        assert compute_completion(150, 100) == 100

    def test_returns_integer(self) -> None:
        assert isinstance(compute_completion(33, 100), int)


class TestConstants:
    def test_chars_per_word_is_5(self) -> None:
        # Industry standard for WPM calculation
        assert CHARS_PER_WORD == 5

    def test_min_minutes_is_a_floor(self) -> None:
        # MIN_MINUTES prevents division by zero when elapsed = 0
        assert MIN_MINUTES > 0
        assert MIN_MINUTES < 0.1
