from enum import Enum, auto


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    START_SCOPE = auto()
    END_SCOPE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    CARET = auto()

    # One or two character tokens
    LEFT_ARROW = auto()  # "<-"
    COMMENT = auto()  # "|>"
    BANG = auto()
    BANG_EQUAL = auto()
    # EQUAL = auto() # UNUSED FOR NOW
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto() # e.g. variables, functions etc.
    STRING = auto()
    NUMBER = auto()

    # Keywords
    FALSE = auto()
    TRUE = auto()
    AND = auto()
    OR = auto()
    ELSE = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    PRINT = auto()
    RETURN = auto()
    WHILE = auto()
    EOF = auto()
    EOL = auto()
    UPTO = auto()
    DOWNTO = auto()
    FUNC_DECL = auto()