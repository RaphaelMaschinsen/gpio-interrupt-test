class AuriliaGPIO:
    def __init__(self, pin_number=25):
        self.pin_number = pin_number
        print("init")

    def add_event_detect(self):
        print(self.pin_number)