from interpreter.src.Interpreter import Interpreter, Journal


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
                print(e)


interpreter = Interpreter()
cli = CLI(interpreter)
cli.run()

interpreter = Interpreter()

print(interpreter.feedBlock(Journal("4+5")).value)
