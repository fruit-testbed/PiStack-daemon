#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO

DEFAULT_INTERVAL = 5
DEFAULT_PULSE_WIDTH = 0.1
DEFAULT_HBT_PIN = 5
DEFAULT_SIG_PIN = 6

class StackDaemon(object):
    def __init__(
            self,
            hbt_pin=DEFAULT_HBT_PIN,
            sig_pin=DEFAULT_SIG_PIN,
            interval=DEFAULT_INTERVAL,
            pulse_width=DEFAULT_PULSE_WIDTH):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(hbt_pin, GPIO.OUT)
        GPIO.setup(sig_pin, GPIO.IN)
        self._hbt_pin = hbt_pin
        self._sig_pin = sig_pin
        self._interval = interval
        self._pulse_width = pulse_width

    def run(self):
        while True:
            self._send_heartbeat()
            sleep(self._interval)


    def _send_heartbeat(self):
        GPIO.output(self._hbt_pin, GPIO.HIGH)
        sleep(self._pulse_width)
        GPIO.output(self._hbt_pin, GPIO.LOW)

if __name__ == "__main__":
    STACK = StackDaemon()
    STACK.run()