from interpreter.src.interpreter_handler import Interpreter, Journal


class CLI:
    def __init__(self, interpreter : Interpreter):
        self.interpreter = interpreter

    def run(self):
        line = ""
        while True:
            line = input(">>> ")
            if line == "gamal":
                return
            try:
                print(self.interpreter.feedBlock(Journal(line)).value)
            except Exception as e:
                print(f"Error: {e}")


interpreter = Interpreter()
cli = CLI(interpreter)
cli.run()

interpreter = Interpreter()

