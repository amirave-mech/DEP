import pytest
from interpreter.src.interpreter_handler import Interpreter, Journal


interpreter = Interpreter()


tests = [
    "5/0",
    "4*5",
    "5.4 * 6.8",
    "7.23 / 21",
    "-5 / -5",
    "-(-5)",
    "-(-10)*-2" 
]

known_exceptions = [
    ZeroDivisionError
]

expected_outputs = [
    ZeroDivisionError,
    20.0,
    36.72,
    0.3442857142857143,
    1.0,
    5.0,
    -20.0
]


def test_interpreter():
    for (test, expected_output) in zip(tests, expected_outputs):
        if expected_output in known_exceptions:
            with pytest.raises(Exception) as exception_info:
                interpreter.feedBlock(Journal(test)).value
            assert exception_info.value.args[0] == expected_output
        else:
            assert interpreter.feedBlock(Journal(test)).value == expected_output
 

if __name__ == "__main__":
    test_interpreter()