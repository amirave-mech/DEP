from interpreter.src.interpreter_handler import Interpreter, Journal


interpreter = Interpreter()


tests = [
    "4*5",
    "5.4 * 6.8",
    "7.23 / 21",
    "-5 / -5",
    "-(-5)",
    "-(-10)*-2" # = -10, need to be fixed
]

expected_outputs = [
    20.0,
    36.72,
    0.3442857142857143,
    1.0,
    5.0,
    -10.0
]


def test_interpreter():
    for (test, expected_output) in zip(tests, expected_outputs):
        assert interpreter.feedBlock(Journal(test)).value == expected_output


if __name__ == "__main__":
    test_interpreter()