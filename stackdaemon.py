#!/usr/bin/env python
from os import system
from time import sleep
import RPi.GPIO as GPIO

DEFAULT_INTERVAL = 5
DEFAULT_PULSE_WIDTH = 0.1
DEFAULT_HBT_PIN = 5
DEFAULT_SIG_PIN = 6
TESTING = False

class StackDaemon(object):
    def __init__(
            self,
            testing=False,
            hbt_pin=DEFAULT_HBT_PIN,
            sig_pin=DEFAULT_SIG_PIN,
            interval=DEFAULT_INTERVAL,
            pulse_width=DEFAULT_PULSE_WIDTH):
        global TESTING
        TESTING = testing
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) #stop it displaying warnings aout channel already in use
        GPIO.setup(hbt_pin, GPIO.OUT)
        GPIO.setup(sig_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        self._hbt_pin = hbt_pin
        self._sig_pin = sig_pin
        self._interval = interval
        self._pulse_width = pulse_width

    def run(self):
        if TESTING:
            print "TESTING MODE"
        GPIO.add_event_detect(self._sig_pin, GPIO.FALLING, callback=sig_recieved)
        while True:
            self._send_heartbeat()
            sleep(self._interval)


    def _send_heartbeat(self):
        GPIO.output(self._hbt_pin, GPIO.HIGH)
        sleep(self._pulse_width)
        GPIO.output(self._hbt_pin, GPIO.LOW)

    def send_signal(self):
        GPIO.setup(self._sig_pin, GPIO.OUT)
        GPIO.output(self._sig_pin, GPIO.LOW)
        sleep(self._pulse_width)
        GPIO.output(self._hbt_pin, GPIO.HIGH)
        GPIO.setup(self._sig_pin, GPIO.IN)

def sig_recieved(channeli):
    if not TESTING:
        system("sudo shutdown -h now")
    else:
        print "signal recieved"

if __name__ == "__main__":
    STACK = StackDaemon()
    STACK.run()
