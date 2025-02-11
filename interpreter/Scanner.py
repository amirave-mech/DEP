from token import Token
from token_type import TokenType

class Scanner:
    source: str
    tokens: list[Token]

    def __init__(self, source: str):
        self.source = source
        self.tokens = []

    def scanTokens(self) -> list[Token]:
        return []