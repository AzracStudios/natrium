from ir import *

class CodeGen:

    def visit(self, ast):
        return self.__getattribute__(f"visit_{type(ast).__name__}")(ast)

    def visit_NumberNode(self, node):
        return NumberIR(node)

    def visit_BinaryOperatorNode(self, node):
        left = self.visit(node.left)
        operator = node.operator
        right = self.visit(node.right)

        return BinaryOperatorIR(left, operator, right)