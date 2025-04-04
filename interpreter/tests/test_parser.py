import interpreter.src.expr as expr

from interpreter.src.parser import Parser
from interpreter.src.Token import Token
from interpreter.src.token_type import TokenType

toks = [
    Token(TokenType.NUMBER, "5", 5, 1),
    Token(TokenType.PLUS, "+", None, 1),
    Token(TokenType.LEFT_PAREN, "(", None, 1),
    Token(TokenType.NUMBER, "6", 6, 1),
    Token(TokenType.PLUS, "+", None, 1),
    Token(TokenType.NUMBER, "6", 6, 1),
    Token(TokenType.RIGHT_PAREN, ")", None, 1),
]

parser = Parser(toks)
expr_ast_opt = parser.parse()

if expr_ast_opt is None:
    raise

print("The result is: ", expr.display(expr_ast_opt))
