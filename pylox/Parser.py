from TokenType import TokenType
import Expr


class Parser:
    """Class to parse tokens into AST"""

    def __init__(self, tokens, error_report):
        self.tokens = tokens
        self.current = 0
        self.error_report = error_report

        self.synchronize_keys = {
            TokenType.CLASS: 1,
            TokenType.FUN: 1,
            TokenType.VAR: 1,
            TokenType.FOR: 1,
            TokenType.IF: 1,
            TokenType.WHILE: 1,
            TokenType.PRINT: 1,
            TokenType.RETURN: 1,
        }

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.match(TokenType.NIL):
            return Expr.Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        self.consume(None, "Unexpected token")

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token, message):
        self.error_report.token_error(token, message)
        return SyntaxError()

    def match(self, *token_types):
        """
        If any of the tokens match, return True and advance else return False
        """

        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def advance(self):
        """Return current token and move current one step forward"""
        if not self.at_end():
            self.current += 1
        return self.previous()

    def check(self, token_type):
        """Check if token type matches current token"""
        if self.at_end():
            return False
        return self.peek().type == token_type

    def peek(self):
        """Return current token"""
        return self.tokens[self.current]

    def at_end(self):
        """Return if at end"""
        return self.peek().type == TokenType.EOF

    def previous(self):
        """Return previous token"""
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()

        while not self.at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in self.synchronize_keys:
                return

            self.advance()

    def parse(self):
        try:
            return self.expression()
        except SyntaxError as error:
            return None
