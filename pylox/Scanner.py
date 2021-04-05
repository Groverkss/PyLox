from Token import Token
from TokenType import TokenType


class Scanner:
    """Class to tokenize and do lexical analysis on source code"""

    def __init__(self, source, error_report):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

        self.error_report = error_report

        self.single_chars = {
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_BRACE,
            "}": TokenType.RIGHT_BRACE,
            ",": TokenType.COMMA,
            ".": TokenType.DOT,
            "-": TokenType.MINUS,
            "+": TokenType.PLUS,
            ";": TokenType.SEMICOLON,
            "*": TokenType.STAR,
        }

        self.double_chars = {
            "!": [TokenType.BANG, TokenType.BANG_EQUAL],
            "=": [TokenType.EQUAL, TokenType.EQUAL_EQUAL],
            "<": [TokenType.LESS, TokenType.LESS_EQUAL],
            ">": [TokenType.GREATER, TokenType.GREATER_EQUAL],
        }

        self.reserved_chars = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

        self.ignore_chars = set([" ", "\r", "\t"])

    def at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        """Return current character and go to next character"""
        ret = self.source[self.current]
        self.current += 1
        return ret

    def match(self, char):
        """
        Advances only if the current character matches char
        and returns if matching
        """
        if self.at_end():
            return False
        elif self.source[self.current] != char:
            return False

        self.current += 1
        return True

    def peek(self):
        """Returns the charcter at current"""
        if self.at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        """Return the character at current + 1"""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def add_token(self, token_type, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def add_string(self):
        while self.peek() != '"' and not self.at_end():
            if self.peek == "\n":
                self.line += 1
            self.advance()

        if self.at_end():
            self.error_report(self.line, "Unterminated string")

        self.advance()

        string_val = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, string_val)

    def add_number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(
            TokenType.NUMBER, float(self.source[self.start : self.current])
        )

    def add_identifier(self):
        while self.peek().isalpha():
            self.advance()

        token_val = self.source[self.start : self.current]
        if token_val in self.reserved_chars:
            self.add_token(self.reserved_chars[token_val])
        else:
            self.add_token(TokenType.IDENTIFIER, token_val)

    def scan_tokens(self):
        """Tokenizes the source code passed to a list of tokens"""
        while not self.at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        """Reads a complete token and appends it to tokens list"""
        c = self.advance()

        if c in self.single_chars:
            self.add_token(self.single_chars[c])
        elif c in self.double_chars:
            token_type = self.double_chars[c][self.match("=")]
            self.add_token(token_type)
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c in self.ignore_chars:
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.add_string()
        elif c.isdigit():
            self.add_number()
        elif c.isalpha():
            self.add_identifier()
        else:
            self.error_report.error(self.line, "Unexpected Character")
