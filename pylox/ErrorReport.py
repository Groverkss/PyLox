import sys


class ErrorReport:
    """Error reporter for PyLox"""

    def __init__(self):
        self.had_error = False

    def report(self, line, where, message):
        print("[Line " + str(line) + "] Err" + where + ": " + message)

    def error(self, line, message):
        self.report(line, "", message)
        self.had_error = True

    def report_exit(self, message):
        self.error(0, message)
        sys.exit(1)
