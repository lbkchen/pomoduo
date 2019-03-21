import time

from threading import Timer
from enum import Enum
from math import floor


class PomodoroState:
    DURATION_SECS = 100

    def __init__(self):
        self.name = "invalid"
        self.duration_secs = self.DURATION_SECS

    def __repr__(self):
        return "<PomodoroState.%s>" % self.name.upper()

    def __str__(self):
        return self.__repr__()


class YieldState(PomodoroState):
    DURATION_SECS = float("inf")

    def __init__(self, duration_secs=DURATION_SECS):
        self.name = "inactive"
        self.duration_secs = duration_secs


class WorkingState(PomodoroState):
    DURATION_SECS = 25 * 60

    def __init__(self, duration_secs=DURATION_SECS):
        self.name = "working"
        self.duration_secs = duration_secs


class RestingState(PomodoroState):
    DURATION_SECS = 5 * 60

    def __init__(self, duration_secs=DURATION_SECS):
        self.name = "resting"
        self.duration_secs = duration_secs


class Pomodoro:
    POLLING_INTERVAL_SEC = 1

    def __init__(self, poll_callback=None, debug=False):
        self.state = YieldState()
        self.timer = None
        self.start_time = time.time()
        self.poll_callback = poll_callback
        self.polling_timer = Timer(self.POLLING_INTERVAL_SEC, self.poll)

        # Debug time in current state
        self._debug = debug
        self.poll()

    @property
    def elapsed(self):
        return round(time.time() - self.start_time)

    @property
    def remaining(self):
        return self.state.duration_secs - self.elapsed

    @property
    def info(self):
        return {
            "state": str(self.state),
            "elapsed": self.elapsed,
            "remaining": self.remaining,
        }

    def begin_current_state(self, on_finish=None):
        if self.timer:
            self.timer.cancel()
        if not on_finish:
            on_finish = self.begin_yielding
        self.timer = Timer(self.state.duration_secs, on_finish)
        self.timer.start()
        self.start_time = time.time()

    def begin_yielding(self):
        self.state = YieldState()
        if self.timer:
            self.timer.cancel()
        self.timer = None

    def begin_working(self):
        self.state = WorkingState()
        self.begin_current_state(self.begin_resting)

    def begin_resting(self):
        self.state = RestingState()
        self.begin_current_state(self.begin_yielding)

    def poll(self):
        # Handle poll first
        self.handle_poll()

        # Repeat timer infinitely by resetting upon completion
        self.polling_timer.cancel()
        self.polling_timer = Timer(self.POLLING_INTERVAL_SEC, self.poll)
        self.polling_timer.start()

    def handle_poll(self):
        if self._debug:
            print("[DEBUG] Current time: %s, state: %s" %
                  (self.elapsed, self.state))

        if self.poll_callback:
            self.poll_callback(self.info)

        # Check for state change
        if self.remaining <= 0:
            print("Need to change state.")
