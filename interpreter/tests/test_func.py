import interpreter.src.expr as expr
from interpreter.src.interpreter_handler import Interpreter

from typing import Final

from interpreter.src.journal.journal import JournalSettings
from interpreter.src.parser import Parser
from interpreter.src.Scanner import Scanner
from interpreter.src.Token import Token
from interpreter.src.token_type import TokenType
from interpreter.src.eval import Eval

SRC: Final = """
function yuvi_cruvi(x, y)
    x <- x + y
    return x
b <- 2
sum <- yuvi_cruvi(b, 3)
print(sum)
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


journal_settings = JournalSettings(None, 100, 10)
interpreter = Interpreter(journal_settings, False)
print(interpreter.feedBlock(SRC).serialize())