class NumberNode:

    def __init__(self, token):
        self.token = token
        self.start_position = self.token.start_position
        self.end_position = self.token.end_position

    def __repr__(self):
        return f"{self.token.value}"


class UnaryOperatorNode:

    def __init__(self, left, value):
        self.left = left
        self.value = value
        self.start_position: Position = self.left.start_position
        self.end_position: Position = self.value.end_position

    def __repr__(self):
        return f"({self.left} {self.value})"



class BinaryOperatorNode:

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        self.start_position: Position = self.left.start_position
        self.end_position: Position = self.right.end_position

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"
