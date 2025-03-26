import interpreter.src.expr as expr
from interpreter.src.expr import Expr
from interpreter.src.Token import Token
from interpreter.src.interpreter_exception import InterpreterException
from interpreter.src.token_type import TokenType
from interpreter.src.stmt import Stmt, FuncDef, FuncBody
import interpreter.src.stmt as stmt

# TODO:
# - Improve error reporting, add concise failure messages (token position, etc..)
# - Catch unexpected EOF caused by invalid syntax


class Parser:
    _tokens: list[Token]
    _pos: int = 0
    _is_in_func_def: bool = False

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos: int = 0

    def parse(self) -> list[Stmt] | None:
        statements: list[Stmt] = []

        while not self.__is_eof():
            if self.__peek().tokenType == TokenType.EOL:
                self.__advance()
            else:
                statements.append(self.__statement())

        return statements

    def __is_eof(self, step = 0) -> bool:
        return self._pos + step == len(self._tokens) - 1

    def __advance(self) -> None:
        if self.__is_eof():
            raise InterpreterException("already EOF")
        self._pos += 1

    def __peek(self, step = 0) -> Token:
        return self._tokens[self._pos+step]

    def __display_peek_info(self) -> str:
        tok = self.__peek()
        return "at line {}, type: {}, lexeme: {}".format(
            tok.line, tok.tokenType, tok.lexeme
        )

    def __is_eol(self) -> bool:
        return self.__peek().tokenType == TokenType.EOL

    def __match_tok_type(self, types: list[TokenType]) -> bool:
        curr_type = self.__peek().tokenType
        return any([tok_type == curr_type for tok_type in types])

    # unless a block statement is seen, statements are separated by lines
    def __advance_line(self):
        if self.__is_eol():
            self.__advance()
        elif not self.__is_eof():
            raise InterpreterException("Expected end of line after statement")

    # Statement parsing
    # TODO: Ensure newline token after reading each statement
    def __statement(self) -> Stmt:
        match self.__peek().tokenType:
            case TokenType.PRINT:
                return self.__print_statement()
            case TokenType.LENGTH:
                return self.__length_statement()
            case TokenType.IDENTIFIER:
                if not self.__is_eof():
                    if self.__peek(1).tokenType == TokenType.LEFT_ARROW:
                        return self.__assignment_statement()
                    if self.__peek(1).tokenType == TokenType.LEFT_BRACKET and not self.__is_eof(4):
                        if self.__peek(4).tokenType == TokenType.LEFT_ARROW:
                            return self.__array_assignment_statement()
            case TokenType.FUNC_DECL:
                return self.__func_def()
            case TokenType.START_SCOPE:
                return self.__block_statement()
            case TokenType.IF:
                return self.__if_statement()
            case TokenType.WHILE:
                return self.__while_statement()
            case TokenType.RETURN:
                return self.__visit_return_statement()
        return self.__expression_statement()

    def __while_statement(self) -> Stmt:
        self.__advance()

        if not self.__match_tok_type([TokenType.LEFT_PAREN]):
            raise InterpreterException("Expected '(' after 'while'")
        self.__advance()

        condition_expr = self.__expression()

        if not self.__match_tok_type([TokenType.RIGHT_PAREN]):
            raise InterpreterException("Expected ')' after while statement condition")
        self.__advance()

        self.__advance_line()

        return stmt.While(condition_expr, self.__statement())

    def __if_statement(self) -> Stmt:
        self.__advance()
        if not self.__match_tok_type([TokenType.LEFT_PAREN]):
            raise InterpreterException("Expected '(' after 'if'")

        self.__advance()

        condition_expr = self.__expression()

        if not self.__match_tok_type([TokenType.RIGHT_PAREN]):
            raise InterpreterException("Expected ')' after if statement condition")

        self.__advance()

        # ensuring new line
        self.__advance_line()

        then_block = self.__statement()

        else_block = None
        if self.__match_tok_type([TokenType.ELSE]):
            self.__advance()

            # ensuring new line
            self.__advance_line()

            else_block = self.__statement()

        return stmt.If(condition_expr, then_block, else_block)

    def __block_statement(self) -> Stmt:
        self.__advance()
        statements: list[Stmt] = []

        while self.__peek().tokenType != TokenType.END_SCOPE and not self.__is_eof():
            statements.append(self.__statement())
        
        if self.__match_tok_type([TokenType.END_SCOPE]):
            self.__advance()
            return stmt.Block(statements)

        raise InterpreterException("expected end of block but reached: ", self.__peek())

    def __print_statement(self) -> Stmt:
        self.__advance()
        val = self.__expression()

        self.__advance_line()

        return stmt.Print(val)

    def __assignment_statement(self) -> Stmt:
        assignment = stmt.Assignment(self.__peek().lexeme, None)
        self.__advance()
        self.__advance()
        assignment.value = self.__expression()

        self.__advance_line()

        return assignment

    def __array_assignment_statement(self) -> Stmt:
        identifier = self.__peek().lexeme

        self.__advance()
        self.__advance()

        index = self.__expression()

        self.__advance()
        self.__advance()

        print(self.__peek())
        value = self.__expression()

        self.__advance_line()

        return stmt.ArrayAssignment(identifier, index, value)


    def __func_call(self, func_name) -> Expr:
        params = []
        self.__advance()
        while not(self.__is_eof()) and not(self.__is_eol()) and self.__peek().tokenType != TokenType.RIGHT_PAREN:
            params.append(self.__expression())
            if self.__peek().tokenType == TokenType.RIGHT_PAREN:
                break
            elif self.__peek().tokenType == TokenType.COMMA:
                self.__advance()
            else:
                raise Exception("Expected ',' between parameter names")

        if self.__peek().tokenType != TokenType.RIGHT_PAREN:
            raise Exception("Expected ')' after function call")
        self.__advance()
        return expr.FuncCall(func_name, params)

    def __func_def(self) -> Stmt:
        self.__advance()
        func_name = self.__peek().lexeme
        self.__advance()  # skip function name

        if self.__peek().tokenType != TokenType.LEFT_PAREN:
            raise Exception("Expected '(' after function name")
        self.__advance()  # skip '('

        params = []
        while not self.__is_eof() and self.__peek().tokenType != TokenType.RIGHT_PAREN:
            if self.__peek().tokenType != TokenType.IDENTIFIER:
                raise Exception("Expected parameter name")
            params.append(self.__peek().lexeme)
            self.__advance()

            if self.__peek().tokenType == TokenType.COMMA:
                self.__advance()
            elif self.__peek().tokenType != TokenType.RIGHT_PAREN:
                raise Exception("Expected ',' or ')' after parameter")

        if self.__peek().tokenType != TokenType.RIGHT_PAREN:
            raise Exception("Expected ')' after parameters")
        self.__advance()  # skip ')'

        if not self.__is_eol():
            raise Exception("Expected newline after function declaration")
        self.__advance_line()  # skip newline

        if self.__peek().tokenType != TokenType.START_SCOPE:
            raise Exception("Expected a code block after function declaration")
        self._is_in_func_def = True
        block = self.__block_statement()
        self._is_in_func_def = False

        return FuncDef(func_name, FuncBody(params, block))

    def __visit_return_statement(self):
        if not self._is_in_func_def:
            raise Exception("Error: cannot Return outside of function body")
        self.__advance()
        ret = stmt.Return(expr.Void())
        if not(self.__peek().tokenType == TokenType.EOL):
            ret = stmt.Return(self.__expression())
        self.__advance()
        return ret

    def __expression_statement(self) -> Stmt:
        val = self.__expression()

        self.__advance_line()

        return stmt.Expression(val)

    # Mutually recursing expression parsing
    def __expression(self) -> Expr:
        return self.__logical_or()

    def __logical_or(self) -> Expr:
        left_expr = self.__logical_and()

        while self.__match_tok_type([TokenType.OR]):
            operator = self.__peek()
            self.__advance()

            right_expr = self.__logical_and()

            left_expr = expr.Logical(left_expr, operator, right_expr)

        return left_expr

    def __logical_and(self) -> Expr:
        left_expr = self.__equality()

        while self.__match_tok_type([TokenType.AND]):
            operator = self.__peek()
            self.__advance()

            right_expr = self.__equality()

            left_expr = expr.Logical(left_expr, operator, right_expr)

        return left_expr

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
        if self.__peek().tokenType == TokenType.LENGTH and not self.__is_eof():
            self.__advance()
            val = self.__expression()

            while isinstance(val, expr.Grouping):
                val = val.expression

            if not (isinstance(val, expr.Literal) and val.value.tokenType == TokenType.IDENTIFIER):
                raise InterpreterException("Cannot get length of non-identifier objects")

            name = val.value.lexeme

            return expr.Length(name)

        if self.__peek().tokenType == TokenType.IDENTIFIER:
            literal = self.__peek()
            if not self.__is_eof():
                name =literal.lexeme
                if self.__peek(1).tokenType == TokenType.LEFT_BRACKET:
                    self.__advance()
                    self.__advance()

                    index = self.__expression()

                    if not self.__match_tok_type([TokenType.RIGHT_BRACKET]):
                        raise InterpreterException("{}: expected ']' after array indexing".format(self.__display_peek_info()))

                    self.__advance()

                    return expr.ArrayAccess(name, index)
                elif self.__peek(1).tokenType == TokenType.LEFT_PAREN:
                    self.__advance()
                    return self.__func_call(name)
                else:
                    if not self.__is_eof():
                        self.__advance()
                    return expr.Literal(literal)

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
                raise InterpreterException("{}: expected ')'".format(self.__display_peek_info()))

            self.__advance()
            return expr.Grouping(grouping_expr)

        if self.__match_tok_type([TokenType.LEFT_BRACKET]):
            self.__advance()

            elts: list[Expr] = [self.__expression()]
            while self.__match_tok_type([TokenType.COMMA]):
                self.__advance()

                elt = self.__expression()
                elts.append(elt)

            if not self.__match_tok_type([TokenType.RIGHT_BRACKET]):
                raise InterpreterException("{}: expected ']'".format(self.__display_peek_info()))
            self.__advance()

            return expr.ArrayLiteral(elts)

        raise InterpreterException("{}: expected expression".format(self.__display_peek_info()))
