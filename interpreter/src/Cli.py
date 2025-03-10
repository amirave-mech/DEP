from interpreter.src.interpreter_handler import Interpreter, Journal
from interpreter.src.journal.Journal import JournalSettings


class CLI:
    def __init__(self, interpreter : Interpreter):
        self._interpreter = interpreter

    def run(self):
        line = ""
        while True:
            line = input(">>> ")
            if line == "gamal":
                return
            try:
                print(self._interpreter.feedBlock(line))
            except Exception as e:
                print(f"Error: {e}")


journal_settings = JournalSettings(None, 100, 10)
interpreter = Interpreter(journal_settings, False)
cli = CLI(interpreter)
cli.run()

interpreter = Interpreter()

