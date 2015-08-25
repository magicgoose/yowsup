from yowsup.layers import YowLayer
import os.path

class YowLoggerLayer(YowLayer):

    LOG_PATH = os.path.join(os.path.expanduser("~"), "yowsup_stack.log")  # TODO — add parameter


    def __init__(self):
        super().__init__()
        self.log_path = self.__class__.LOG_PATH

    def send(self, data):
        if self.log_path:
            ldata = prettify(data)
            self.log("tx:\n%s\n\n" % ldata)
        self.toLower(data)

    def receive(self, data):
        if self.log_path:
            ldata = prettify(data)
            self.log("rx:\n%s\n\n" % ldata)
        self.toUpper(data)

    def __str__(self):
        return "Logger Layer"

    def log(self, data):
        with open(self.log_path, "a") as file:
            file.write(data)


def prettify(data):
    return list(data) if type(data) is bytearray else data
