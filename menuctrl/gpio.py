import time
import threading
import gpiod
import select

from datetime import timedelta
from gpiod.line import Bias, Edge
from .lcd import LCD


class AuriliaGPIO:
    def __init__(self):
        self.chip_path = "/dev/gpiochip0"

    def add_event_detect(self, pin_number, edge_detection, callback_function, bouncetime=50):
        thread = threading.Thread(target=self.async_watch_line_value, args=(pin_number, edge_detection,
                                                                            callback_function, bouncetime))
        thread.start()

    def async_watch_line_value(self, pin_number, edge_detection, callback_function, bouncetime):
        # Assume a button connecting the pin to ground,
        # so pull it up and provide some debounce.
        with gpiod.request_lines(
            self.chip_path,
            consumer="async-watch-line-value",
            config={
                pin_number: gpiod.LineSettings(
                    edge_detection=edge_detection,
                    bias=Bias.PULL_UP,
                    debounce_period=timedelta(milliseconds=bouncetime),
                )
            },
        ) as request:
            poll = select.poll()
            poll.register(request.fd, select.POLLIN)
            while True:
                # Other fds could be registered with the poll and be handled
                # separately using the return value (fd, event) from poll()
                poll.poll()
                for event in request.read_edge_events():
                    callback_function()


GPIO = AuriliaGPIO()
