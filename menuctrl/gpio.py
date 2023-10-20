import time
import threading


class AuriliaGPIO:
    def __init__(self, name="TestString"):
        self.name = name

    def add_event_detect(self):
        thread = threading.Thread(target=self.pin_interrupt_task)
        thread.start()

    def pin_interrupt_task(self):
        while True:
            print(self.name)
            time.sleep(1)
