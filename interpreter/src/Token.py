from interpreter.src.token_type import TokenType


class Token:
    tokenType: TokenType
    lexeme: str
    literal = None
    line: int
    char_range: tuple[int, int]

    def __init__(
        self,
        tokenType: TokenType,
        lexeme: str,
        literal: object,
        line: int,
        char_range: tuple[int, int],
    ):
        self.tokenType = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.char_range = char_range

    def __str__(self):
        if self.literal is None:
            return str(self.tokenType) + " " + self.lexeme
        else:
            return str(self.tokenType) + " " + self.lexeme + " " + str(self.literal)
