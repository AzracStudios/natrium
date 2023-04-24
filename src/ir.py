from utils import check_type
from token import *

class NumberIR:

    def __init__(self, node):
        self.node = node
        self.code = ""

    def generate(self):
        self.code = f"{self.node.token.value}"
        return self


class BinaryOperatorIR:

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        self.code = ""

    def generate(self):
        left = self.left.generate()
        op = self.operator.type
        right = self.right.generate()

        if check_type(left, BinaryOperatorIR):
            self.code += left.code

            ## a:BINOP_IR op:TOKEN b:BINOP_IR
            ## compute a
            ## result of a -> rcx
            ## compute b
            ## result of b -> rbx
            ## result of a in rcx -> rax
            ## compute (a op b)
            ## result (a op b) -> rax

            if check_type(right, BinaryOperatorIR):
                self.code += f"mov rcx, rax\n"
                self.code += right.code
                self.code += "mov rbx, rax\n"
                self.code += "mov rax, rcx\n"
                if op == TT_PLUS:
                    self.code += f"add rax, rbx\n"
                if op == TT_MINUS:
                    self.code += f"sub rax, rbx\n"
                if op == TT_MUL:
                    self.code += f"mul rbx\n"
                if op == TT_DIV:
                    self.code += f"div rbx\n"

        
        if check_type(left, NumberIR):
            ## a:NUMBER_IR op:TOKEN b:BINOP_IR
            ## compute b
            ## result of b in rax -> rcx
            ## number a -> rax
            ## compute (a op b)
            ## result (a op b) -> rax

            if check_type(right, BinaryOperatorIR):
                self.code += right.code
                self.code += f"mov rcx, rax\n"
                self.code += f"mov rax, {left.code}\n"
                if op == TT_PLUS:
                    self.code += f"add rax, rcx\n"
                if op == TT_MINUS:
                    self.code += f"sub rax, rcx\n"
                if op == TT_MUL:
                    self.code += f"mul rcx\n"
                if op == TT_DIV:
                    self.code += f"div rcx\n"

            ## number a -> rax
            else:
                self.code += f"mov rax, {left.code}\n"

        
        ## a:NUMBER_IR op b:NUMBER_IR
        ## number a -> rax
        ## number b -> rbx ? mul || div
        ## compute (a op b)
        ## result (a op b) -> rax

        if check_type(right, NumberIR):
            if op == TT_PLUS:
                self.code += f"add rax, {right.code}\n"
            if op == TT_MINUS:
                self.code += f"sub rax, {right.code}\n"
            if op == TT_MUL:
                self.code += f"mov rbx, {right.code}\n"
                self.code += f"mul rbx\n"
            if op == TT_DIV:
                self.code += f"mov rbx, {right.code}\n"
                self.code += f"div rbx\n"

        return self