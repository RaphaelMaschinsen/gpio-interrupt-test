import threading
from datetime import timedelta
import gpiod
from gpiod.line import Bias, Edge


class AuriliaGPIO:
    def __init__(self):
        self.chip_path = "/dev/gpiochip0"
        self.pin_values = {}

    def add_event_detect(self, pin_number, edge_detection, callback_function, bouncetime=0):
        thread = threading.Thread(target=self.poll_line_value, args=(pin_number, edge_detection,
                                                                            callback_function, bouncetime))
        thread.start()

    def poll_line_value(self, pin_number, edge_detection, callback_function, bouncetime):
        # Assume a button connecting the pin to ground,
        # so pull it up and provide some debounce.
        with gpiod.request_lines(
            self.chip_path,
            consumer="watch-line",
            config={
                pin_number: gpiod.LineSettings(
                    edge_detection=Edge.BOTH,
                    bias=Bias.PULL_UP,
                    debounce_period=timedelta(milliseconds=bouncetime),
                )
            },
        ) as request:
            while True:
                # Blocks until at least one event is available
                for event in request.read_edge_events():
                    pin_value =  request.get_value(pin_number).value
                    self.pin_values.update(pin_number, pin_value)
                    callback_function()

    def get_line_value(self, pin_number):
        try:
            return self.pin_values[pin_number]
        except:
            print("Error [gpio.py]: no value for pin_number stored")

GPIO = AuriliaGPIO()
