import json
from interpreter.src.interpreter_handler import Interpreter
from interpreter.src.journal.journal import JournalSettings, Journal


class CLI:
    def __init__(self, interpreter : Interpreter):
        self._interpreter = interpreter

    def run(self):
        line = ""
        while True:
            line += input(">>> ")
            if line == "gamal":
                return
            try:
                if line.endswith('\\'):
                    line = line[:-1] + '\n'
                else:
                    print(line)
                    should_print_journal = False
                    if line.endswith('~'):
                        line = line[:-1]
                        should_print_journal = True
                    
                    result, journal = self._interpreter.feedBlock(line)
                    print(result)
                    
                    if should_print_journal:
                        print(json.dumps(journal.serialize(), indent=2))
                        
                    line = ""
            except Exception as e:
                print(f"Error: {e}")


journal_settings = JournalSettings(None, 100, 10)
interpreter = Interpreter(journal_settings, False)
cli = CLI(interpreter)
cli.run()

interpreter = Interpreter()

