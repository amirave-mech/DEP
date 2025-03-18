from __future__ import annotations

from dataclasses import dataclass

from interpreter.src.expr import Expr

from interpreter.src.Token import Token

type Stmt = Expression | Print | Assignment | Block | Void | FuncDef | FuncCall | While

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

@dataclass
class Block:
    statements: list[Stmt]

@dataclass
class If:
    condition: Expr
    then_block: Stmt
    else_block: Stmt | None

@dataclass
class While:
    condition: Expr
    body: Stmt

@dataclass
class FuncDef:
    name: str
    params: list[str]
    body: Block

@dataclass
class FuncCall:
    func_name: str
    params: list[any]

@dataclass
class Void:
    pass