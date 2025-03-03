from interpreter.src.Token import Token
from interpreter.src.token_type import TokenType

reserved_keywords = {
    "and": TokenType.AND,
    "or": TokenType.OR,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "for": TokenType.FOR,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "var": TokenType.VAR,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "nil": TokenType.NIL,
}

class Scanner:
    _source: str
    _tokens: list[Token]
    _start: int = 0
    _current: int = 0
    _line: int = 1
    _indent_stack: list[int] = [0]
    _last_token_was_colon: bool = False
    
    def __init__(self, source: str):
        self._source = source
        self._tokens = []

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self._start = self._current
            self.scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line, (self._current, self._current)))
        return self._tokens

    def scan_token(self) -> None:
        c = self.advance()

        match c:
            case "(": self.add_token(TokenType.LEFT_PAREN)
            case ")": self.add_token(TokenType.RIGHT_PAREN)
            case "[": self.add_token(TokenType.LEFT_BRACKET)
            case "]": self.add_token(TokenType.RIGHT_BRACKET)
            case ",": self.add_token(TokenType.COMMA)
            case ".": self.add_token(TokenType.DOT)
            case "-": self.add_token(TokenType.MINUS)
            case "+": self.add_token(TokenType.PLUS)
            case "/": self.add_token(TokenType.SLASH)
            case ";": self.add_token(TokenType.SEMICOLON)
            case "*": self.add_token(TokenType.STAR)
            case "^": self.add_token(TokenType.CARET)
            case ":":
                self.add_token(TokenType.COLON)
                self._last_token_was_colon = True
            case "!": self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
            case "=": self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL_EQUAL)
            case "<": self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
            case ">": self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
            case "|":
                if self.match(">"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.error("Unexpected character '|")
            case " " | "\r" | "\t":
                pass  # Ignore spaces inside lines
            case "\n":
                self._line += 1
                self.handle_indentation()
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    self.error(f"Unexpected character '{c}'")

    def handle_indentation(self) -> None:
        count = 0
        while self.peek() == ' ':
            self.advance()
            count += 1

        if count > self._indent_stack[-1]:
            if not self._last_token_was_colon:
                self.error(f"[Line {self._line}] Error: Indentation without preceding colon")
            self._indent_stack.append(count)
            self.add_token(TokenType.START_SCOPE)
        elif count < self._indent_stack[-1]:
            while count < self._indent_stack[-1]:
                self._indent_stack.pop()
                self.add_token(TokenType.END_SCOPE)
        elif self._last_token_was_colon:
            self.error(f"[Line {self._line}] Error: Expected indentation after colon")
        
        self._last_token_was_colon = False  # Reset only after checking indentation

    def advance(self) -> str:
        self._current += 1
        return self._source[self._current - 1]

    def add_token(self, token_type: TokenType, literal: object | None = None) -> None:
        text = self._source[self._start:self._current]
        self._tokens.append(Token(token_type, text, literal, self._line, (self._start, self._current)))

    def is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self._source[self._current] != expected:
            return False
        self._current += 1
        return True

    def peek(self) -> str:
        return '\0' if self.is_at_end() else self._source[self._current]

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self._line += 1
            self.advance()

        if self.is_at_end():
            self.error("Unterminated string")
            return

        self.advance()
        value = self._source[self._start + 1:self._current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        num_str = self._source[self._start:self._current]
        self.add_token(TokenType.NUMBER, float(num_str))

    def identifier(self) -> None:
        while self.peek().isalnum():
            self.advance()
        text = self._source[self._start:self._current].lower()
        token_type = reserved_keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def peek_next(self) -> str:
        return '\0' if self._current + 1 >= len(self._source) else self._source[self._current + 1]

    def error(self, message: str) -> None:
        print(f"[Line {self._line}] Error: {message}")