from __future__ import annotations

from dataclasses import dataclass

# from .token import Token
# from .token_type import TokenType
from interpreter.src.Token import Token
from interpreter.src.token_type import TokenType

type Expr = Grouping | Binary | Logical | Unary | Literal | ArrayLiteral | ArrayAccess


@dataclass
class Grouping:
    expression: Expr


@dataclass
class Binary:
    left: Expr
    operator: Token
    right: Expr

# Even though the `Binary` node structure is exactly the same,
# the separation would be useful at the evaluation step since
# in contrast to `Binary`, `Logical` nodes short circuit
@dataclass
class Logical:
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

@dataclass
class ArrayLiteral:
    elts: list[Expr]

@dataclass
class ArrayAccess:
    name: str
    idx: Expr


def display(expr: Expr) -> str:
    match expr:
        case Grouping(expr):
            return "(group {})".format(display(expr))
        case Binary(left, operator, right):
            return "({} {} {})".format(display(left), operator, display(right))
        case Logical(left, operator, right):
            return "({} {} {})".format(display(left), operator, display(right))
        case Unary(operator, expr):
            return "({} {})".format(operator, display(expr))
        case Literal(value):
            match value.tokenType:
                case TokenType.FALSE | TokenType.TRUE | TokenType.NIL:
                    return str(value.tokenType)
                case _:
                    return str(value.literal)
