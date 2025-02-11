from token_type import TokenType

class Token:
    tokenType: TokenType
    lexeme: str
    literal = None
    line: int

    def __init__(self, tokenType: TokenType, lexeme: str, literal: object, line: int):
        self.tokenType = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return self.tokenType + " " + self.lexeme + " " + self.literal