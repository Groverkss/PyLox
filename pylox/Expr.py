from Token import Token
from TokenType import TokenType


class Expr:
    pass


def parenthesize(*args):
    args = list(map(lambda x: str(x), args))
    string = " ".join(args)
    return "(" + string + ")"


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return parenthesize(self.operator, self.left, self.right)


class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return parenthesize("group", self.expr)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value:
            return str(self.value)
        else:
            return "nil"


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __str__(self):
        return parenthesize(self.operator, self.right)
