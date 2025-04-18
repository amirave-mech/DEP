import interpreter.src.expr as expr
from interpreter.src.interpreter_handler import Interpreter
import os

from typing import Final

from interpreter.src.journal.journal import JournalSettings
from interpreter.src.parser import Parser
from interpreter.src.Scanner import Scanner
from interpreter.src.Token import Token
from interpreter.src.token_type import TokenType
from interpreter.src.eval import Eval

SRC: Final = """
function yuvi_cruvi(arr, len)
    i <- 1
    sum <- 0
    while (i <= len)
        sum <- sum + arr[i]
        arr[i] <- -1
        i <- i+1
    return sum
function factorial(n)
    if (n = 0)
        return 1
    else
        return n*factorial(n-1)
function print_arr(a, len)
    i <- 1
    while (i <= len)
        print(a[i])
        i <- i+1
b <- [0,1,2,3]
sum <- yuvi_cruvi(b, 4)
print(sum)
ten_fact <- factorial(10)
print(ten_fact)
print_arr(b, 4)
"""

# scanner = Scanner(SRC)
# tokens = scanner.scan_tokens()
# [print(tok) for tok in tokens]
# parser = Parser(tokens)
# stmt_ast_opt = parser.parse()
#
# [print(stmt) for stmt in stmt_ast_opt]
#
# evaluator = Eval()
# evaluator.evaluate(stmt_ast_opt)

source: str
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "quicksort.txt"))
with open(src_path, "r") as file:
    source = file.read()

journal_settings = JournalSettings(None, 100, 10)
interpreter = Interpreter(journal_settings, False)
print(interpreter.feedBlock(source).serialize())