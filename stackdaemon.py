#!/usr/bin/env python3
"""
    Interface for Pistack
    October/November 2017
    Philip Basford
"""
from os import system
from time import sleep
from argparse import ArgumentParser
import RPi.GPIO as GPIO

from stackerrors import NoStackFound

DEFAULT_INTERVAL = 5
DEFAULT_PULSE_WIDTH = 0.1
DEFAULT_HBT_PIN = 5
DEFAULT_SIG_PIN = 6
DEVICE_TREE_PATH = "/proc/device-tree/hat/product"
DEVICE_TREE_PRODUCT = "Pi stack"

TESTING = False

class StackDaemon(object):
    """
        Interface for dealing with the pistack microcontroller
    """

    def __init__(
            self,
            testing=False,
            hbt_pin=DEFAULT_HBT_PIN,
            sig_pin=DEFAULT_SIG_PIN,
            interval=DEFAULT_INTERVAL,
            pulse_width=DEFAULT_PULSE_WIDTH):
        """
            Setup the interface.
            If testing is true then don't perform acutal shutdown
            the pins used, heartbeat interval, and signal with can be changed
            using these parameters
        """
        if not detect_hat():
            raise NoStackFound("No Pi stack detected unable to continue")
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
        """
            Starts sending a heartbeat out to the pistack and listens (interrupt based)
            for shutdown signal
        """
        if TESTING:
            print("TESTING MODE")
        GPIO.add_event_detect(self._sig_pin, GPIO.FALLING, callback=sig_recieved)
        while True:
            self._send_heartbeat()
            sleep(self._interval)


    def _send_heartbeat(self):
        """
            Send heartbeat to pistack to keep health check happy
        """
        GPIO.output(self._hbt_pin, GPIO.HIGH)
        sleep(self._pulse_width)
        GPIO.output(self._hbt_pin, GPIO.LOW)

    def send_signal(self):
        """
            Pulls the signal line low to tell the pistack a shutdown is in progress
        """
        GPIO.setup(self._sig_pin, GPIO.OUT)
        GPIO.output(self._sig_pin, GPIO.LOW)
        sleep(self._pulse_width)
        GPIO.output(self._hbt_pin, GPIO.HIGH)
        GPIO.setup(self._sig_pin, GPIO.IN)

def detect_hat():
    """
        Checks the HAT product string from the eeprom to make sure that the
        pi stack is connected
    """
    hat = open(DEVICE_TREE_PATH, "r").read().rstrip('\x00')
    return hat == DEVICE_TREE_PRODUCT

def sig_recieved(channel):
    """
        Called when a signal is recieved, if not testing will initiate a shutdown of the pi
    """
    if not TESTING:
        system("sudo shutdown -h now")
    else:
        print("signal recieved")

if __name__ == "__main__":
    PARSER = ArgumentParser(
        description="Send the heartbeat to the pistack board and listten for shutdown signal")
    PARSER.add_argument(
        "-v", "--version", action="version",
        version="%(prog)s 0.2")
    PARSER.add_argument(
        "-t", "--testing", action="store_true",
        help="Testing mode - won't shutdown on signal")
    ARGS = PARSER.parse_args()
    TESTING = ARGS.testing
    print(TESTING)
    STACK = StackDaemon(TESTING)
    STACK.run()
