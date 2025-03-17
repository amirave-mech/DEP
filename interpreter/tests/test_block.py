import interpreter.src.expr as expr

from typing import Final

from interpreter.src.parser import Parser
from interpreter.src.Scanner import Scanner
from interpreter.src.Token import Token
from interpreter.src.token_type import TokenType
from interpreter.src.eval import Eval

SRC: Final = """
x = 1
print x
    x = 2
    print x
        x = 3
        print x
    print x
print x
"""

scanner = Scanner(SRC)
tokens = scanner.scan_tokens()
[print(tok) for tok in tokens]
parser = Parser(tokens)
stmt_ast_opt = parser.parse()

if stmt_ast_opt is None:
    raise

[print(stmt) for stmt in stmt_ast_opt]

evaluator = Eval()
evaluator.evaluate(stmt_ast_opt)