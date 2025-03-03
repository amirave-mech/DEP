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
    "def": TokenType.DEF
}

class Scanner:
    _source: str
    _tokens: list[Token]
    _start: int = 0
    _current: int = 0
    _line: int = 1
    _indent_stack: list[int] = [0]
    _last_token_was_colon: bool = False
    _func_def: bool = False # is set to True while a function is being defined, set to False when that is done
    
    def __init__(self, source: str):
        self._source = source
        self._tokens = []

    def scan_tokens(self) -> list[Token]:
        # for i in range(10):
        #     new_var = self.extract_word()
        #     print(len(new_var))
        #     print(new_var)
        # print("hi")
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
            case "!": self.add_token(TokenType.BANG_EQUAL if self.match_and_advance("=") else TokenType.BANG)
            case "=": self.add_token(TokenType.EQUAL_EQUAL if self.match_and_advance("=") else TokenType.EQUAL_EQUAL)
            case "<": self.add_token(TokenType.LESS_EQUAL if self.match_and_advance("=") else TokenType.LESS)
            case ">": self.add_token(TokenType.GREATER_EQUAL if self.match_and_advance("=") else TokenType.GREATER)
            case "|":
                if self.match_and_advance(">"):
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
        if text:  # Skip adding empty tokens
            self._tokens.append(Token(token_type, text, literal, self._line, (self._start, self._current)))

    def is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def match(self, expected: str) -> bool:
        return self.is_at_end() or self._source[self._current] != expected
    
    # advances if the expected is matched
    def match_and_advance(self, expected: str) -> bool:
        if self.match(expected):
            self.advance()
            return True
        return False
    
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
        self._current -= 1 # it was already incremented falsly in the scan_token func
        text = self.extract_word()
        
        # Check if this is a reserved keyword
        token_type = reserved_keywords.get(text.lower(), TokenType.IDENTIFIER)
        
        # If it's a function definition, just enable parsing mode, don't extract again
        if token_type == TokenType.DEF:
            self._func_def = True
            self.add_token(token_type)
            self.parse_function_signature()  # Call function signature parsing immediately
            return  # Prevent double tokenization
        
        self.add_token(token_type)

    def extract_word(self) -> str:
        """Extracts a word (identifier or keyword), skipping leading whitespace but stopping at non-alphanumeric characters."""
        # Skip leading whitespaces but not newlines
        while self.peek() in " \t":
            self.advance()
        
        self._start = self._current  # Correctly set _start here
        
        while self.peek().isalnum() or self.peek() == "_":  # Allow underscores for variable names
            self.advance()
        
        return self._source[self._start:self._current]

    def parse_function_signature(self) -> None:
        """Handles function definitions after encountering 'def'."""
        # Expect a function name (identifier)
        while self.peek() in " \t":  # Skip spaces before function name
            self.advance()
        
        if not self.peek().isalpha():
            self.error(f"[Line {self._line}] Expected function name after 'def'")
            return
        
        func_name = self.extract_word()  # Extract once, now correctly
        if func_name in reserved_keywords:
            self.error(f"[Line {self._line}] Error: Function name cannot be a reserved keyword")
            return
        self.add_token(TokenType.FUNC_NAME)
        
        # Expect a left parenthesis
        while self.peek() in " \t":  # Skip spaces before (
            self.advance()
        
    
        if not self.match("("):
            self.error(f"[Line {self._line}] Expected '(' after function name")
            return
        else:
            print("what the fuck")
        self._start = self._current # skip the other things so we only add a parenthesis without other shit
        self.add_token(TokenType.LEFT_PAREN)
        
        # Parse parameters (comma-separated identifiers)
        while self.peek() in " \t":  # Skip spaces before parameters
            self.advance()
        
        if self.peek().isalpha():  # Check if there are parameters
            while True:
                param_name = self.extract_word()
                if param_name:  # Ensure it's not empty before adding
                    self.add_token(TokenType.PARAM)
                
                while self.peek() in " \t":  # Skip spaces before comma
                    self.advance()
                
                if self.peek() == ",":
                    self.advance()
                    self.add_token(TokenType.COMMA)
                elif self.peek() == ")":
                    self._start = self._current # skip the other things so we only add a parenthesis without other shit
                    break  # Stop if we reach closing parenthesis
                else:
                    self.error(f"[Line {self._line}] Unexpected character in parameter list: {self.peek()}")
                    return
        
        # Expect a right parenthesis
        if not self.match(")"):
            self.error(f"[Line {self._line}] Expected ')' to close function parameters")
            return
        self.add_token(TokenType.RIGHT_PAREN)
        
        # Reset function definition state
        self._func_def = False

    def peek_next(self) -> str:
        return '\0' if self._current + 1 >= len(self._source) else self._source[self._current + 1]

    def error(self, message: str) -> None:
        print(f"[Line {self._line}] Error: {message}")