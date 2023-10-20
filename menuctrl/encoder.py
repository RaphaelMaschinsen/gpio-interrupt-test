from .gpio import AuriliaGPIO
import gpiod
import select


GPIO_CHIP = "/dev/gpiochip0"
INPUT = 25


def test():
    gpio = AuriliaGPIO()
    gpio.add_event_detect()
