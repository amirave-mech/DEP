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
    COMMENT = auto()  # "|>"

    # One or two character tokens
    LEFT_ARROW = auto()  # "<-"
    BANG = auto()
    BANG_EQUAL = auto()
    # EQUAL = auto() # UNUSED FOR NOW
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    FALSE = auto()
    TRUE = auto()
    AND = auto()
    OR = auto()
    ELSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    PRINT = auto()
    RETURN = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()
