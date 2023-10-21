from .gpio import GPIO
from gpiod.line import Edge
import time

def task1():
    print("switch callback")


def task2():
    print("rotary callback")


def test():
    GPIO.add_event_detect(25, Edge.BOTH, task1, bouncetime=30)
    GPIO.add_event_detect(14, Edge.BOTH, task2)
    GPIO.add_event_detect(26, Edge.BOTH, task2)
    while True:
        GPIO.get_line_value(25)
        time.sleep(0.5)
