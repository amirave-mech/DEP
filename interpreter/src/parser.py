from Token import Token
from token_type import TokenType
import expr
from expr import Expr

# TODO:
# - Improve error reporting, add concise failure messages (token position, etc..)
# - Catch unexpected EOF caused by invalid syntax


class Parser:
    _tokens: list[Token]
    _pos: int = 0

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens

    def parse(self) -> Expr | None:
        try:
            return self.__expression()
        except Exception as err:
            print("Failed to parse: {}".format(err))

    def __is_eof(self) -> bool:
        return self._pos == len(self._tokens) - 1

    def __advance(self) -> None:
        if self.__is_eof():
            raise Exception("already EOF")
        self._pos += 1

    def __peek(self) -> Token:
        return self._tokens[self._pos]

    def __display_peek_info(self) -> str:
        tok = self.__peek()
        return "at line {}, type: {}, lexeme: {}".format(
            tok.line, tok.tokenType, tok.lexeme
        )

    def __match_tok_type(self, types: list[TokenType]) -> bool:
        curr_type = self.__peek().tokenType
        return any([tok_type == curr_type for tok_type in types])

    # Mutually recursing expression parsing
    def __expression(self) -> Expr:
        return self.__equality()

    def __equality(self) -> Expr:
        left_expr = self.__comparison()

        while self.__match_tok_type([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.__peek()
            self.__advance()

            right_expr = self.__comparison()

            left_expr = expr.Binary(left_expr, operator, right_expr)

        return left_expr

    def __comparison(self) -> Expr:
        left_expr = self.__term()

        while self.__match_tok_type(
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ]
        ):
            operator = self.__peek()
            self.__advance()

            right_expr = self.__term()

            left_expr = expr.Binary(left_expr, operator, right_expr)

        return left_expr

    def __term(self) -> Expr:
        left_expr = self.__factor()

        while self.__match_tok_type([TokenType.MINUS, TokenType.PLUS]):
            operator = self.__peek()
            self.__advance()

            right_expr = self.__factor()

            left_expr = expr.Binary(left_expr, operator, right_expr)

        return left_expr

    def __factor(self) -> Expr:
        left_expr = self.__unary()

        while self.__match_tok_type([TokenType.SLASH, TokenType.STAR]):
            operator = self.__peek()
            self.__advance()

            right_expr = self.__unary()

            left_expr = expr.Binary(left_expr, operator, right_expr)

        return left_expr

    def __unary(self) -> Expr:
        if self.__match_tok_type([TokenType.BANG, TokenType.MINUS]):
            operator = self.__peek()
            self.__advance()

            return expr.Unary(operator, self.__unary())
        return self.__primary()

    def __primary(self) -> Expr:
        # TODO: Add identifiers (variable expressions)
        if self.__match_tok_type(
            [
                TokenType.NUMBER,
                TokenType.STRING,
                TokenType.TRUE,
                TokenType.FALSE,
                TokenType.NIL,
            ]
        ):
            literal = self.__peek()
            if not self.__is_eof():
                self.__advance()
            return expr.Literal(literal)

        if self.__match_tok_type([TokenType.LEFT_PAREN]):
            self.__advance()

            grouping_expr = self.__expression()

            if not self.__match_tok_type([TokenType.RIGHT_PAREN]):
                raise Exception("{}: expected ')'".format(self.__display_peek_info()))

            return expr.Grouping(grouping_expr)

        raise Exception("{}: expected expression".format(self.__display_peek_info()))
