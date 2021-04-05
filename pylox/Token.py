class Token:
    """Token representation class"""

    def __init__(self, token_type, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        if self.lexeme:
            return self.type.name + ": " + self.lexeme
        else:
            return self.type.name