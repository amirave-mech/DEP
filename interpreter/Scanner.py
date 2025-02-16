from Token import Token
from token_type import TokenType


class Scanner:
    _source: str
    _tokens: list[Token]

    _start: int = 0
    _current: int = 0
    _line: int = 1

    def __init__(self, source: str):
        self._source = source
        self._tokens = []

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self._start = self._current
            self.scan_token()

        self._tokens.append(Token(TokenType.EOF, '', None, self._line, (self._current, self._current)))
        return self._tokens

    def scan_token(self) -> None:
        """Scan the next token and append it to the list of tokens"""
        c = self.advance()

        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '[':
                self.add_token(TokenType.LEFT_BRACKET)
            case ']':
                self.add_token(TokenType.RIGHT_BRACKET)
            case '{':
                self.add_token(TokenType.START_SCOPE)
            case '}':
                self.add_token(TokenType.END_SCOPE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case '/':
                self.add_token(TokenType.SLASH)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '^':
                self.add_token(TokenType.CARET)

            case '!':
                self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL_EQUAL)
            case '<':
                self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
            case '>':
                self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
            case '|':
                if self.match('>'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    # TODO: dont exit out of the loop? maybe just report the error?
                    raise Exception(self._line, "[Scanner] Unexpected Character")

            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self._line += 1

            case _:
                # TODO: dont exit out of the loop? maybe just report the error?
                raise Exception(self._line, "[Scanner] Unexpected Character")

    def advance(self) -> str:
        self._current += 1
        return self._source[self._current - 1]

    def add_token(self, token_type: TokenType, literal: object | None = None) -> None:
        text = self._source[self._start:self._current]
        self._tokens.append(Token(token_type, text, literal, self._line, (self._start, self._current)))

    def is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '/0'

        return self._source[self._current]
