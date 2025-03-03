from interpreter.src.Interpreter import Interpreter, Journal


class CLI:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def run(self):
        line = ""
        while True:
            line = input(">>> ")
            if line == "gamal":
                return
            print(self.interpreter.feedBlock(Journal(line)).value)

interpreter = Interpreter()
cli = CLI(interpreter)
cli.run()

interpreter = Interpreter()

print(interpreter.feedBlock(Journal("4+5")).value)
