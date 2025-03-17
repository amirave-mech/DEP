from __future__ import annotations

from dataclasses import dataclass

# from .token import Token
# from .token_type import TokenType
from interpreter.src.Token import Token
from interpreter.src.token_type import TokenType

type Expr = Grouping | Binary | Unary | Literal


@dataclass
class Grouping:
    expression: Expr


@dataclass
class Binary:
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Unary:
    operator: Token
    expression: Expr


@dataclass
class Literal:
    value: Token


def display(expr: Expr) -> str:
    match expr:
        case Grouping(expr):
            return "(group {})".format(display(expr))
        case Binary(left, operator, right):
            return "({} {} {})".format(display(left), operator, display(right))
        case Unary(operator, expr):
            return "({} {})".format(operator, display(expr))
        case Literal(value):
            match value.tokenType:
                case TokenType.FALSE | TokenType.TRUE | TokenType.NIL:
                    return str(value.tokenType)
                case _:
                    return str(value.literal)
