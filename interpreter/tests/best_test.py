from interpreter.src.Interpreter import Interpreter, Journal


interpreter = Interpreter()


"""
if you want to add test, 
just add a code block or line and it will run on it automaticly :)
"""

tests = [
    "5/0",
    "4*5",
    "5.4 * 6.8",
    "7.23 / 21",
    "-5 / -5",
    "-(-5)",
    "-(-10)-*2" # = -10, need to be fixed

]

for test in tests:
    try:
        print(interpreter.feedBlock(Journal(test)).value)
    except Exception as e:
        print(e)
