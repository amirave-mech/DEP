from expr import display
from eval import Eval, Literal
from parser import Parser
from Scanner import Scanner

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
