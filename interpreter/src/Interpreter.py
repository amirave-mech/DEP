from interpreter.src.eval import Eval, Literal
from interpreter.src.parser import Parser
from interpreter.src.Scanner import Scanner
from interpreter.src.expr import Expr

class Journal:
    def __init__(self, value):
        self.value = value



class Interpreter:
    def __init__(self):
        pass 

    def feedBlock(self, code_block: Journal):
        scanner = Scanner(code_block.value)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expr_ast_opt = parser.parse()
        return Journal(Eval.expression(expr_ast_opt))
