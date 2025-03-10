from interpreter.src.eval import Eval, Literal
from interpreter.src.parser import Parser
from interpreter.src.Scanner import Scanner
from interpreter.src.expr import display

class Journal:
    def __init__(self, value):
        self.value = value



class Interpreter:
    _evaluator = Eval()

    def __init__(self):
        pass 

    def feedBlock(self, code_block: Journal):
        scanner = Scanner(code_block.value)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        stmt_ast_opt = parser.parse()
        return Journal(self._evaluator.evaluate(stmt_ast_opt))
