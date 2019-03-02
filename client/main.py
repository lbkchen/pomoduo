#!/usr/bin/env python

import signal
import skywriter


some_value = 5000


@skywriter.flick()
def flick(start, finish):
    print('Got a flick!', start, finish)


@skywriter.double_tap()
def doubletap(position):
    print('Double tap!', position)


@skywriter.tap()
def tap(position):
    print('Tap!', position)


@skywriter.touch()
def touch(position):
    print('Touch!', position)


signal.pause()
