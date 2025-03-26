from __future__ import annotations

from dataclasses import dataclass

from interpreter.src.expr import Expr

from interpreter.src.Token import Token

type Stmt = Expression | Print | Assignment | Block | FuncDef | While | If | Return

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
class ArrayAssignment:
    name: str
    idx: Expr
    value: Expr

@dataclass
class Block:
    statements: list[Stmt]

@dataclass
class FuncBody:
    params: list[str]
    body: Block

@dataclass
class FuncDef:
    func_name: str
    func: FuncBody

@dataclass
class Return:
    ret_val: Expr

@dataclass
class If:
    condition: Expr
    then_block: Stmt
    else_block: Stmt | None

@dataclass
class While:
    condition: Expr
    body: Stmt