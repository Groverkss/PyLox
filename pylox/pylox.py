import sys

from TokenType import TokenType
from ErrorReport import ErrorReport
from Scanner import Scanner
from Parser import Parser

from pprint import pprint


class PyLox:
    """
    Main class for PyLox. Runs in two modes:

    1. Source file --> Usage: pylox [script]
    2. Interactive mode --> Usage: pylox
    """

    def __init__(self):
        self.error_report = ErrorReport()

    def main(self):
        if len(sys.argv) > 2:
            self.error_report.report_exit("Usage: pylox [script]")
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[0])
        else:
            self.run_prompt()

    def run_file(self, path):
        """Run in source file mode"""
        try:
            source_file = open(path, "r")
            source = source_file.read()
        except:
            self.error_report.report_exit("Error reading from source file")
            return

        self.run(source)

    def run_prompt(self):
        """Run in interactive mode"""
        while True:
            print("> ", end="")
            try:
                line = input()
            except (EOFError, KeyboardInterrupt):
                print("Bye!")
                sys.exit(0)

            self.run(line)

    def run(self, source):
        self.error_report.had_error = False

        scanner = Scanner(source, self.error_report)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens, self.error_report)
        expression = parser.parse()

        if self.error_report.had_error:
            return

        print(expression)


if __name__ == "__main__":
    pylox = PyLox()
    pylox.main()
