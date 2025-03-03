from __future__ import annotations

from dataclasses import dataclass

from interpreter.src.expr import Expr

from interpreter.src.Token import Token

type Stmt = Expression | Print | Assignment


@dataclass
class Expression:
    expression: Expr


@dataclass
class Print:
    expression: Expr

@dataclass
class Assignment:
    name: str
    value: Expr