from rpi_lcd import LCD as LCDRPI


# LCD Dummy class to log into console instead of an lcd
# Logging into systemd journal on raspi works with this library:
# from cysystemd import journal
# journal.write(self.displayed_message)
class LCDDummy:
    def __init__(self):
        self.displayed_message = ""

    def clear(self):
        self.displayed_message = ""

    # Function that displays a string on the lcd
    def message(self, message):
        self.displayed_message = message
        print(self.displayed_message)


class LCD:
    def __init__(self):
        self.lcd = LCDRPI()
        self.clear()

    def clear(self):
        self.displayed_message = ""
        self.lcd.clear()

    # Function that displays a string on the lcd
    def message(self, message):
        self.displayed_message = message
        self.lcd.clear()
        if "\n" in self.displayed_message:
            self.lcd.text(self.displayed_message.splitlines()[0], 1)
            self.lcd.text(self.displayed_message.splitlines()[1], 2)
        else:
            self.lcd.text(self.displayed_message, 1)