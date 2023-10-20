from .gpio import GPIO
from gpiod.line import Bias, Edge


def task():
    print("hello")


def test():
    GPIO.add_event_detect(25, Edge.FALLING, task)
