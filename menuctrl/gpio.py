import threading
from datetime import timedelta
import gpiod
from gpiod.line import Bias, Direction


class AuriliaGPIO:
    def __init__(self):
        self.chip_path = "/dev/gpiochip0"

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
                    edge_detection=edge_detection,
                    bias=Bias.PULL_UP,
                    debounce_period=timedelta(milliseconds=bouncetime),
                )
            },
        ) as request:
            while True:
                # Blocks until at least one event is available
                for event in request.read_edge_events():
                    value =  request.get_value(pin_number)
                    print("{}={}".format(pin_number, value))
                    callback_function()
    
    def get_line_value(self, pin_number):
        with gpiod.request_lines(
            self.chip_path,
            consumer="watch-line",
            config={pin_number: gpiod.LineSettings(direction=Direction.AS_IS)}
        ) as request:
            value = request.get_value(pin_number)
            print("{}={}".format(pin_number, value == 1))


GPIO = AuriliaGPIO()
