from Token import Token
from TokenType import TokenType


class RuntimeError(Exception):
    pass


class Expr:
    def isTruthy(self, value):
        if value == None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def interpret(self):
        try:
            return self.eval()
        except RuntimeError as e:
            print("RuntimeError:", e)
            return None

    def eval(self):
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

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        ttype = self.operator.type

        try:
            if ttype == TokenType.MINUS:
                return float(left) - float(right)
            elif ttype == TokenType.SLASH:
                return float(left) / float(right)
            elif ttype == TokenType.STAR:
                return float(left) * float(right)
            elif ttype == TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
            elif ttype == TokenType.GREATER:
                return float(left) > float(right)
            elif ttype == TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            elif ttype == TokenType.LESS:
                return float(left) < float(right)
            elif ttype == TokenType.LESS_EQUAL:
                return float(left) <= float(right)
            elif ttype == TokenType.BANG_EQUAL:
                return left != right
            elif ttype == TokenType.EQUAL_EQUAL:
                return left == right
        except:
            raise RuntimeError(f"At line {self.operator.line}")

        # Unreachable
        raise RuntimeError(f"At line {self.operator.line}")


class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return parenthesize("group", self.expr)

    def eval(self):
        return self.expr.eval()


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value:
            return str(self.value)
        else:
            return "nil"

    def eval(self):
        return self.value


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __str__(self):
        return parenthesize(self.operator, self.right)

    def eval(self):
        right = self.right.eval()

        valueMap = {
            TokenType.MINUS: -float(right),
            TokenType.BANG: self.isTruthy(right),
        }

        if self.operator.type in valueMap:
            try:
                return valueMap[self.operator.type]
            except:
                raise RuntimeError(f"At line {self.operator.line}")

        # Unreachable
        raise RuntimeError(f"At line {self.operator.line}")
