from .gpio import GPIO
from gpiod.line import Bias, Edge


def task1():
    print("switch callback")


def task2():
    print("rotary callback")


def test():
    GPIO.add_event_detect(25, Edge.FALLING, task1, bouncetime=250)
    GPIO.add_event_detect(14, Edge.BOTH, task2)
    GPIO.add_event_detect(26, Edge.BOTH, task2)
