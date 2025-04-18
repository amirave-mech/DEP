import math
from typing import Callable
import interpreter.src.expr as expr
from interpreter.src.exceptions import ReturnException
from interpreter.src.expr import Expr
from interpreter.src.Token import Token
from interpreter.src.interpreter_exception import InterpreterException
from interpreter.src.journal.journal_events import *
from interpreter.src.token_type import TokenType
import interpreter.src.stmt as stmt
from interpreter.src.stmt import Stmt
from interpreter.src.environment import Environment

type Literal = str | float | bool | list[Literal]

# TODO: Should `Token` hold booleans as literals and not just token types?


# NOTE: While this class currently acts as a namespace, instance-based state will be held in later stages
class Eval:
    def __init__(self):
        self._environment = Environment()
        self._event_listeners: list[Callable[[Event], None]] = []
        self._environment.assign("mod", stmt.FuncBody(["x", "y"], stmt.BuiltinFunctions.MOD))
        self._environment.assign("log", stmt.FuncBody(["base", "x"], stmt.BuiltinFunctions.LOG))
        self._environment.assign("floor", stmt.FuncBody(["x"], stmt.BuiltinFunctions.FLOOR))
        self._environment.assign("ceil", stmt.FuncBody(["x"], stmt.BuiltinFunctions.CEIL))

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
            # case stmt.Length():
            #     self.__visit_length_stmt(statement)
            case stmt.Expression():
                self.__visit_expr_stmt(statement)
            case stmt.Assignment():
                self.__visit_assign_stmt(statement)
            case stmt.ArrayAssignment():
                self.__visit_array_assign_stmt(statement)
            case stmt.Block():
                self.__visit_block_stmt(statement)
            case stmt.If():
                self.__visit_if_stmt(statement)
            case stmt.While():
                self.__visit_while_stmt(statement)
            case stmt.FuncDef():
                self.__visit_func_def(statement)
            case stmt.Return():
                self.__visit_return_stmt(statement)

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

    def __visit_array_assign_stmt(self, statement: stmt.ArrayAssignment):
        new_value = self.expression(statement.value)

        array = self._environment.get(statement.name)
        if array is None:
            raise InterpreterException("variable '{}' is not defined".format(statement.name))
        # TODO: Notify journal of array modification
        if not isinstance(array, list):
            raise InterpreterException("Trying to access a non-array variable")

        index = int(self.expression(statement.idx))
        if index < 1 or index > len(array):
            raise InterpreterException("Invalid array indexing, exceeding array size")

        # TEMPORARY EVENT EMITTER
        temp = array.copy()
        array[index - 1] = new_value
        self._emit_event(ArrayModificationEvent(statement.name, array, temp))

    def __visit_block_stmt(self, statement: stmt.Block, new_env=None):
        curr_env = self._environment
        if new_env is None:
            new_env = Environment(self._environment)
        self._environment = new_env
        self.evaluate(statement.statements)
        self._environment = curr_env

    def __visit_func_def(self, statement: stmt.FuncDef):
        if self._environment.get_root_env().get(statement.func_name) is not None:
            raise InterpreterException(f"Error: redefinition of previously defined function {statement.func_name}")
        self._environment.assign_to_root(statement.func_name, statement.func)

    def __visit_func_call(self, statement: expr.FuncCall):
        func: stmt.FuncBody
        func = self._environment.get(statement.func_name)
        if func is None:
            raise InterpreterException("variable '{}' is not defined".format(statement.func_name))

        if type(func) is not stmt.FuncBody:
            raise InterpreterException("""An internal error has occurred, a function was used that was indeed not defined as a
             function! For support please incessantly call 053-337-1749, thank you.""")
        if len(func.params) is not len(statement.params):
            raise InterpreterException("""Error: mismatched number of parameters and arguments given!
             For support please incessantly call 053-337-1749, thank you.""")
        if type(func.body) == stmt.BuiltinFunctions:
            match func.body:
                case stmt.BuiltinFunctions.MOD:
                    return self.expression(statement.params[0]) % self.expression(statement.params[1])
                case stmt.BuiltinFunctions.LOG:
                    return math.log(self.expression(statement.params[1]), self.expression(statement.params[0]))
                case stmt.BuiltinFunctions.FLOOR:
                    return float(math.floor(self.expression(statement.params[0])))
                case stmt.BuiltinFunctions.CEIL:
                    return float(math.ceil(self.expression(statement.params[0])))

        func_env = Environment(self._environment.get_root_env())
        for p_name, p_val in zip(func.params, statement.params):
            func_env.assign(p_name, self.expression(p_val))
        try:
            self.__visit_block_stmt(func.body, func_env)
        except ReturnException as ret_val:
            return ret_val.ret_val
        return expr.Void

    def __visit_return_stmt(self, statement: Stmt):
        expression = self.expression(statement.ret_val)
        raise ReturnException(expression)

    def __visit_if_stmt(self, statement: stmt.If):
        condition = self.expression(statement.condition)

        if condition:
            self._emit_event(IfStartEvent(condition))
            self.__execute_statement(statement.then_block)
            self._emit_event(IfEndEvent())
        elif statement.else_block is not None:
            self._emit_event(ElseStartEvent())
            self.__execute_statement(statement.else_block)
            self._emit_event(ElseEndEvent())
        else:
            self._emit_event(IfStartEvent(False))
            self._emit_event(IfEndEvent())

    def __visit_while_stmt(self, statement: stmt.While):
        self._emit_event(WhileStartEvent("missing"))

        iterations = 0
        while self.expression(statement.condition):
            self._emit_event(WhileIterationStartEvent())
            self.__execute_statement(statement.body)
            iterations += 1
            self._emit_event(WhileIterationEndEvent())

        self._emit_event(WhileEndEvent(iterations))

    def expression(self, ast: Expr) -> Literal:
        match ast:
            case expr.Literal():
                return self.__visit_literal(ast)
            case expr.ArrayLiteral():
                return self.__visit_array_literal(ast)
            case expr.ArrayAccess():
                return self.__visit_array_access(ast)
            case expr.Length():
                return self.__visit_length(ast)
            case expr.Grouping():
                return self.__visit_grouping(ast)
            case expr.Unary():
                return self.__visit_unary(ast)
            case expr.Logical():
                return self.__visit_logical(ast)
            case expr.Binary():
                return self.__visit_binary(ast)
            case expr.FuncCall():
                return self.__visit_func_call(ast)

    # Expression Visitors
    def __visit_literal(self, expr: expr.Literal) -> Literal:
        if expr.value.tokenType == TokenType.IDENTIFIER:
            variable = self._environment.get(expr.value.lexeme)
            if variable is None:
                raise InterpreterException("variable '{}' is not defined".format(expr.value.lexeme))
            return self._environment.get(expr.value.lexeme)

        if expr.value.tokenType == TokenType.TRUE:
            return True
        if expr.value.tokenType == TokenType.FALSE:
            return False

        match expr.value.literal:
            case str() | float():
                return expr.value.literal
            case int():
                return float(expr.value.literal)
            case _:
                raise InterpreterException(
                    "Literal token of unexpected type: {}".format(expr.value)
                )

    def __visit_array_literal(self, expr: expr.ArrayLiteral) -> Literal:
        evaluated_elts = []

        for elt in expr.elts:
            # TODO: Constrain array elements types to be of the same one
            evaluated_elts.append(self.expression(elt))

        return evaluated_elts

    def __visit_array_access(self, expr: expr.ArrayAccess) -> Literal:
        array = self._environment.get(expr.name)
        if array is None:
            raise InterpreterException("variable '{}' is not defined".format(expr.name))
        # TODO: Notify journal of array modification
        if not isinstance(array, list):
            raise InterpreterException("Trying to access a non-array variable")

        index = int(self.expression(expr.idx))
        if index < 1 or index > len(array):
            raise InterpreterException("Invalid array indexing, exceeding array size")

        return array[index - 1]

    def __visit_length(self, expr: expr.Length) -> Literal:
        variable = self._environment.get(expr.name)
        if variable is None:
            raise InterpreterException("variable '{}' is not defined".format(expr.name))
        return float(len(variable))

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
                    raise InterpreterException("Division by zero")
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
                if not (isinstance(left, float) or isinstance(right, float)):
                    raise InterpreterException(self.__format_invalid_literal(TokenType.GREATER))
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                if not (isinstance(left, float) or isinstance(right, float)):
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
