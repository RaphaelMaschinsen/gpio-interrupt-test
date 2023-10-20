import time
import threading
import gpiod
import select

from datetime import timedelta
from gpiod.line import Bias, Edge
from .lcd import LCD


class AuriliaGPIO:
    def add_event_detect(self):
        thread = threading.Thread(target=self.pin_interrupt_thread)
        thread.start()

    def pin_interrupt_thread(self):
        self.async_watch_line_value("/dev/gpiochip0", 25)

    def async_watch_line_value(self, chip_path, line_offset):
        # Assume a button connecting the pin to ground,
        # so pull it up and provide some debounce.
        with gpiod.request_lines(
            chip_path,
            consumer="async-watch-line-value",
            config={
                line_offset: gpiod.LineSettings(
                    edge_detection=Edge.FALLING,
                    bias=Bias.PULL_UP,
                    debounce_period=timedelta(milliseconds=50),
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
                    self.LCD.message("pimpel")


GPIO = AuriliaGPIO()
