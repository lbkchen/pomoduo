import time

from threading import Timer
from enum import Enum
from math import floor


class PomodoroState(Enum):
    INACTIVE = 0
    WORKING = 1
    RESTING = 2
    YIELD_FOR_CONTINUE = 3


class Pomodoro:
    WORK_TIME_SEC = 25 * 60
    REST_TIME_SEC = 5 * 60
    POLLING_INTERVAL_SEC = 1

    STATE_INTERVALS = {
        PomodoroState.INACTIVE: float("inf"),
        PomodoroState.WORKING: WORK_TIME_SEC,
        PomodoroState.RESTING: REST_TIME_SEC,
        PomodoroState.YIELD_FOR_CONTINUE: float("inf"),
    }

    def __init__(self, debug=False):
        self.state = PomodoroState.INACTIVE
        self.start_time = time.time()
        self.stop_time = None
        self.polling_timer = Timer(self.POLLING_INTERVAL_SEC, self.poll)

        # Debug time in current state
        self._debug = debug
        self.poll()

    @property
    def elapsed(self):
        return round(time.time() - self.start_time)

    @property
    def info(self):
        return {
            "state": self.state.value,
            "elapsed": self.elapsed,
        }

    def start(self):
        self.state = PomodoroState.WORKING
        self.initialize_timer()

        self.timer = Timer(self.WORK_TIME_SEC, self.handle_yield)
        self.timer.start()

    def initialize_timer(self):
        self.start_time = time.time()
        self.end_time = None

    def poll(self):
        # Handle poll first
        self.handle_poll()

        # Repeat timer infinitely by resetting upon completion
        if self.polling_timer.is_alive():
            self.polling_timer.cancel()
        self.polling_timer = Timer(self.POLLING_INTERVAL_SEC, self.poll)
        self.polling_timer.start()

    def handle_poll(self):
        if self._debug:
            print("[DEBUG] Current time: %s, state: %s" %
                  (self.elapsed, self.state))

        # Check for state change
        current_interval = self.STATE_INTERVALS[self.state]
        if self.elapsed >= current_interval:
            print("Need to change state.")

    def handle_yield(self):
        pass
