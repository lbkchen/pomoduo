from threading import Timer
from enum import Enum


class PomodoroState(Enum):
    INACTIVE = 0
    WORKING = 1
    RESTING = 2
    YIELD_FOR_CONTINUE = 3


class Pomodoro:
    WORK_TIME_SEC = 25 * 60
    REST_TIME_SEC = 5 * 60

    def __init__(self, debug=False):
        self.state = PomodoroState.INACTIVE
        self.timer = Timer(self.WORK_TIME_SEC, self.handle_yield)

        # Debug time in current state
        self._debug = debug
        self._debug_time = 0
        self._debug_delta = 5
        self._debug_timer = Timer(self._debug_delta, self._debug_log)

    def _debug_log(self, reset_debug_time=False):
        if reset_debug_time:
            self._debug_time = 0
        print("[DEBUG] Current time: %s, state: %s" %
              (self._debug_time, self.state))
        self._debug_timer.cancel()
        self._debug_timer = Timer(self._debug_delta, self._debug_log)
        self._debug_timer.start()
        self._debug_time += self._debug_delta

    def start(self):
        self.state = PomodoroState.WORKING
        self.timer.cancel()
        self.timer = Timer(self.WORK_TIME_SEC, self.handle_yield)
        self.timer.start()
        if self._debug:
            self._debug_log()

    def handle_yield(self):
        pass

    def reset(self):
        self.state = PomodoroState.INACTIVE
        if self.timer:
            self.timer.cancel()
