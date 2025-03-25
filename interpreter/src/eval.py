from typing import Callable
import interpreter.src.expr as expr
from interpreter.src.expr import Expr
from interpreter.src.Token import Token
from interpreter.src.interpreter_exception import InterpreterException
from interpreter.src.journal.journal_events import *
from interpreter.src.token_type import TokenType
import interpreter.src.stmt as stmt
from interpreter.src.stmt import Stmt
from interpreter.src.environment import Environment

type Literal = str | float | bool

# TODO: Should `Token` hold booleans as literals and not just token types?


# NOTE: While this class currently acts as a namespace, instance-based state will be held in later stages
class Eval:
    def __init__(self):
        self._environment = Environment()
        self._event_listeners: list[Callable[[Event], None]] = []
        
    def subscribe(self, listener: Callable[[Event], None]):
        self._event_listeners.append(listener)
        
    def unsubscribe(self, listener: Callable[[Event], None]):
        self._event_listeners.remove(listener)
        
    def _emit_event(self, event: Event):
        for listener in self._event_listeners:
            listener(event)

    def evaluate(self, statements: list[Stmt]):
        for statement in statements:
            self.__execute_statement(statement)

    def __execute_statement(self, statement: Stmt) -> None:
        match statement:
            case stmt.Print():
                self.__visit_print_stmt(statement)
            case stmt.Expression():
                self.__visit_expr_stmt(statement)
            case stmt.Assignment():
                self.__visit_assign_stmt(statement)
            case stmt.Block():
                self.__visit_block_stmt(statement)
            case stmt.If():
                self.__visit_if_stmt(statement)
            case stmt.While():
                self.__visit_while_stmt(statement)

    def __visit_print_stmt(self,statement: stmt.Print):
        expression = self.expression(statement.expression)
        # TEMPORARY EVENT EMITTER
        self._emit_event(PrintEvent(expression))
        print(expression)

    def __visit_expr_stmt(self,statement: stmt.Expression):
        _ = (self.expression(statement.expression))

    def __visit_assign_stmt(self, statement: stmt.Assignment):
        new_value = self.expression(statement.value)
        # TEMPORARY EVENT EMITTER
        old_value = self._environment.get(statement.name)
        self._emit_event(VariableAssignmentEvent(statement.name, old_value, new_value))
        self._environment.assign(statement.name, new_value)

    def __visit_block_stmt(self, statement: stmt.Block):
        self._environment = Environment(self._environment)
        self.evaluate(statement.statements)
        self._environment = self._environment.parent

    def __visit_if_stmt(self, statement: stmt.If):
        condition = self.expression(statement.condition)

        if condition:
            self.__execute_statement(statement.then_block)
        elif statement.else_block is not None:
            self.__execute_statement(statement.else_block)

    def __visit_while_stmt(self, statement: stmt.While):
        while(self.expression(statement.condition)):
            self.__execute_statement(statement.body)

    def expression(self, ast: Expr) -> Literal:
        match ast:
            case expr.Literal():
                return self.__visit_literal(ast)
            case expr.Grouping():
                return self.__visit_grouping(ast)
            case expr.Unary():
                return self.__visit_unary(ast)
            case expr.Logical():
                return self.__visit_logical(ast)
            case expr.Binary():
                return self.__visit_binary(ast)

    # Expression Visitors
    def __visit_literal(self, expr: expr.Literal) -> Literal:
        if expr.value.tokenType == TokenType.IDENTIFIER:
            return self._environment.get(expr.value.lexeme)

        if expr.value.literal is None:
            raise InterpreterException("Unexpected non-literal token: {}".format(expr.value))

        match expr.value.literal:
            case str() | bool() | float():
                return expr.value.literal
            case int():
                return float(expr.value.literal)
            case _:
                raise InterpreterException(
                    "Literal token of unexpected type: {}".format(expr.value)
                )

    def __visit_grouping(self, expr: expr.Grouping) -> Literal:
        return self.expression(expr.expression)

    def __visit_unary(self, expr: expr.Unary) -> Literal:
        # TODO: Verify type safety of `value`
        value = self.expression(expr.expression)

        match expr.operator.tokenType:
            case TokenType.MINUS:
                if not isinstance(value, float):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.MINUS))
                value = -value
            case TokenType.BANG:
                if not isinstance(value, bool):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.BANG))
                # The language is strictly typed - the negation operator only works on booleans
                value = not value
            case _:
                raise InterpreterException("Unexpected unary operation: {}".format(expr.operator))

        return value

    def __visit_logical(self, expr: expr.Binary) -> Literal:
        left = self.expression(expr.left)

        if not(isinstance(left, bool)):
            raise InterpreterException(self.__format_invalid_literal(expr.operator))

        if expr.operator.tokenType == TokenType.OR and left:
            return True
        if expr.operator.tokenType == TokenType.AND and not left:
            return False

        right = self.expression(expr.right)
        if not(isinstance(right, bool)):
            raise InterpreterException(self.__format_invalid_literal(expr.operator))

        return right

    def __visit_binary(self, expr: expr.Binary) -> Literal:
        left = self.expression(expr.left)
        right = self.expression(expr.right)

        match expr.operator.tokenType:
            case TokenType.MINUS:
                if not (isinstance(left, float) and isinstance(right, float)):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.MINUS))
                return float(left) - float(right)
            case TokenType.SLASH:
                if not (isinstance(left, float) and isinstance(right, float)):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.SLASH))
                if float(right) == 0:
                    raise InterpreterException(ZeroDivisionError)
                return float(left) / float(right)
            case TokenType.STAR:
                if not (isinstance(left, float) and isinstance(right, float)):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.STAR))
                return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                elif isinstance(left, str) and isinstance(right, str):
                    return left + right
                else:
                    raise InterpreterException(self.__format_invalid_literal(TokenType.PLUS))
            case TokenType.GREATER:
                if not isinstance(left, float) or isinstance(right, float):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.GREATER))
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                if not isinstance(left, float) or isinstance(right, float):
                    raise InterpreterException(
                        self.__format_invalid_literal(TokenType.GREATER_EQUAL)
                    )
                return float(left) >= float(right)
            case TokenType.LESS:
                if not (isinstance(left, float) and isinstance(right, float)):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.LESS))
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                if not (isinstance(left, float) and isinstance(right, float)):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.LESS_EQUAL))
                return float(left) <= float(right)
            case TokenType.EQUAL_EQUAL:
                return left == right
            case TokenType.BANG_EQUAL:
                return left != right
            case _:
                raise InterpreterException("Invalid binary operation: {}".format(expr.operator))

    def __format_invalid_literal(self, op_type: TokenType) -> str:
        # TODO: Provide information about which literal token is invalid
        return "{} operator applied on an invalid literal type".format(op_type)
