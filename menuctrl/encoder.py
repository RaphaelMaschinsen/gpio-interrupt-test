from .gpio import AuriliaGPIO

def test():
    gpio = AuriliaGPIO()
    gpio.add_event_detect()
