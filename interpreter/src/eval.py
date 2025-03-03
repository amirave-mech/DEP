import interpreter.src.expr as expr
from interpreter.src.expr import Expr
from interpreter.src.Token import Token
from interpreter.src.token_type import TokenType

type Literal = str | float | bool

# TODO: Should `Token` hold booleans as literals and not just token types?


# NOTE: While this class currently acts as a namespace, instance-based state will be held in later stages
class Eval:
    @staticmethod
    def evaluate(statements: list[Stmt]):
        try:
            for statement in statements:
                Eval.execute_statement(statement)
        except:
            # TODO: Add runtime evaluation errors reporting
            pass

    @staticmethod
    def execute_statement(statement: Stmt) -> None:
        match statement:
            case stmt.Print():
                Eval.__visit_print_stmt(statement)
            case stmt.Expression():
                Eval.__visit_expr_stmt(statement)

    @staticmethod
    def __visit_print_stmt(stmt: stmt.Print):
        expr = Eval.expression(stmt.expression)
        print(expr)

    @staticmethod
    def __visit_expr_stmt(stmt: stmt.Expression):
        _ = Eval.expression(stmt.expression)

    @staticmethod
    def expression(ast: Expr) -> Literal:
        match ast:
            case expr.Literal():
                return Eval.__visit_literal(ast)
            case expr.Grouping():
                return Eval.__visit_grouping(ast)
            case expr.Unary():
                return Eval.__visit_unary(ast)
            case expr.Binary():
                return Eval.__visit_binary(ast)

    # Expression Visitors
    @staticmethod
    def __visit_literal(expr: expr.Literal) -> Literal:
        # print(type(expr.value.literal))
        if expr.value.literal is None:
            raise Exception("Unexpected non-literal token: {}".format(expr.value))

        match expr.value.literal:
            case str() | bool() | float():
                return expr.value.literal
            case int():
                return float(expr.value.literal)
            case _:
                raise Exception(
                    "Literal token of unexpected type: {}".format(expr.value)
                )

    @staticmethod
    def __visit_grouping(expr: expr.Grouping) -> Literal:
        return Eval.expression(expr.expression)

    @staticmethod
    def __visit_unary(expr: expr.Unary) -> Literal:
        # TODO: Verify type safety of `value`
        value = Eval.expression(expr.expression)

        match expr.operator.tokenType:
            case TokenType.MINUS:
                if not isinstance(value, float):
                    raise Exception(Eval.__format_invalid_literal(TokenType.MINUS))
                value = -value
            case TokenType.BANG:
                if not isinstance(value, bool):
                    raise Exception(Eval.__format_invalid_literal(TokenType.BANG))
                # The language is strictly typed - the negation operator only works on booleans
                value = not value
            case _:
                raise Exception("Unexpected unary operation: {}".format(expr.operator))

        return value

    @staticmethod
    def __visit_binary(expr: expr.Binary) -> Literal:
        left = Eval.expression(expr.left)
        right = Eval.expression(expr.right)

        match expr.operator.tokenType:
            case TokenType.MINUS:
                if not (isinstance(left, float) or isinstance(right, float)):
                    raise Exception(Eval.__format_invalid_literal(TokenType.MINUS))
                return float(left) - float(right)
            case TokenType.SLASH:
                if not (isinstance(left, float) or isinstance(right, float)):
                    raise Exception(Eval.__format_invalid_literal(TokenType.SLASH))
                if float(right) == 0:
                    raise Exception(ZeroDivisionError)
                return float(left) / float(right)
            case TokenType.STAR:
                if not (isinstance(left, float) or isinstance(right, float)):
                    raise Exception(Eval.__format_invalid_literal(TokenType.STAR))
                return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                elif isinstance(left, str) and isinstance(right, str):
                    return left + right
                else:
                    raise Exception(Eval.__format_invalid_literal(TokenType.PLUS))
            case TokenType.GREATER:
                if not isinstance(left, float) or isinstance(right, float):
                    raise Exception(Eval.__format_invalid_literal(TokenType.GREATER))
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                if not isinstance(left, float) or isinstance(right, float):
                    raise Exception(
                        Eval.__format_invalid_literal(TokenType.GREATER_EQUAL)
                    )
                return float(left) >= float(right)
            case TokenType.LESS:
                if not isinstance(left, float) or isinstance(right, float):
                    raise Exception(Eval.__format_invalid_literal(TokenType.LESS))
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                if not isinstance(left, float) or isinstance(right, float):
                    raise Exception(Eval.__format_invalid_literal(TokenType.LESS_EQUAL))
                return float(left) <= float(right)
            case TokenType.EQUAL_EQUAL:
                return left == right
            case TokenType.BANG_EQUAL:
                return left == right
            case _:
                raise Exception("Invalid binary operation: {}".format(expr.operator))

    @staticmethod
    def __format_invalid_literal(op_type: TokenType) -> str:
        # TODO: Provide information about which literal token is invalid
        return "{} operator applied on an invalid literal type".format(op_type)
